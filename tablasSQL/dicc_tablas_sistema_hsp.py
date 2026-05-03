from tipo_dato_sql import *
from diccionario_a_sql import DiccionarioSQL

tablas = {
    "departamento":{
        "codigoDepartamento":[Char(2), "PK"],
        "nombreDepartamento":[Varchar(25), "NN"],
    },
    "municipio":{
        "codigoMunicipio":[Char(5), "PK"],
        "nombreMunicipio":[Varchar(25), "NN"],
        "departamento.codigoDepartamento":["FK"],
    },
    "paciente":{
        "numeroIdentificacion": [Varchar(15), "PK"],
        "primerNombre":[Varchar(25),"NN"],
        "segundoNombre":[Varchar(25)],
        "primerApellido":[Varchar(25),"NN"],
        "segundoApellido":[Varchar(25)],
        "fechaNacimiento":[Date()],
        "peso":[Varchar(10)],
        "telefono":[Varchar(15), "NN"],
        "correoElectronico":[Varchar(128)],
        "direccion":[Text()],
        "profesion":[Text()],
        "antecedentes":[Text()],
        "alergias":[Text()],
        "municipio.codigoMunicipio":["FK"],
    },
    "tratamiento":{
        "codigoTratamiento":[Char(16), "PK"],
        "nombreTratamiento":[Text(), "NN"],
        "paciente.numeroIdentificacion":["FK"],
    },
    "citaportratamiento":{
        "tratamiento.codigoTratamiento":["FK"],
        "cita.codigoCita":["FK"],
    },
    "cita":{
        "codigoCita":[Char(16),"PK"],
        "fecha":[Date(), "NN"],
        "hora":[Time(), "NN"],
        "patologia":[Text()],
        "tratamientoRecomendado":[Text()],
        "precio":[Int()],
        "observacion":[Text()],
        "estado.codigoEstado":["FK"],
    },
    "estado":{
        "codigoEstado":[Char(3), "PK"],
        "nombreEstado":[Varchar(32), "NN"],
    },
    "imagen":{
        "refImagen":[Varchar(32), "PK"],
        "cita.codigoCita":["FK"],
    },
}

with open("tablas_sistema.sql", "w", encoding='utf-8') as comandos:
    comandos.write(DiccionarioSQL(tablas))