from sqlalchemy.orm import Session
from models.node_model import Node
from models.edge_model import Edge
import osmnx as ox

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
        if row['u'] != row['v']:
          edge = Edge(
              # id=row['osmid'],
              node_u=row['u'],
              node_v=row['v'],
              length=row['length'],
              weight=0.0
          )
          db.add(edge)
    db.commit()