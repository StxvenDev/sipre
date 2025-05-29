import networkx as nx
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from models.node_model import Node
from models.edge_model import Edge
from db.database import SessionLocal
import random
import math

def euclidean_heuristic(u, v, node_coords):
    lat1, lon1 = node_coords[u]
    lat2, lon2 = node_coords[v]
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def draw_graph():
    db = SessionLocal()
    nodes = db.query(Node.id, Node.lat, Node.lon).all()
    edges = db.query(Edge.node_u, Edge.node_v, Edge.weight, Edge.estrato).all()
    db.close()

    if not nodes or not edges:
        print("No hay nodos o aristas en la base de datos.")
        return

    G = nx.Graph()
    node_coords = {}
    for node_id, lat, lon in nodes:
        G.add_node(node_id, pos=(lat, lon))
        node_coords[node_id] = (lat, lon)

    for u, v, weight, estrato in edges:
        G.add_edge(u, v, weight=weight, estrato=estrato)

    # Buscar nodos conectados a aristas con estrato 1 o 2
    estrato_nodes = set()
    for u, v, _, estrato in edges:
        if estrato == 1:
            estrato_nodes.add(u)
            estrato_nodes.add(v)
    estrato_nodes = list(estrato_nodes)
    if not estrato_nodes:
        print("No hay nodos conectados a aristas con estrato 1 ")
        return

    # start_node = nodes[0][0]
    start_node = 1091385678
    end_node = random.choice(estrato_nodes)

    print(f"Buscando camino desde {start_node} hasta {end_node} (estrato 1 )")

    try:
        path = nx.astar_path(
            G,
            start_node,
            end_node,
            heuristic=lambda u, v: euclidean_heuristic(u, v, node_coords),
            weight='weight'
        )
        print("Camino más corto (A*):", path)
    except nx.NetworkXNoPath:
        print("No hay camino entre los nodos seleccionados.")
        path = []

    pos = {node: (lon, lat) for node, lat, lon in nodes}  # Para que el eje X sea longitud
    plt.figure(figsize=(8, 8))

    # Colorea las aristas
    edge_colors = []
    for u, v in G.edges():
        if (u, v) in zip(path, path[1:]) or (v, u) in zip(path, path[1:]):
            edge_colors.append("red")
        elif G[u][v]['estrato'] == 1:
            edge_colors.append("yellow")
        else:
            edge_colors.append("gray")

    # Dibuja todos los nodos en gris claro
    nx.draw(
        G, pos,
        node_size=0,
        with_labels=False,
        edge_color=edge_colors,
        width=2,
        node_color="#cccccc"
    )

    # Dibuja el nodo inicial en verde y el final en azul, con mayor tamaño
    nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_color="green", node_size=100, label="Inicio")
    nx.draw_networkx_nodes(G, pos, nodelist=[end_node], node_color="blue", node_size=100, label="Fin")

    # Etiquetas solo para inicio y fin, incluyendo coordenadas
    start_label = f"Inicio\n({node_coords[start_node][0]:.4f}, {node_coords[start_node][1]:.4f})"
    end_label = f"Fin\n({node_coords[end_node][0]:.4f}, {node_coords[end_node][1]:.4f})"
    nx.draw_networkx_labels(
        G, pos,
        labels={start_node: start_label, end_node: end_label},
        font_color="black",
        font_size=10
    )

    plt.legend(["Inicio", "Fin"])
    plt.savefig("grafo.png")
    plt.close()
    print("Imagen del grafo guardada como grafo.png")
