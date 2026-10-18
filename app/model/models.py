# modelado de las tablas con sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String,CHAR, Date, ForeignKey, Integer, Text, Time, Boolean
from datetime import date, time
from typing import Optional

class Base(DeclarativeBase):
    pass

class Paciente(Base):
    __tablename__ = "paciente"

    numeroIdentificacion: Mapped[str] = mapped_column(String(15), primary_key=True)
    primerNombre: Mapped[str] = mapped_column(String(25), nullable=False)
    segundoNombre: Mapped[Optional[str]] = mapped_column(String(25))
    primerApellido: Mapped[str] = mapped_column(String(25), nullable=False)
    segundoApellido: Mapped[Optional[str]] = mapped_column(String(25))
    fechaNacimiento: Mapped[date] = mapped_column(Date)
    telefono: Mapped[str] = mapped_column(String(15), nullable=False)
    correoElectronico: Mapped[Optional[str]] = mapped_column(String(128))
    direccion: Mapped[Optional[str]] = mapped_column(Text)
    profesion: Mapped[Optional[str]] = mapped_column(Text)
    estadoActivo: Mapped[bool] = mapped_column(Boolean)

class Tratamiento(Base):
    __tablename__ = "tratamiento"

    codigoTratamiento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigoHash: Mapped[str] = mapped_column(CHAR(7), nullable=False)
    nombreTratamiento: Mapped[str] = mapped_column(Text, nullable=False)
    descripcionTratamiento: Mapped[Optional[str]] = mapped_column(Text)
    fk_numeroIdentificacion: Mapped[str] = mapped_column(String(15), ForeignKey("paciente.numeroIdentificacion"))

class CitaPorTratamiento(Base):
    __tablename__ = "citaportratamiento"

    codigoCitaPorTratamiento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fk_codigoTratamiento: Mapped[int] = mapped_column(Integer, ForeignKey("tratamiento.codigoTratamiento"))
    fk_codigoCita: Mapped[int] = mapped_column(Integer, ForeignKey("cita.codigoCita"))

class Cita(Base):
    __tablename__ = "cita"

    codigoCita: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigoHash: Mapped[str] = mapped_column(CHAR(5), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    hora: Mapped[time] = mapped_column(Time, nullable=False)
    precio: Mapped[Optional[int]] = mapped_column(Integer)
    observacion: Mapped[Optional[str]] = mapped_column(Text)
    fk_codigoEstado: Mapped[str] = mapped_column(CHAR(3), ForeignKey("estadocita.codigoEstado"))

class EstadoCita(Base):
    __tablename__ = "estadocita"

    codigoEstado: Mapped[str] = mapped_column(CHAR(3), primary_key=True)
    nombreEstado: Mapped[str] = mapped_column(String(32), nullable=False)

class Imagen(Base):
    __tablename__ = "imagen"

    codigoImagen: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    refImagen: Mapped[str] = mapped_column(String(32), nullable=False)
    fk_codigoCita: Mapped[int] = mapped_column(Integer, ForeignKey("cita.codigoCita"))