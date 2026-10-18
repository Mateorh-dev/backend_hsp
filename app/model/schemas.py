# modelo de datos ingresados con pydantic
from datetime import date, time
from typing import Optional
from pydantic import BaseModel

# Paciente
class DataPacienteCreate(BaseModel):
    numeroIdentificacion: str
    primerNombre: str
    segundoNombre: Optional[str] = None
    primerApellido: str
    segundoApellido: Optional[str] = None
    fechaNacimiento: date
    telefono: str
    correoElectronico: Optional[str] = None
    direccion: Optional[str] = None
    profesion: Optional[str] = None

class DataPacienteUpdate(BaseModel):
    primerNombre: Optional[str] = None
    segundoNombre: Optional[str] = None
    primerApellido: Optional[str] = None
    segundoApellido: Optional[str] = None
    fechaNacimiento: Optional[date] = None
    telefono: Optional[str] = None
    correoElectronico: Optional[str] = None
    direccion: Optional[str] = None
    profesion: Optional[str] = None

class DataPacienteId(BaseModel):
    numeroIdentificacion: str


# Tratamiento
class DataTratamientoCreate(BaseModel):
    nombreTratamiento: str
    descripcionTratamiento: Optional[str] = None
    fk_numeroIdentificacion: str

class DataTratamientoUpdate(BaseModel):
    nombreTratamiento: Optional[str] = None
    descripcionTratamiento: Optional[str] = None
    fk_numeroIdentificacion: Optional[str] = None

class DataTratamientoId(BaseModel):
    codigoTratamiento: int


# CitaPorTratamiento
class DataCitaPorTratamientoCreate(BaseModel):
    fk_codigoTratamiento: int
    fk_codigoCita: int

class DataCitaPorTratamientoHashCreate(BaseModel):
    codigoHashTratamiento: str
    codigoHashCita: str

class DataCitaPorTratamientoUpdate(BaseModel):
    fk_codigoTratamiento: Optional[int] = None
    fk_codigoCita: Optional[int] = None

class DataCitaPorTratamientoHashUpdate(BaseModel):
    codigoHashTratamiento: Optional[str] = None
    codigoHashCita: Optional[str] = None

class DataCitaPorTratamientoId(BaseModel):
    codigoCitaPorTratamiento: int


# Cita
class DataCitaCreate(BaseModel):
    fecha: date
    hora: time
    precio: Optional[int] = None
    observacion: Optional[str] = None
    fk_codigoEstado: str

class DataCitaUpdate(BaseModel):
    fecha: Optional[date] = None
    hora: Optional[time] = None
    precio: Optional[int] = None
    observacion: Optional[str] = None
    fk_codigoEstado: Optional[str] = None

class DataCitaId(BaseModel):
    codigoCita: int


# EstadoCita
class DataEstadoCitaCreate(BaseModel):
    codigoEstado: str
    nombreEstado: str

class DataEstadoCitaUpdate(BaseModel):
    nombreEstado: Optional[str] = None

class DataEstadoCitaId(BaseModel):
    codigoEstado: str


# Imagen
class DataImagenCreate(BaseModel):
    codigoImagen: int
    refImagen: str
    fk_codigoCita: int

class DataImagenUpdate(BaseModel):
    refImagen: Optional[str] = None
    fk_codigoCita: Optional[int] = None

class DataImagenId(BaseModel):
    codigoImagen: int
