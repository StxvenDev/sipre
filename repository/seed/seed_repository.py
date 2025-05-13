from sqlalchemy.orm import Session
from models.node_model import Node
from models.edge_model import Edge
import osmnx as ox
import random

def seed_graph(db: Session):
    G = ox.graph_from_place('Cartagena, Colombia', network_type='drive')
    nodes, edges = ox.graph_to_gdfs(G)
    nodes.reset_index(inplace=True)
    for index, row in nodes.iterrows():
        node = Node(
            id=row['osmid'],
            lat=row['y'],
            lon=row['x']
        )
        db.add(node)
    db.commit()
    edges.reset_index(inplace=True)

    # Calcular el promedio de longitud de todas las aristas válidas
    valid_lengths = edges[edges['u'] != edges['v']]['length']
    total_node = db.query(Node).count()
    avg_length = valid_lengths.sum() / total_node if total_node else 1

    for index, row in edges.iterrows():
        if row['u'] != row['v']:
            num_cais = random.randint(1, 3)
            estrato = random.randint(1, 6)
            cams = random.randint(1, 5)
            length = row['length']
            traffic = random.randint(1, 10)

            # Normalización de variables
            norm_length = length / avg_length if avg_length else 1
            norm_estrato = (estrato - 1) / 5  # estrato de 1 a 6 → 0 a 1
            norm_cams = (cams - 1) / 4        # cams de 1 a 5 → 0 a 1
            norm_traffic = (traffic - 1) / 9  # traffic de 1 a 10 → 0 a 1
            norm_cais = (num_cais - 1) / 2    # num_cais de 1 a 3 → 0 a 1

            # Nueva fórmula ponderada
            weight = (
                (norm_length) +
                0.8 * norm_cais +
                0.5 * norm_cams +
                0.35 * norm_traffic -
                0.4 * norm_estrato
            )

            edge = Edge(
                node_u=row['u'],
                node_v=row['v'],
                length=length,
                num_cais=num_cais,
                estrato=estrato,
                cams=cams,
                traffic=traffic,
                weight=weight
            )
            db.add(edge)
    db.commit()