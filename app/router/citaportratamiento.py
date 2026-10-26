from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from ..core.database import Database
from ..model.models import CitaPorTratamiento, Cita, Tratamiento
from ..model.schemas import DataCitaPorTratamientoCreate, DataCitaPorTratamientoHashCreate, DataCitaPorTratamientoUpdate, DataCitaPorTratamientoHashUpdate, DataCitaPorTratamientoId

db = Database()

router = APIRouter(tags=["CitaPorTratamiento"])

@router.get("/select/citaportratamiento")
def consultar_citaportratamiento(data: DataCitaPorTratamientoId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(CitaPorTratamiento)
            .where(CitaPorTratamiento.codigoCitaPorTratamiento == data.codigoCitaPorTratamiento)
        )
        citaportratamiento = session.execute(request).scalar_one()
        return citaportratamiento
    except SQLAlchemyError as e:
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
    

"""@router.get("/select/like/citaportratamiento")
def consultar_like_citaportratamiento():
    session  = db.SessionLocal()
    try:
        pass
    except SQLAlchemyError as e:
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
    
"""
@router.post("/insert/citaportratamiento")
def registrar_citaportratamiento(data: DataCitaPorTratamientoCreate):
    session  = db.SessionLocal()
    try:
        register = CitaPorTratamiento(
            fk_codigoTratamiento = data.fk_codigoTratamiento,
            fk_codigoCita = data.fk_codigoCita,
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
@router.post("/insert/hash/citaportratamiento")
def registrar_por_hash_citaportratamiento(data: DataCitaPorTratamientoHashCreate):
    session  = db.SessionLocal()
    try:
        request_cita = (
            select(Cita)
            .where(Cita.codigoHash == data.codigoHashCita)
        )
        request_tratamiento = (
            select(Tratamiento)
            .where(Tratamiento.codigoHash == data.codigoHashTratamiento)
        )
        cita = session.execute(request_cita).scalar_one()
        tratamiento = session.execute(request_tratamiento).scalar_one()
        
        register = CitaPorTratamiento(
            fk_codigoTratamiento = tratamiento.codigoTratamiento,
            fk_codigoCita = cita.codigoCita,
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


@router.patch("/update/citaportratamiento")
def actualizar_citaportratamiento(data: DataCitaPorTratamientoUpdate, identification: DataCitaPorTratamientoId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(CitaPorTratamiento)
            .where(CitaPorTratamiento.codigoCitaPorTratamiento == identification.codigoCitaPorTratamiento)
        )
        citaportratamiento = session.execute(request). scalar_one()
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        for columna, dato in changes.items():
            setattr(citaportratamiento, columna, dato)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()


# @router.delete("/delete/citaportratamiento")
# def eliminar_citaportratamiento():
#     session  = db.SessionLocal()
#     try:
#         pass
#     except SQLAlchemyError as e:
#         session.rollback()
#         raise HTTPException (
#             status_code= 500,
#             detail= f"Error: {e}"
#         )
#     finally:
#         session.close()
