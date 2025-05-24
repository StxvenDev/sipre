import igraph as ig
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from models.node_model import Node
from models.edge_model import Edge
from db.database import SessionLocal

def draw_graph():
    db = SessionLocal()
    nodes = db.query(Node.id).all()
    edges = db.query(Edge.node_u, Edge.node_v, Edge.weight).all()
    db.close()

    if not nodes or not edges:
        print("No hay nodos o aristas en la base de datos.")
        return

    node_ids = [n[0] for n in nodes]
    id_to_index = {node_id: idx for idx, node_id in enumerate(node_ids)}
    ig_edges = [(id_to_index[e[0]], id_to_index[e[1]]) for e in edges]
    weights = [e[2] for e in edges]

    g = ig.Graph()
    g.add_vertices(len(node_ids))
    g.add_edges(ig_edges)
    g.es['weight'] = weights

    print("GRAFO (formato: nodo -> [vecinos])")
    for idx, node_id in enumerate(node_ids[:50]):
        neighbors = [node_ids[n] for n in g.neighbors(idx)]
        print(f"{node_id} -> {neighbors}")

    start_idx = 0
    end_idx = len(node_ids) - 1

    if g.vcount() < 1000000000000000:
        path = g.get_shortest_paths(start_idx, to=end_idx, weights='weight', output='vpath')[0]
        print("Camino más corto:", [node_ids[i] for i in path])
        layout = g.layout("auto")
        ig.plot(
            g,
            layout=layout,
            vertex_label=None,
            edge_color=["red" if (e.source in path and e.target in path) else "gray" for e in g.es],
            bbox=(600, 600),
            target="grafo.png",  # Guarda la imagen
            vertex_size=1    # Tamaño pequeño para los nodos
        )
        print("Imagen del grafo guardada como grafo.png")
        # plt.show()  # No necesario en entorno web
    else:
        print("El grafo es demasiado grande para calcular el camino o dibujarlo.")
