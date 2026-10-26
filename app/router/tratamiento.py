from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from ..core.database import Database
from ..model.models import Tratamiento
from ..model.schemas import DataTratamientoCreate, DataTratamientoUpdate, DataTratamientoId
from ..model.hash import generar_hash

db = Database()

router = APIRouter(tags=["Tratamiento"])

@router.get("/select/tratamiento")
def consultar_tratamiento(data: DataTratamientoId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Tratamiento)
            .where(Tratamiento.codigoTratamiento == data.codigoTratamiento)
        )
        cita = session.execute(request).scalar_one()
        return cita
    except SQLAlchemyError as e:
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
    

@router.get("/select/dynamic/tratamiento")
def consulta_dinamica_tratamiento(data: str):
    session  = db.SessionLocal()
    try:
        request = (
            select(Tratamiento)
            .where(
                or_(
                    Tratamiento.codigoTratamiento.like(f"%{data}%"),
                    Tratamiento.codigoHash.like(f"%{data}%")
                )
            )
        )
        tratamiento = session.execute(request).scalars().all()
        if not tratamiento:
            raise HTTPException (status_code=400)
        return tratamiento
    except SQLAlchemyError as e:
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
    

@router.post("/insert/tratamiento")
def registrar_tratamiento(data: DataTratamientoCreate):
    session  = db.SessionLocal()
    try:
        register = Tratamiento(
            codigoHash = generar_hash(7),
            nombreTratamiento = data.nombreTratamiento,
            descripcionTratamiento = data.descripcionTratamiento,
            fk_numeroIdentificacion = data.fk_numeroIdentificacion,
        )
        session.add(register)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
    

@router.patch("/update/tratamiento")
def actualizar_tratamiento(data: DataTratamientoUpdate, identification: DataTratamientoId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Tratamiento)
            .where(Tratamiento.codigoTratamiento == identification.codigoTratamiento)
        )
        tratamiento = session.execute(request).scalar_one()
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        for columna, dato in changes.items():
            setattr(tratamiento, columna, dato)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
    

# @router.delete("/delete/tratamiento")
# def eliminar_tratamiento():
#     session  = db.SessionLocal()
#     try:
#         pass
#     except:
#         pass
#     finally:
#         session.close()
