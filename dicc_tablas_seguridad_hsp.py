from tipo_dato_sql import *
from diccionario_a_sql import DiccionarioSQL

tablas = {
    "usuario":{
        "codigoUsuario":[Int(),"PK","AUTO"],
        "acceso":[Varchar(250), "NN"],
        "contraseña":[Varchar(250), "NN"],
    },
    "rolporusuario":{
        "usuario.codigoUsuario":["FK"],
        "rol.codigoRol":["FK"],
    },
    "rol":{
        "codigoRol":[Char(3), "PK"],
        "descripcionRol":[Text()],
    },
    "permisoporrol":{
        "rol.codigoRol":["FK"],
        "permiso.codigoPermiso":["FK"],
    },
    "permiso":{
        "codigoPermiso":[Char(3),"PK"],
        "descripcionPermiso":[Text()],
        "estadoPermiso":[Bool(), "NN"],
    },
}

with open("tablas_seguridad.sql", "w", encoding='utf-8') as comandos:
    comandos.write(DiccionarioSQL(tablas))