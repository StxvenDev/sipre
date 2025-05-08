from sqlalchemy import Column, Float, BigInteger, ForeignKey
from db.database import Base


class Edge(Base):
    __tablename__ = "edges"

    id = Column(BigInteger, primary_key=True, index=True)
    # name = Column(String(50), nullable=False)
    node_u = Column(BigInteger, ForeignKey('nodes.id'),nullable=False)
    node_v = Column(BigInteger,ForeignKey('nodes.id'), nullable=False)
    length = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)

    def __repr__(self):
        return f"Edge(id={self.id}, node_u={self.node_u}, node_v={self.node_v}, length={self.length}, weight={self.weight})"
    
    