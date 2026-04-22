from tipo_dato_sql import *
from diccionario_a_sql import DiccionarioSQL

tablas = {
    "paciente":{
        "cedula":[Varchar(15), "PK"],
        "nombre":[Varchar(25)],
        "apellido":[Varchar(25), "NN"],
        "fecha_nacimiento":[Date()],
        "peso":[Decimal(5)],
        "telefono":[Varchar(15), "NN"],
        "municipio.codigoMunicipio":["FK"],
    },
    "municipio":{
        "codigoMunicipio":[Char(5), "PK"],
        "nombreMunicipio":[Varchar(25), "NN"],
        "departamento.codigoDepartamento":["FK"],
    },
    "departamento":{
        "codigoDepartamento":[Char(5), "PK"],
        "nombreDepartamento":[Varchar(25), "NN"],
        "paciente.cedula":["FK"],
    }
}

with open("tablas.sql", "w") as comandos:
    comandos.write(DiccionarioSQL(tablas))