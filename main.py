from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import inspect

from db.database import test_connection, SessionLocal, Base, engine
from repository.node.node_repository import create_node, get_nodes
from repository.seed.seed_repository import seed_graph
from repository.edge.edge_repository import upload_data_layer
from services.edge_services import draw_graph


def create_tables_if_not_exist():
    """Crea las tablas requeridas si no existen en la base de datos."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    required_tables = set(Base.metadata.tables.keys())
    missing_tables = required_tables - tables
    if missing_tables:
        print(f"Creando tablas faltantes: {missing_tables}")
        Base.metadata.create_all(bind=engine)
    else:
        print("Todas las tablas requeridas ya existen.")


create_tables_if_not_exist()

app = FastAPI()


@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API está activa."""
    return {"message": "Hello World"}


@app.post("/create_node")
async def create_node_controller():
    """Crea un nodo de ejemplo en la base de datos."""
    db = SessionLocal()
    try:
        node = create_node(db, id=1, lat=123456, lon=654321)
        return {"message": "Node created successfully", "node": node}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating node: {e}")
    finally:
        db.close()


@app.post("/seed_graph")
async def seed_graph_endpoint():
    """Puebla la base de datos con nodos y aristas desde OSMnx."""
    db = SessionLocal()
    try:
        seed_graph(db)
        return {"message": "successfully seeded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al poblar la base de datos: {str(e)}")
    finally:
        db.close()


@app.get("/upload_data_layer")
async def upload_data():
    """Obtiene las aristas de la base de datos."""
    db = SessionLocal()
    try:
        edges = await upload_data_layer(db)
        return {"message": "successfully fetched", "edges": edges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las aristas: {str(e)}")
    finally:
        db.close()


@app.get("/test_connection")
async def test_connection_controller():
    """Verifica la conexión con la base de datos."""
    try:
        test_connection()
        return {"message": "Connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}")


@app.get("/nodes_db")
async def get_nodes_db():
    """Obtiene los nodos de la base de datos."""
    db = SessionLocal()
    try:
        nodes = await get_nodes(db)
        return {"message": "successfully fetched", "nodes": nodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los nodos: {str(e)}")
    finally:
        db.close()


@app.get("/draw_graph")
async def draw_graph_db():
    """Genera y devuelve una imagen del grafo actual."""
    draw_graph()
    return FileResponse("grafo.png", media_type="image/png")


