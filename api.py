import mariadb
from fastapi import FastAPI, HTTPException
import datos_pefil_db as dp
import comandos_sql as com_sql

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
app = FastAPI()

#Definición de rutas  
# @app.get("/")  
# async def root(): 
#     return {"mensaje": "Hola desde FastAPI con MariaDB"}

# c @app.post("/insert")
# r @app.get("/select")
# u @app.put("/update")
# d @app.delete("/delete")

@app.get("/selectall/{nametable}")
async def consultar_datos_general(nametable:str,page:int=1):
    sql = com_sql.consulta_paginada(nametable,page)
    if page < 1:
        raise HTTPException(status_code=400, detail="Numero de pagina no valido, debe ser mayor que 0")
    try:
        cursor_obj.execute(sql)
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="No se encontraron datos")
        return rows
    except mariadb.Error:
        raise HTTPException(status_code=500, detail="Tabla no encontrado")

# paciente
@app.get("/select/paciente")
async def consultar_id_paciente(numeroIdentificacion:str):
    ni = numeroIdentificacion
    sql = com_sql.consulta_por_identificador("paciente","numeroIdentificacion")
        # SELECT * FROM paciente WHERE numeroIdentificacion='?';
    if len(ni) < 1 or len(ni) > 15:
        raise HTTPException(status_code=400, detail="Numero de identificacion no valido, debe estar entre el rango de 1 a 15 caracteres")
    try:
        cursor_obj.execute(sql,(ni,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Numero de identificacion no encontrado")
        return rows
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
@app.post("/insert/paciente")
async def registrar_paciente(numeroIdentificacion:str,primerNombre:str,segundoNombre:str,primerApellido:str,segundoApellido:str,fechaNacimiento:str,peso:str,telefono:str,direccion:str,correoElectronico:str,Profesion:str,antecedentes:str,alergias:str,fk_codigoMunicipio:str):
    sql = """
INSERT INTO paciente (numeroIdentificacion,primerNombre,segundoNombre,primerApellido,segundoApellido,fechaNacimiento,peso,telefono,direccion,correoElectronico,Profesion,antecedentes,alergias,fk_codigoMunicipio)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
"""
    try:
        cursor_obj.execute(sql,(numeroIdentificacion,primerNombre.upper(),segundoNombre.upper(),primerApellido.upper(),segundoApellido.upper(),fechaNacimiento,peso,telefono,direccion,correoElectronico,Profesion,antecedentes,alergias,fk_codigoMunicipio))
        cc.commit()
        return {"mensaje":f"Se registro el paciente {numeroIdentificacion},{primerNombre},{primerApellido},{telefono},{correoElectronico} correctamente"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
# u @app.put("/update")
@app.delete("/delete/paciente")
async def eliminar_paciente(numeroIdentificacion:str):
    ni = numeroIdentificacion
    sql_consultar = com_sql.consulta_por_identificador("paciente","numeroIdentificacion")
    sql_eliminar = com_sql.eliminar_por_identificador("paciente","numeroIdentificacion")
    if len(ni) < 1 or len(ni) > 15:
        raise HTTPException(status_code=400, detail="Numero de identificacion no valido, debe estar entre el rango de 1 a 15 caracteres")
    try:
        cursor_obj.execute(sql_consultar,(ni,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Numero de identificacion no encontrado")
        cursor_obj.execute(sql_eliminar,(ni,))
        cc.commit()
        return{"mensaje" : f"Se elimino el paciente identificado {rows[0]["numeroIdentificacion"]}, {rows[0]["primerNombre"]} {rows[0]["primerApellido"]}"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

# cita
@app.get("/select/cita")
async def consultar_id_cita(codigoCita:str):
    ct = codigoCita
    sql = com_sql.consulta_por_identificador("cita","codigoCita")
        # SELECT * FROM cita WHERE codigoCita='?';
    if len(ct) != 16:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 16 caracteres")
    try:
        cursor_obj.execute(sql,(ct,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        return rows
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
@app.post("/insert/cita")
async def registrar_cita(codigoCita:str,fecha:str,hora:str,patologias:str,tratamientoRecomendado:str,precio:int,observacion:str,fk_codigoEstado:str):
    sql = """
INSERT INTO cita (codigoCita,fecha,hora,patologias,tratamientoRecomendado,precio,observacion,fk_codigoEstado)
VALUES (?,?,?,?,?,?,?,?);
"""
    try:
        cursor_obj.execute(sql,(codigoCita,fecha,hora,patologias,tratamientoRecomendado,precio,observacion,fk_codigoEstado))
        cc.commit()
        return {"mensaje":f"Se registro el cita {codigoCita},{fecha},{hora},{patologias},{tratamientoRecomendado},{precio},{observacion},{fk_codigoEstado} correctamente"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
# u @app.put("/update")
@app.delete("/delete/cita")
async def eliminar_cita(codigoCita:str):
    ct = codigoCita
    sql_consultar = com_sql.consulta_por_identificador("cita","codigoCita")
    sql_eliminar = com_sql.eliminar_por_identificador("cita","codigoCita")
    if len(ct) != 16:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 16 caracteres")
    try:
        cursor_obj.execute(sql_consultar,(ct,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        cursor_obj.execute(sql_eliminar,(ct,))
        cc.commit()
        return{"mensaje" : f"Se elimino la cita identificada {rows[0]["codigoCita"]}"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

# tratamiento
@app.get("/select/tratamiento")
async def consultar_id_tratamiento(codigoTratamiento:str):
    ct = codigoTratamiento
    sql = com_sql.consulta_por_identificador("tratamiento","codigoTratamiento")
        # SELECT * FROM tratamiento WHERE codigoTratamiento='?';
    if len(ct) != 16:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 16 caracteres")
    try:
        cursor_obj.execute(sql,(ct,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        return rows
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
@app.post("/insert/tratamiento")
async def registrar_tratamiento(codigoTratamiento:str,nombreTratamiento:str,fk_numeroIdentificacion:str):
    sql = """
INSERT INTO tratamiento (codigoTratamiento,nombreTratamiento,fk_numeroIdentificacion)
VALUES (?,?,?);
"""
    try:
        cursor_obj.execute(sql,(codigoTratamiento,nombreTratamiento,fk_numeroIdentificacion))
        cc.commit()
        return {"mensaje":f"Se registro el tratamiento {codigoTratamiento},{nombreTratamiento},{fk_numeroIdentificacion} correctamente"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
# u @app.put("/update")
@app.delete("/delete/tratamiento")
async def eliminar_tratamiento(codigoTratamiento:str):
    ct = codigoTratamiento
    sql_consultar = com_sql.consulta_por_identificador("tratamiento","codigoTratamiento")
    sql_eliminar = com_sql.eliminar_por_identificador("tratamiento","codigoTratamiento")
    if len(ct) != 16:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 16 caracteres")
    try:
        cursor_obj.execute(sql_consultar,(ct,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        cursor_obj.execute(sql_eliminar,(ct,))
        cc.commit()
        return{"mensaje" : f"Se elimino el tratamiento identificado {rows[0]["codigoTratamiento"]}, {rows[0]["nombreTratamiento"]} "}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

# municipio
@app.get("/select/municipio")
async def consultar_id_municipio(codigoMunicipio:str):
    cm = codigoMunicipio
    sql = com_sql.consulta_por_identificador("municipio","codigoMunicipio")
        # SELECT * FROM municipio WHERE codigoMunicipio='{cm}';
    if len(cm) != 5:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 5 caracteres")
    try:
        cursor_obj.execute(sql,(cm,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        return rows
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
@app.post("/insert/municipio")
async def registrar_municipio(codigoMunicipio:str,nombreMunicipio:str,fk_codigoDepartamento:str):
    sql = """
INSERT INTO municipio (codigoMunicipio,nombreMunicipio,fk_codigoDepartamento)
VALUES (?,?,?);
"""
    try:
        cursor_obj.execute(sql,(codigoMunicipio,nombreMunicipio,fk_codigoDepartamento))
        cc.commit()
        return {"mensaje":f"Se registro el municipio {codigoMunicipio},{nombreMunicipio},{fk_codigoDepartamento} correctamente"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
# u @app.put("/update")
@app.delete("/delete/municipio")
async def eliminar_municipio(codigoMunicipio:str):
    cm = codigoMunicipio
    sql_consultar = com_sql.consulta_por_identificador("municipio","codigoMunicipio")
    sql_eliminar = com_sql.eliminar_por_identificador("municipio","codigoMunicipio")
    if len(cm) != 5:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 5 caracteres")
    try:
        cursor_obj.execute(sql_consultar,(cm,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        cursor_obj.execute(sql_eliminar,(cm,))
        cc.commit()
        return{"mensaje" : f"Se elimino el municipio identificado {rows[0]["codigoMunicipio"]}, {rows[0]["nombreMunicipio"]} "}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

# departamento
@app.get("/select/departamento")
async def consultar_id_departamento(codigoDepartamento:str):
    cd = codigoDepartamento
    sql = com_sql.consulta_por_identificador("departamento","codigoDepartamento")
        # SELECT * FROM departamento WHERE codigoDepartamento='?';
    if len(cd) != 2:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 2 caracteres")
    try:
        cursor_obj.execute(sql,(cd,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        return rows
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
@app.post("/insert/departamento")
async def registrar_departamento(codigoDepartamento:str,nombreDepartamento:str):
    sql = """
INSERT INTO departamento (codigoDepartamento,nombreDepartamento)
VALUES (?,?)
"""
    try:
        cursor_obj.execute(sql,(codigoDepartamento,nombreDepartamento.upper()))
        cc.commit()
        return {"mensaje" : f"Se registro el departamento {codigoDepartamento}, {nombreDepartamento} correctamnte"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
# u @app.put("/update")
@app.delete("/delete/departamento")
async def eliminar_departamento(codigoDepartamento:str):
    cd = codigoDepartamento
    sql_consultar = com_sql.consulta_por_identificador("departamento","codigoDepartamento")
    sql_eliminar = com_sql.eliminar_por_identificador("departamento","codigoDepartamento")
        # DELETE FROM departamento WHERE codigoDepartamento='?'
    if len(cd) != 2:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 2 caracteres")
    try:
        cursor_obj.execute(sql_consultar,(cd,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        cursor_obj.execute(sql_eliminar,(cd,))
        cc.commit()
        return{"mensaje" : f"Se elimino el departamento identificado {rows[0]["codigoDepartamento"]}, {rows[0]["nombreDepartamento"]} "}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

# estado
@app.get("/select/estado")
async def consultar_id_estado(codigoEstado:str):
    ce = codigoEstado
    sql = com_sql.consulta_por_identificador("estado","codigoEstado")
        # SELECT * FROM estado WHERE codigoEstado='{ce}';
    if len(ce) != 3:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 3 caracteres")
    try:
        cursor_obj.execute(sql,(ce,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        return rows
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
@app.post("/insert/estado")
async def registrar_estado(codigoEstado:str,nombreEstado:str):
    sql = """
INSERT INTO estado (codigoEstado,nombreEstado)
VALUES (?,?);
"""
    try:
        cursor_obj.execute(sql,(codigoEstado,nombreEstado))
        cc.commit()
        return {"mensaje":f"Se registro el estado {codigoEstado},{nombreEstado} correctamente"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
# u @app.put("/update")
@app.delete("/delete/estado")
async def eliminar_estado(codigoEstado:str):
    ce = codigoEstado
    sql_consultar = com_sql.consulta_por_identificador("estado","codigoEstado")
    sql_eliminar = com_sql.eliminar_por_identificador("estado","codigoEstado")
    if len(ce) != 3:
        raise HTTPException(status_code=400, detail="Codigo no valido, debe constar de 3 caracteres")
    try:
        cursor_obj.execute(sql_consultar,(ce,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Codigo no encontrado")
        cursor_obj.execute(sql_eliminar,(ce,))
        cc.commit()
        return{"mensaje" : f"Se elimino el estado identificado {rows[0]["codigoEstado"]}, {rows[0]["nombreEstado"]} "}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

# imagen
@app.get("/select/imagen")
async def consultar_id_imagen(refImagen:str):
    ri = refImagen
    sql = com_sql.consulta_por_identificador("imagen","refImagen")
        # SELECT * FROM imagen WHERE refImagen='{ri}';
    if len(ri) < 1 or len(ri) > 32:
        raise HTTPException(status_code=400, detail="Referencia no valido, debe constar entre 1 y 32 caracteres")
    try:
        cursor_obj.execute(sql,(ri,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Referencia no encontrada")
        return rows
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
@app.post("/insert/imagen")
async def registrar_imagen(refImagen:str,fk_codigoCita:str):
    sql = """
INSERT INTO imagen (refImagen,fk_codigoCita)
VALUES (?,?);
"""
    try:
        cursor_obj.execute(sql,(refImagen,fk_codigoCita))
        cc.commit()
        return {"mensaje":f"Se registro la imagen {refImagen},{fk_codigoCita} correctamente"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
# u @app.put("/update")
@app.delete("/delete/imagen")
async def eliminar_imagen(refImagen:str):
    ri = refImagen
    sql_consultar = com_sql.consulta_por_identificador("imagen","refImagen")
    sql_eliminar = com_sql.eliminar_por_identificador("imagen","refImagen")
    if len(ri) < 1 or len(ri) > 32:
        raise HTTPException(status_code=400, detail="Referencia no valido, debe constar entre 1 y 32 caracteres")
    try:
        cursor_obj.execute(sql_consultar,(ri,))
        rows = cursor_obj.fetchall()
        if not rows:
            raise HTTPException(status_code=400, detail="Referencia no encontrada")
        cursor_obj.execute(sql_eliminar,(ri,))
        cc.commit()
        return{"mensaje" : f"Se elimino la imagen identificada {rows[0]["refImagen"]}"}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

# # citaportratamiento
# @app.get("/select/citaportratamiento")
# async def consultar_id_citaportratamiento(id:str):
#     sql = f"""
# SELECT * FROM citaportratamiento WHERE  = ;
# """
#     if len(id) < 0 or len(id) > 1:
#         raise HTTPException(status_code=400, detail="- no valido") 
#     try:
#         cursor_obj.execute(sql)
#         rows = cursor_obj.fetchall()
#         if not rows:
#             raise HTTPException(status_code=400, detail="- no encontrado")
#         return rows
#     except mariadb.Error as e:
#         raise HTTPException(status_code=500, detail=f"Error {e}")
# # c @app.post("/insert")
# # u @app.put("/update")
# # d @app.delete("/delete")
