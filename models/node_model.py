from sqlalchemy import Column, Float, BigInteger
from db.database import Base


class Node(Base):
    __tablename__ = "nodes"

    id = Column(BigInteger, primary_key=True, index=True)
    # name = Column(String(50), nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    def __repr__(self):
        return f"Node(id={self.id}, latitude={self.lat}, longitude={self.lon})"
    
    