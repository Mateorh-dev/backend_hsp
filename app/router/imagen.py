from fastapi import APIRouter
from ..core.database import Database
# from ..model.schemas import 

db = Database()

router = APIRouter(tags=["Imagen"])

@router.get("/select/imagen")
def consultar_imagen():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
    

"""@router.get("/select/like/imagen")
def consultar_like_imagen():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
    
"""
@router.post("/insert/imagen")
def registrar_imagen():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
    

@router.put("/update/imagen")
def actualizar_imagen():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
    

@router.delete("/delete/imagen")
def eliminar_imagen():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
