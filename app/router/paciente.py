from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from ..core.database import Database
from ..model.models import Paciente
from ..model.schemas import DataPacienteCreate, DataPacienteUpdate, DataPacienteId

db = Database()

router = APIRouter(tags=["Paciente"])

@router.get("/check/paciente")
def check_paciente(data: DataPacienteId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Paciente)
            .where(
                Paciente.numeroIdentificacion == data.numeroIdentificacion,
                Paciente.estadoActivo == True
            )
        )
        paciente = session.execute(request).scalar_one_or_none()
        if paciente is None:
            raise HTTPException (status_code=400)
        else:
            raise HTTPException (status_code=200)

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()

@router.get("/select/paciente")
def consultar_paciente(data: DataPacienteId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Paciente)
            .where(Paciente.numeroIdentificacion == data.numeroIdentificacion)
        )
        paciente = session.execute(request).scalar_one_or_none()
        if paciente is None:
            raise HTTPException (status_code=400)
        return paciente

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()

@router.get("/select/dynamic/paciente")
def consulta_dinamica_paciente(data: str):
    session  = db.SessionLocal()
    try:
        request = (
            select(Paciente)
            .where(
                or_(
                    Paciente.numeroIdentificacion.like(f"%{data}%"),
                    Paciente.primerNombre.ilike(f"%{data}%"),
                    Paciente.segundoNombre.ilike(f"%{data}%"),
                    Paciente.primerApellido.ilike(f"%{data}%"),
                    Paciente.segundoApellido.ilike(f"%{data}%")
                ),
                Paciente.estadoActivo == True
            )
            .order_by(Paciente.primerNombre)
            .limit(15)
        )
        paciente = session.execute(request).scalars().all()
        if not paciente:
            raise HTTPException (status_code=400)
        return paciente

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
        
# @router.get("/select/like/paciente")
# def consultar_like_paciente():
#     session  = db.SessionLocal()
#     try:
#         pass
#     except:
#         pass
#     finally:
#         session.close()


@router.post("/insert/paciente")
def registrar_paciente(data: DataPacienteCreate):
    session  = db.SessionLocal()
    try:
        request = (
            select(Paciente)
            .where(Paciente.numeroIdentificacion == data.numeroIdentificacion)
        )
        exist = session.execute(request).scalar_one_or_none()

        if exist:
            if exist.estadoActivo:
                raise HTTPException (
                    status_code= 400,
                    detail= f"Registro Duplicado, {data.numeroIdentificacion} ya existe"
                )
            if not exist.estadoActivo:
                exist.primerNombre = data.primerNombre
                exist.segundoNombre = data.segundoNombre
                exist.primerApellido = data.primerApellido
                exist.segundoApellido = data.segundoApellido
                exist.fechaNacimiento = data.fechaNacimiento
                exist.telefono = data.telefono
                exist.correoElectronico = data.correoElectronico
                exist.direccion = data.direccion
                exist.profesion = data.profesion
                exist.estadoActivo = True
                
                session.commit()
        else:
            register = Paciente(
                numeroIdentificacion = data.numeroIdentificacion,
                primerNombre = data.primerNombre,
                segundoNombre = data.segundoNombre,
                primerApellido = data.primerApellido,
                segundoApellido = data.segundoApellido,
                fechaNacimiento = data.fechaNacimiento,
                telefono = data.telefono,
                correoElectronico = data.correoElectronico,
                direccion = data.direccion,
                profesion = data.profesion,
                estadoActivo = True,
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
 

@router.patch("/update/paciente")
def actualizar_paciente(data: DataPacienteUpdate, identification: DataPacienteId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Paciente)
            .where(
                Paciente.numeroIdentificacion == identification.numeroIdentificacion,
                Paciente.estadoActivo == True
            )
        )
        paciente = session.execute(request).scalar_one_or_none()
        if paciente is None:
            raise HTTPException (
                status_code= 400,
                detail= f"{identification.numeroIdentificacion} no existe"
            )
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        for columna, dato in changes.items():
            setattr(paciente, columna, dato)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
    

@router.delete("/delete/paciente")
def eliminar_paciente(data: DataPacienteId = Depends()):
    session  = db.SessionLocal()
    try:
        request = (
            select(Paciente)
            .where(Paciente.numeroIdentificacion == data.numeroIdentificacion)
        )
        paciente = session.execute(request).scalar_one_or_none()
        if paciente is None:
            raise HTTPException (
                status_code= 400,
                detail= f"{data.numeroIdentificacion} no existe"
            )
        paciente.estadoActivo = False
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException (
            status_code= 500,
            detail= f"Error: {e}"
        )
    finally:
        session.close()
