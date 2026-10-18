from fastapi import APIRouter
from ..core.database import Database
from ..model.schemas import 

db = Database()

session  = db.SessionLocal()
try:
    pass
except:
    pass
finally:
    session.close()

router = APIRouter(tags=[""])

@router.get("/select/")
def consultar_():
    return
@router.get("/select/like/")
def consultar_like_():
    return
@router.post("/insert/")
def registrar_():
    return
@router.put("/update/")
def actualizar_():
    return
@router.delete("/delete/")
def eliminar_():
    return
