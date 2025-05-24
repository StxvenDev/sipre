from sqlalchemy.orm import Session
from models.node_model import Node
from models.edge_model import Edge
import osmnx as ox
import random
import math

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

    def calculate_straight_line_distance(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine para distancia en línea recta
        R = 6371  # Radio de la Tierra en km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        try:
            a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
            # a = max(0.0, min(1.0, a))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) 
            print(f"Distancia entre ({lat1}, {lon1}) y ({lat2}, {lon2}): {R * c * 1000} m")
            return R * c * 1000 
        except ValueError as e:
            print(a);
            print(f"Error calculando distancia entre ({lat1}, {lon1}) y ({lat2}, {lon2}): {e}")
            raise


        

    for index, row in edges.iterrows():
        if row['u'] != row['v']:
            num_cais = random.randint(1, 3)
            estrato = random.randint(1, 6)
            cams = random.randint(1, 5)
            length = row['length'] if row['length'] > 0 else 1
            traffic = random.randint(1, 10)

            # Obtener lat/lon desde la base de datos
            node_u = db.query(Node).filter(Node.id == row['u']).first()
            node_v = db.query(Node).filter(Node.id == row['v']).first()

            if not node_u or not node_v:
                continue  # saltar si no están los nodos

            straight_line = calculate_straight_line_distance(node_u.lat, node_u.lon, node_v.lat, node_v.lon)

            # Peso total sin normalización ni ponderaciones
            weight = length + straight_line + num_cais + estrato + cams + traffic

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




