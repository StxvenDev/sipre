from sqlalchemy.orm import Session
from models.node_model import Node
from models.edge_model import Edge
import osmnx as ox
import random
def seed_graph(db: Session):
    G = ox.graph_from_place('Cartagena, Colombia', network_type='drive')
    nodes, edges = ox.graph_to_gdfs(G)
    # print(nodes.columns)
    # print(edges)
    nodes.reset_index(inplace=True)
        # print(f"De {u} a {v}, key={key}, longitud={data.get('length')}")
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

        sum_length=0
        if row['u'] != row['v']:
            sum_length += row['length']
            print(f"suma distancia {sum_length}")
        total_node = db.query(Node).count()
        avg_length = sum_length / total_node
        print(f"Promedio de longitud: {avg_length}")

        if row['u'] != row['v']:
            num_cais=random.randint(1, 2)
            estrato=random.randint(1, 6)
            cams=random.randint(1, 5)
            length=row['length']
            traffic=random.randint(1, 10)
            weight= (length / avg_length) + ((num_cais * 0.55) - (estrato * 0.4) + (cams * 0.3) + (traffic * 0.1))
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