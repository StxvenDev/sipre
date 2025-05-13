from sqlalchemy.orm import Session
from models.cais_model import Cai

def create_cai(db: Session, id: int, localidad: str, nombre: str, lat: float, lon: float):
    cai = Cai(id=id, localidad=localidad, nombre=nombre, lat=lat, lon=lon)
    db.add(cai)
    db.commit()
    db.refresh(cai)
    return cai

def get_all_cais(db: Session):
    return db.query(Cai).all()
