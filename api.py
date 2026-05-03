import mariadb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import datos_perfil_db as dp
import comandos_sql as com_sql
from objeto_crud import SistemaCRUD

DB_HOST = dp.HOST
DB_NAME = dp.NAME
DB_USER = dp.USER
DB_PASWD = dp.PASWD

try:
    cc = mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASWD,
        database=DB_NAME,
        port=3306 # puerto de MariaDB
    )
except mariadb.Error as e:
    print(f"Error al conectar a MariaDB: {e}")
    exit(1)

cursor_obj = cc.cursor(dictionary=True)
app = FastAPI(root_path="/api")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

protocolos = {
    "HTTPException":HTTPException,
    "cursor_obj":cursor_obj,
    "mariadb":mariadb,
    "cc":cc,
}

"""
Definición de rutas  
c @app.post("/insert")
r @app.get("/select")
u @app.put("/update")
d @app.delete("/delete")
"""
@app.get("/")  
async def Check(): 
    return {"mensaje": "Hola, este es el backend de HSP"}

@app.get("/selectall/{nombretabla}")
async def consultar_datos_general(nombretabla:str,pagina:int=1):
    sql = com_sql.consulta_paginada(nombretabla,pagina)
    if pagina < 1:
        raise HTTPException(status_code=400, detail="Numero de pagina no valido, debe ser mayor que 0")
    try:
        cursor_obj.execute(sql)
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="No se encontraron datos")
        return rows
    except mariadb.Error:
        raise HTTPException(status_code=500, detail="Tabla no encontrada")

# SISTEMA

# paciente
t_paciente = SistemaCRUD(
    tabla="paciente",
    identificador= {"numeroIdentificacion":[15,"rango"]},
    primerNombre=None,
    segundoNombre=None,
    primerApellido=None,
    segundoApellido=None,
    fechaNacimiento=None,
    peso=None,
    telefono=None,
    correoElectronico=None,
    direccion=None,
    profesion=None,
    antecedentes=None,
    alergias=None,
    fk_codigoMunicipio=None,
    )
@app.get("/select/paciente", tags=["Paciente"])
async def consultar_id_paciente(numeroIdentificacion:str):
    return t_paciente.get(protocolos,numeroIdentificacion)
@app.post("/insert/paciente", tags=["Paciente"])
async def registrar_paciente(numeroIdentificacion:str,primerNombre:str,segundoNombre:str,primerApellido:str,segundoApellido:str,fechaNacimiento:str,peso:str,telefono:str,direccion:str,correoElectronico:str,profesion:str,antecedentes:str,alergias:str,fk_codigoMunicipio:str):
    return t_paciente.post(
        protocolos,
        numeroIdentificacion,
        primerNombre.upper(),
        segundoNombre.upper(),
        primerApellido.upper(),
        segundoApellido.upper(),
        fechaNacimiento,
        peso,
        telefono,
        correoElectronico,
        direccion,
        profesion,
        antecedentes,
        alergias,
        fk_codigoMunicipio,
        )
@app.put("/update/paciente", tags=["Paciente"])
async def actualizar_paciente(numeroIdentificacion:str,primerNombre:str="",segundoNombre:str="",primerApellido:str="",segundoApellido:str="",fechaNacimiento:str="",peso:str="",telefono:str="",direccion:str="",correoElectronico:str="",profesion:str="",antecedentes:str="",alergias:str="",fk_codigoMunicipio:str=""):
    return t_paciente.put(
        protocolos,
        numeroIdentificacion,
        primerNombre = primerNombre.upper(),
        segundoNombre = segundoNombre.upper(),
        primerApellido = primerApellido.upper(),
        segundoApellido = segundoApellido.upper(),
        fechaNacimiento = fechaNacimiento,
        peso = peso,
        telefono = telefono,
        correoElectronico = correoElectronico,
        direccion = direccion,
        profesion = profesion,
        antecedentes = antecedentes,
        alergias = alergias,
        fk_codigoMunicipio = fk_codigoMunicipio,
        )
@app.delete("/delete/paciente", tags=["Paciente"])
async def eliminar_paciente(numeroIdentificacion:str):
    return t_paciente.delete(protocolos,numeroIdentificacion)

# cita
t_cita = SistemaCRUD(
    tabla="cita",
    identificador={"codigoCita":[16,"fijo"]},
    fecha=None,
    hora=None,
    patologia=None,
    tratamientoRecomendado=None,
    precio=None,
    observacion=None,
    fk_codigoEstado=None,
    )
@app.get("/select/cita", tags=["Cita"])
async def consultar_id_cita(codigoCita:str):
    return t_cita.get(protocolos,codigoCita)
@app.post("/insert/cita", tags=["Cita"])
async def registrar_cita(codigoCita:str,fecha:str,hora:str,patologia:str,tratamientoRecomendado:str,precio:int,observacion:str,fk_codigoEstado:str):
    return t_cita.post(
        protocolos,
        codigoCita,
        fecha,
        hora,
        patologia,
        tratamientoRecomendado,
        precio,
        observacion,
        fk_codigoEstado,
        )
