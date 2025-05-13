from sqlalchemy import Column, String, Float, Integer, BigInteger
from db.database import Base

class Cai(Base):
    __tablename__ = "cais"

    id = Column(BigInteger, primary_key=True, index=True)
    localidad = Column(String(100), nullable=False)
    nombre = Column(String(100), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    def __repr__(self):
        return f"Cai(id={self.id}, localidad='{self.localidad}', nombre='{self.nombre}', lat={self.lat}, lon={self.lon})"
