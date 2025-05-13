from sqlalchemy import Column, Float, BigInteger, ForeignKey, Integer
from db.database import Base


class Edge(Base):
    __tablename__ = "edges"

    id = Column(BigInteger, primary_key=True, index=True)
    # name = Column(String(50), nullable=False)
    node_u = Column(BigInteger, ForeignKey('nodes.id'),nullable=False)
    node_v = Column(BigInteger,ForeignKey('nodes.id'), nullable=False)
    length = Column(Float, nullable=True)
    num_cais = Column(Integer, nullable=False)
    estrato = Column(Integer, nullable=False)
    cams = Column(Integer, nullable=False)
    traffic = Column(Integer, nullable=False)
    weight = Column(Float, nullable=True)

    def __repr__(self):
        return f"Edge(id={self.id}, node_u={self.node_u}, node_v={self.node_v}, length={self.length}, weight={self.weight}), num_cais={self.num_cais}, estrato={self.estrato}, cams={self.cams}) traffic={self.traffic}"
    
    