@app.put("/update/cita", tags=["Cita"])
async def actualizar_cita(codigoCita:str,fecha:str="",hora:str="",patologia:str="",tratamientoRecomendado:str="",precio:int=0,observacion:str="",fk_codigoEstado:str=""):
    return t_cita.put(
        protocolos,
        codigoCita,
        fecha = fecha,
        hora = hora,
        patologia = patologia,
        tratamientoRecomendado = tratamientoRecomendado,
        precio = precio,
        observacion = observacion,
        fk_codigoEstado = fk_codigoEstado,
        )
@app.delete("/delete/cita", tags=["Cita"])
async def eliminar_cita(codigoCita:str):
    return t_cita.delete(protocolos,codigoCita)

# tratamiento
t_tratamiento = SistemaCRUD(
    tabla="tratamiento",
    identificador={"codigoTratamiento":[16,"fijo"]},
    nombreTratamiento=None,
    fk_numeroIdentificacion=None,
    )
@app.get("/select/tratamiento", tags=["Tratamiento"])
async def consultar_id_tratamiento(codigoTratamiento:str):
    return t_tratamiento.get(protocolos,codigoTratamiento)
@app.post("/insert/tratamiento", tags=["Tratamiento"])
async def registrar_tratamiento(codigoTratamiento:str,nombreTratamiento:str,fk_numeroIdentificacion:str):
    return t_tratamiento.post(
        protocolos,
        codigoTratamiento,
        nombreTratamiento,
        fk_numeroIdentificacion,
        )
@app.put("/update/tratamiento", tags=["Tratamiento"])
async def actualizar_tratamiento(codigoTratamiento:str,nombreTratamiento:str="",fk_numeroIdentificacion:str=""):
    return t_tratamiento.put(
        protocolos,
        codigoTratamiento,
        nombreTratamiento = nombreTratamiento,
        fk_numeroIdentificacion = fk_numeroIdentificacion,
        )
@app.delete("/delete/tratamiento", tags=["Tratamiento"])
async def eliminar_tratamiento(codigoTratamiento:str):
    return t_tratamiento.delete(protocolos, codigoTratamiento)

# municipio
t_municipio = SistemaCRUD(
    tabla="municipio",
    identificador={"codigoMunicipio":[5,"fijo"]},
    nombreMunicipio=None,
    fk_codigoDepartamento=None,
    )
@app.get("/select/municipio", tags=["Municipio"])
async def consultar_id_municipio(codigoMunicipio:str):
    return t_municipio.get(protocolos,codigoMunicipio)
@app.post("/insert/municipio", tags=["Municipio"])
async def registrar_municipio(codigoMunicipio:str,nombreMunicipio:str,fk_codigoDepartamento:str):
    return t_municipio.post(
        protocolos,
        codigoMunicipio,
        nombreMunicipio.upper(),
        fk_codigoDepartamento,
        )
@app.put("/update/municipio", tags=["Municipio"])
async def actualizar_municipio(codigoMunicipio:str,nombreMunicipio:str="",fk_codigoDepartamento:str=""):
    return t_municipio.put(
        protocolos,
        codigoMunicipio,
        nombreMunicipio = nombreMunicipio.upper(),
        fk_codigoDepartamento = fk_codigoDepartamento,
        )
@app.delete("/delete/municipio", tags=["Municipio"])
async def eliminar_municipio(codigoMunicipio:str):
    return t_municipio.delete(protocolos,codigoMunicipio)

# departamento
t_departamento = SistemaCRUD(
    tabla="departamento",
    identificador={"codigoDepartamento":[2,"fijo"]},
    nombreDepartamento=None,
    )
@app.get("/select/departamento", tags=["Departamento"])
async def consultar_id_departamento(codigoDepartamento:str):
    return t_departamento.get(protocolos,codigoDepartamento)
@app.post("/insert/departamento", tags=["Departamento"])
async def registrar_departamento(codigoDepartamento:str,nombreDepartamento:str):
    return t_departamento.post(
        protocolos,
        codigoDepartamento,
        nombreDepartamento.upper(),
        )
@app.put("/update/departamento", tags=["Departamento"])
async def actualizar_departamento(codigoDepartamento:str,nombreDepartamento:str=""):
    return t_departamento.put(
        protocolos,
        codigoDepartamento,
        nombreDepartamento = nombreDepartamento.upper(),
    )
@app.delete("/delete/departamento", tags=["Departamento"])
async def eliminar_departamento(codigoDepartamento:str=""):
    return t_departamento.delete(protocolos,codigoDepartamento)

# estado
t_estado = SistemaCRUD(
    tabla="estado",
    identificador={"codigoEstado":[3,"fijo"]},
    nombreEstado=None,
    )
@app.get("/select/estado", tags=["Estado"])
async def consultar_id_estado(codigoEstado:str):
    return t_estado.get(protocolos,codigoEstado)
