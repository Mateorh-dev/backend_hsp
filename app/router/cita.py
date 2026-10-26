from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from ..core.database import Database
from ..model.models import Cita, CitaPorTratamiento, Tratamiento
from ..model.schemas import DataCitaCreate, DataCitaUpdate, DataCitaId, DataTratamientoId
from ..model.hash import generar_hash

db = Database()

router = APIRouter(tags=["Cita"])

@router.get("/select/cita")
def consultar_cita(data: DataCitaId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Cita)
            .where(Cita.codigoCita == data.codigoCita)
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

@router.get("/select/dynamic/cita")
def consulta_dinamica_cita(data: str):
    session  = db.SessionLocal()
    try:
        request = (
            select(Cita)
            .where(
                or_(
                    Cita.codigoCita.like(f"%{data}%"),
                    Cita.codigoHash.like(f"%{data}%"),
                )
            )
        )
        cita = session.execute(request).scalars().all()
        if not cita:
            raise HTTPException (status_code=400)
        return cita
    except SQLAlchemyError as e:
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()

@router.get("/select/by_tratamiento/cita")
def consulta_by_tratamiento_cita(data: DataTratamientoId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Cita)
            .join(CitaPorTratamiento, Cita.codigoCita == CitaPorTratamiento.fk_codigoCita)
            .join(Tratamiento, CitaPorTratamiento.fk_codigoTratamiento == Tratamiento.codigoTratamiento)
            .where(Tratamiento.codigoTratamiento == data.codigoTratamiento)
            .order_by(Cita.codigoCita.desc())
        )
        citas = session.execute(request).scalars().all()
        if not citas:
            raise HTTPException (status_code=400)
        return citas
    except SQLAlchemyError as e:
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()

@router.get("/select/by_tratamiento/hash/cita")
def consulta_by_tratamiento_hash_cita(data: str):
    session  = db.SessionLocal()
    try:
        request_tratamiento = (
            select(Tratamiento)
            .where(Tratamiento.codigoHash == data)
        )
        tratamiento = session.execute(request_tratamiento).scalar_one_or_none()
        request = (
            select(Cita)
            .join(CitaPorTratamiento, Cita.codigoCita == CitaPorTratamiento.fk_codigoCita)
            .join(Tratamiento, CitaPorTratamiento.fk_codigoTratamiento == Tratamiento.codigoTratamiento)
            .where(Tratamiento.codigoTratamiento == tratamiento.codigoTratamiento)
            .order_by(Cita.codigoCita.desc())
        )
        citas = session.execute(request).scalars().all()
        if not citas:
            raise HTTPException (status_code=400)
        return citas
    except SQLAlchemyError as e:
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()


@router.post("/insert/cita")
def registrar_cita(data: DataCitaCreate):
    session  = db.SessionLocal()
    try:
        register = Cita(
            codigoHash = generar_hash(),
            fecha = data.fecha,
            hora = data.hora,
            precio = data.precio,
            observacion = data.observacion,
            fk_codigoEstado = data.fk_codigoEstado,
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
    

@router.patch("/update/cita")
def actualizar_cita(data: DataCitaUpdate, identification: DataCitaId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Cita)
            .where(Cita.codigoCita == identification.codigoCita)
        )
        cita = session.execute(request).scalar_one()
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        for columna, dato in changes.items():
            setattr(cita, columna, dato)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()


# @router.delete("/delete/cita")
# def eliminar_cita():
#     session  = db.SessionLocal()
#     try:
#         pass
#     except SQLAlchemyError as e:
#         raise HTTPException (
#             status_code= 500,
#             detail= f"Error: {e}"
#         )
#     finally:
#         session.close()
