from fastapi import FastAPI, HTTPException
from db.database import test_connection, SessionLocal,Base, engine
from repository.node.node_repository import create_node
from repository.seed.seed_repository import seed_graph
from dotenv import load_dotenv
from models.node_model import Node
from models.cais_model import Cai
from repository.cai.cai_repository import create_cai, get_all_cais
from repository.node.node_repository import get_nodes
# from sqlalchemy import inspect

load_dotenv()

# if not inspect(engine).has_table('nodes') or not inspect(engine).has_table('edges'):
#     # Create the tables if they do not exist
#     Base.metadata.create_all(bind=engine)
#Base.metadata.create_all(bind=engine)

app = FastAPI()



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




@app.post("/create_cai")
async def create_cai_controller(id: int, localidad: str, nombre: str, lat: float, lon: float):
    try:
        db = SessionLocal()
        cai = create_cai(db, id=id, localidad=localidad, nombre=nombre, lat=lat, lon=lon)
        return {
            "message": "CAI created successfully",
            "cai": {
                "id": cai.id,
                "localidad": cai.localidad,
                "nombre": cai.nombre,
                "lat": cai.lat,
                "lon": cai.lon,
            }
        }
    except Exception as e:
        return {"message": f"Error creating CAI: {e}"}
    finally:
        db.close()

@app.get("/cais")
async def get_cais_controller():
    try:
        db = SessionLocal()
        cais = get_all_cais(db)
        return {
            "message": "CAIs fetched successfully",
            "cais": [
                {
                    "id": cai.id,
                    "localidad": cai.localidad,
                    "nombre": cai.nombre,
                    "lat": cai.lat,
                    "lon": cai.lon,
                } for cai in cais
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CAIs: {str(e)}")
    finally:
        db.close()