@app.post("/insert/estado", tags=["Estado"])
async def registrar_estado(codigoEstado:str,nombreEstado:str):
    return t_estado.post(
        protocolos,
        codigoEstado,
        nombreEstado.title(),
        )
@app.put("/update/estado", tags=["Estado"])
async def actualizar_estado(codigoEstado:str,nombreEstado:str=""):
    return t_estado.put(
        protocolos,
        codigoEstado,
        nombreEstado = nombreEstado.title(),
    )
@app.delete("/delete/estado", tags=["Estado"])
async def eliminar_estado(codigoEstado:str):
    return t_estado.delete(protocolos,codigoEstado)

# imagen
t_imagen = SistemaCRUD(
    tabla="imagen",
    identificador={"refImagen":[32,"rango"]},
    fk_codigoCita=None,
    )
@app.get("/select/imagen", tags=["Imagen"])
async def consultar_id_imagen(refImagen:str):
    return t_imagen.get(protocolos,refImagen)
@app.post("/insert/imagen", tags=["Imagen"])
async def registrar_imagen(refImagen:str,fk_codigoCita:str):
    return t_imagen.post(
        protocolos,
        refImagen,
        fk_codigoCita,
        )
@app.put("/update/imagen", tags=["Imagen"])
async def actualizar_imagen(refImagen:str,fk_codigoCita:str=""):
    return t_imagen.put(
        protocolos,
        refImagen,
        fk_codigoCita = fk_codigoCita,
        )
@app.delete("/delete/imagen", tags=["Imagen"])
async def eliminar_imagen(refImagen:str):
    return t_imagen.delete(protocolos,refImagen)

# SEGURIDAD

# usuario
t_usuario = SistemaCRUD(
    tabla="usuario",
    identificador={"codigoUsuario":[10,"rango"]},
    acceso=None,
    contraseña=None,
    )
@app.get("/select/usuario", tags=["Usuario"])
async def consultar_id_usuario(codigoUsuario:str):
    return t_usuario.get(protocolos,codigoUsuario)
@app.post("/insert/usuario", tags=["Usuario"])
async def registrar_usuario(codigoUsuario:str,acceso:str,contraseña:str):
    return t_usuario.post(
        protocolos,
        codigoUsuario,
        acceso,
        contraseña,
        )
@app.put("/update/usuario", tags=["Usuario"])
async def actualizar_usuario(codigoUsuario:str,acceso:str="",contraseña:str=""):
    return t_usuario.put(
        protocolos,
        codigoUsuario,
        acceso = acceso,
        contraseña = contraseña,
        )
@app.delete("/delete/usuario", tags=["Usuario"])
async def eliminar_usuario(codigoUsuario:str):
    return t_usuario.delete(protocolos,codigoUsuario)

# rol
t_rol = SistemaCRUD(
    tabla="rol",
    identificador={"codigoRol":[3,"fijo"]},
    descripcionRol=None,
    )
@app.get("/select/rol", tags=["Rol"])
async def consultar_id_rol(codigoRol:str):
    return t_rol.get(protocolos,codigoRol)
@app.post("/insert/rol", tags=["Rol"])
async def registrar_rol(codigoRol:str,descripcionRol:str):
    return t_rol.post(
        protocolos,
        codigoRol,
        descripcionRol,
        )
@app.put("/update/rol", tags=["Rol"])
async def actualizar_rol(codigoRol:str,descripcionRol:str=""):
    return t_rol.put(
        protocolos,
        codigoRol,
        descripcionRol = descripcionRol,
        )
@app.delete("/delete/rol", tags=["Rol"])
async def eliminar_rol(codigoRol:str):
    return t_rol.delete(protocolos,codigoRol)

# permiso
t_permiso = SistemaCRUD(
    tabla="permiso",
    identificador={"codigoPermiso":[3,"fijo"]},
    descripcionPermiso=None,
    estadoPermiso=None,
    )
@app.get("/select/permiso", tags=["Permiso"])
async def consultar_id_permiso(codigoPermiso:str):
    return t_permiso.get(protocolos,codigoPermiso)
@app.post("/insert/permiso", tags=["Permiso"])
async def registrar_permiso(codigoPermiso:str,descripcionPermiso:str,estadoPermiso:str):
    return t_permiso.post(
        protocolos,
        codigoPermiso,
        descripcionPermiso,
        estadoPermiso,
        )
@app.put("/update/permiso", tags=["Permiso"])
async def actualizar_permiso(codigoPermiso:str,descripcionPermiso:str="",estadoPermiso:str=""):
    return t_permiso.put(
        protocolos,
        codigoPermiso,
        descripcionPermiso = descripcionPermiso,
        estadoPermiso = estadoPermiso,
        )
@app.delete("/delete/permiso", tags=["Permiso"])
async def eliminar_permiso(codigoPermiso:str):
    return t_permiso.delete(protocolos,codigoPermiso)