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

    for index, row in edges.iterrows():
        if row['u'] != row['v']:
            num_cais = random.randint(1, 3)
            estrato = random.randint(1, 6)
            cams = random.randint(1, 5)
            length = row['length']
            traffic = random.randint(1, 10)
            weight = length  + num_cais + estrato + cams + traffic

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