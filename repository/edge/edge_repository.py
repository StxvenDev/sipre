from sqlalchemy.orm import Session
from models.edge_model import Edge
import osmnx as ox

def upload_data_layer(db: Session):
    edge = db.query(Edge).all()
    return edge

    
