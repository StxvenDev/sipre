from fastapi import FastAPI, HTTPException
from db.database import test_connection, SessionLocal,Base, engine
from repository.node.node_repository import create_node
from repository.seed.seed_repository import seed_graph
from models.node_model import Node
from repository.node.node_repository import get_nodes
from repository.edge.edge_repository import upload_data_layer
# from sqlalchemy import inspect


# if not inspect(engine).has_table('nodes') or not inspect(engine).has_table('edges'):
#     # Create the tables if they do not exist
# Base.metadata.create_all(bind=engine)


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_node")
async def create_node_controller():
    try:
        # Simulate creating a node
        db = SessionLocal()
        node = create_node(db, id=1, lat=123456, lon=654321)
        return {
                "message": "Node created successfully",
                "node": node
                }
    except Exception as e:
        return {"message": f"Error creating node: {e}"}
    finally:
        db.close()


@app.post("/SEED")
async def seed():
    try:
        db = SessionLocal()
        seed_graph(db)
        return {
                "message": "successfully seeded",
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar nodos: {str(e)}")
    finally:
        db.close()


@app.get("/upload_data_layer")
async def upload_data():
    try:
        db = SessionLocal()
        edges = await upload_data_layer(db)
        return {
                "message": "successfully fetched",
                "edges": edges
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las aristas: {str(e)}")
    finally:
        db.close()




@app.get("/test_connection")
async def test_connection_controller():
    try:
        test_connection()
        return {"message": "Connection successful"}
    except Exception as e:
        return {"message": f"Connection failed: {e}"}
    

@app.get("/nodes_db")
async def get_nodes_db():
    try:
        db = SessionLocal()
        nodes = await get_nodes(db)
        return {
                "message": "successfully fetched",
                "nodes": nodes
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los nodos: {str(e)}")
    finally:
        db.close()



