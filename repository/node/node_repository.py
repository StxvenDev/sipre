from sqlalchemy.orm import Session
from models.node_model import Node
import osmnx as ox

def create_node(db: Session, id: int, lat: float, lon: float):
    node = Node(
        id=id,
        lat=lat,
        lon=lon
    )
    db.add(node)
    db.commit()
    db.refresh(node)
    return node.__repr__()




def get_nodes(db: Session):
    return db.query(Node).all()
