from sqlalchemy.orm import Session
from models.node_model import Node
from models.edge_model import Edge
import osmnx as ox
import random


def calculate_edge_weight(length, num_cais, estrato, cams, traffic, weight_factors=None):
    """
    Calcula el peso de una arista de forma flexible y escalable.
    Permite ajustar la importancia de cada factor mediante weight_factors.
    """
    if weight_factors is None:
        weight_factors = {
            'length': 1.0,
            'num_cais': 1.0,
            'estrato': 1.0,
            'cams': 1.0,
            'traffic': 1.0
        }
    return (
        weight_factors['length'] * length +
        weight_factors['num_cais'] * num_cais +
        weight_factors['estrato'] * estrato +
        weight_factors['cams'] * cams +
        weight_factors['traffic'] * traffic
    )

def seed_graph(db: Session, estrato_1_limit=200, weight_factors=None):
    """
    Crea nodos y aristas en la base de datos a partir de un grafo de OSMnx.
    Permite ajustar el límite de estrato 1 y los factores de peso.
    """
    G = ox.graph_from_place('Cartagena, Colombia', network_type='drive')
    nodes_gdf, edges_gdf = ox.graph_to_gdfs(G)
    _seed_nodes(db, nodes_gdf)
    _seed_edges(db, edges_gdf, estrato_1_limit=estrato_1_limit, weight_factors=weight_factors)

def _seed_nodes(db: Session, nodes_gdf):
    """Inserta nodos en la base de datos desde el GeoDataFrame de nodos."""
    nodes_gdf.reset_index(inplace=True)
    for _, row in nodes_gdf.iterrows():
        node = Node(
            id=row['osmid'],
            lat=row['y'],
            lon=row['x']
        )
        db.add(node)
    db.commit()

def _seed_edges(db: Session, edges_gdf, estrato_1_limit=200, weight_factors=None):
    """Inserta aristas en la base de datos desde el GeoDataFrame de aristas."""
    edges_gdf.reset_index(inplace=True)
    for index, row in edges_gdf.iterrows():
        if row['u'] == row['v']:
            continue
        num_cais = random.randint(1, 3)
        estrato = 1 if index < estrato_1_limit else random.randint(2, 6)
        cams = random.randint(1, 5)
        length = row['length']
        traffic = random.randint(1, 10)
        # Validación de datos para evitar pesos negativos o nulos
        if length is None or length <= 0:
            print(f"Advertencia: longitud inválida en arista {row['u']}->{row['v']}. Se omite.")
            continue
        weight = calculate_edge_weight(length, num_cais, estrato, cams, traffic, weight_factors)
        if weight <= 0:
            print(f"Advertencia: peso no positivo en arista {row['u']}->{row['v']}. Se omite.")
            continue

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