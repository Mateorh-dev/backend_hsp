from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from ..core.database import Database
from ..model.models import EstadoCita
# from ..model.schemas import DataEstadoCitaId

db = Database()

router = APIRouter(tags=["EstadoCita"])

@router.get("/select/estadocita")
def consultar_estadocita():
    session  = db.SessionLocal()
    try:
        request = select(EstadoCita)
        estados = session.execute(request).scalars().all()
        return estados
    except SQLAlchemyError as e:
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
    
"""
@router.get("/select/like/estadocita")
def consultar_like_estadocita():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
    
@router.post("/insert/estadocita")
def registrar_estadocita():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
    

@router.put("/update/estadocita")
def actualizar_estadocita():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
    

@router.delete("/delete/estadocita")
def eliminar_estadocita():
    session  = db.SessionLocal()
    try:
        pass
    except:
        pass
    finally:
        session.close()
"""
