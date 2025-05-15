from sqlalchemy.orm import Session
from models.node_model import Node
from models.edge_model import Edge
from db.database import SessionLocal
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_from_db():
    db = SessionLocal()
    nodes = db.query(Node).all()
    edges = db.query(Edge).all()
    db.close()

    G = nx.Graph()  # Usa nx.Graph() si tu grafo es no dirigido

    # Agrega nodos
    for node in nodes:
        G.add_node(node.id)

    # Agrega aristas
    for edge in edges:
        G.add_edge(edge.node_u, edge.node_v, weight=edge.weight)

    # Dibuja en consola (lista de adyacencia)
    print("GRAFO (formato: nodo -> [vecinos])")
    for node in G.nodes():
        print(f"{node} -> {list(G.neighbors(node))}")

    # Ejemplo: define tus nodos de inicio y fin
    start_id = 11642908296
    end_id = 7546194063

    # Calcula el camino más corto usando el peso
    path = nx.astar_path(G, start_id, end_id, weight='weight')

    # Dibuja todos los nodos y aristas
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False, node_color='lightblue', edge_color='gray')

    # Extrae las aristas del camino óptimo
    path_edges = list(zip(path, path[1:]))

    # Dibuja el camino óptimo en rojo
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.show()
