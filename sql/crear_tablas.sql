-- CREAR BASE DE DATOS
CREATE DATABASE HSP_DB;
USE HSP_DB

-- CREAR TABLAS
CREATE TABLE paciente (
    numeroIdentificacion VARCHAR(15) PRIMARY KEY,
    primerNombre VARCHAR(25) NOT NULL,
    segundoNombre VARCHAR(25),
    primerApellido VARCHAR(25) NOT NULL,
    segundoApellido VARCHAR(25),
    fechaNacimiento DATE,
    peso VARCHAR(10),
    telefono VARCHAR(15) NOT NULL,
    direccion TEXT,
    correoElectronico VARCHAR(128),
    Profesion TEXT,
    antecedentes TEXT,
    alergias TEXT,
    fk_codigoMunicipio CHAR(5) NOT NULL
);
CREATE TABLE cita (
    codigoCita CHAR(16) PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    patologias TEXT,
    tratamientoRecomendado TEXT,
    precio INT,
    observacion TEXT,
    fk_codigoEstado CHAR(3) NOT NULL
);
CREATE TABLE tratamiento (
    codigoTratamiento CHAR(16) PRIMARY KEY,
    nombreTratamiento TEXT NOT NULL,
    fk_numeroIdentificacion VARCHAR(15) NOT NULL
);
CREATE TABLE municipio (
    codigoMunicipio CHAR(5) PRIMARY KEY,
    nombreMunicipio VARCHAR(25) NOT NULL,
    fk_codigoDepartamento CHAR(2) NOT NULL
);
CREATE TABLE departamento (
    codigoDepartamento CHAR(2) PRIMARY KEY,
    nombreDepartamento VARCHAR(25) NOT NULL
);
CREATE TABLE estado (
    codigoEstado CHAR(3) PRIMARY KEY,
    nombreEstado VARCHAR(32) NOT NULL
);
CREATE TABLE imagen (
    refImagen VARCHAR(32) PRIMARY KEY,
    fk_codigoCita CHAR(16) NOT NULL
);
CREATE TABLE citaportratamiento (
    fk_codigoTratamiento CHAR(16) NOT NULL,
    fk_codigoCita CHAR(16) NOT NULL,
    FOREIGN KEY (fk_codigoTratamiento) REFERENCES Tratamiento(codigoTratamiento),
    FOREIGN KEY (fk_codigoCita) REFERENCES cita(codigoCita)
);
ALTER TABLE paciente
add CONSTRAINT fk_codigoMunicipio
FOREIGN KEY (fk_codigoMunicipio) REFERENCES municipio(codigoMunicipio);

ALTER TABLE cita
add CONSTRAINT fk_codigoEstado
FOREIGN KEY (fk_codigoEstado) REFERENCES estado(codigoEstado);

ALTER TABLE tratamiento
add CONSTRAINT fk_numeroIdentificacion
FOREIGN KEY (fk_numeroIdentificacion) REFERENCES paciente(numeroIdentificacion);

ALTER TABLE municipio
add CONSTRAINT fk_codigoDepartamento
FOREIGN KEY (fk_codigoDepartamento) REFERENCES departamento(codigoDepartamento);

ALTER TABLE imagen
add CONSTRAINT fk_codigoCita
FOREIGN KEY (fk_codigoCita) REFERENCES cita(codigoCita);