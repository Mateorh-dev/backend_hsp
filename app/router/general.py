from fastapi import APIRouter
from ..core.database import Database
# from ..model.schemas import 

db = Database()

router = APIRouter()

@router.get("/selectall/")
def consultar_datos_general():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
