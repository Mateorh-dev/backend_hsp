from tipo_dato_sql import *
from diccionario_a_sql import DiccionarioSQL

tablas = {
    "paciente":{
        "numeroIdentificacion": [Varchar(15), "PK"],
        "primerNombre":[Varchar(25), "NN"],
        "segundoNombre":[Varchar(25)],
        "primerApellido":[Varchar(25), "NN"],
        "segundoApellido":[Varchar(25)],
        "fechaNacimiento":[Date(), "NN"],
        "telefono":[Varchar(15), "NN"],
        "correoElectronico":[Varchar(128)],
        "direccion":[Text()],
        "profesion":[Text()],
        "estadoActivo":[Bool(),"NN"],
    },
    "tratamiento":{
        "codigoTratamiento":[Int(), "PK", "AUTO"],
        "codigoHash":[Char(7), "NN"],
        "nombreTratamiento":[Text(), "NN"],
        "descripcionTratamiento":[Text()],
        "paciente.numeroIdentificacion":["FK"],
    },
    "citaportratamiento":{
        "codigoCitaPorTratamiento":[Int(), "PK", "AUTO"],
        "tratamiento.codigoTratamiento":["FK"],
        "cita.codigoCita":["FK"],
    },
    "cita":{
        "codigoCita":[Int(), "PK", "AUTO"],
        "codigoHash":[Char(5), "NN"],
        "fecha":[Date(), "NN"],
        "hora":[Time(), "NN"],
        "precio":[Int()],
        "observacion":[Text()],
        "estadocita.codigoEstado":["FK"],
    },
    "estadocita":{
        "codigoEstado":[Char(3), "PK"],
        "nombreEstado":[Varchar(32), "NN"],
    },
    "imagen":{
        "codigoImagen":[Int(), "PK", "AUTO"],
        "refImagen":[Varchar(32), "NN"],
        "cita.codigoCita":["FK"],
    },
}

with open("tablas_sistema.sql", "w", encoding='utf-8') as comandos:
    comandos.write(DiccionarioSQL(tablas))