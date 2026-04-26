"""
COMPORTAMIENTO OBJETO
Objeto solicita (tabla, id, **kwargs)
  kwargs, va a constar de "nombre":"tipo"
  # (NO VA) items = Objetos pydantic # A partir de los datos de arriba se genra un objeto
  metodo get
  metodo post
  metodo put
  metodo delete
"""

import comandos_sql as com_sql

class SistemaCRUD:
    """
    id (dict): "nombre_id":[tamaño #,validacion("fijo"|"rango")]
    """
    def __init__(self, tabla:str, identificador:dict, **atributos):
        self.tabla = tabla
        self.id = identificador
        self.atributos = atributos
    
    def get(self, protocolos:dict, identificador):
        HTTPException = protocolos['HTTPException']
        cursor_obj = protocolos['cursor_obj']
        mariadb = protocolos['mariadb']

        (nombre_id, tipo_id), = self.id.items()
        
        sql = com_sql.consulta_por_identificador(self.tabla,nombre_id)        
        
        error_consulta = False
        if tipo_id[1] == "fijo" and len(identificador) != tipo_id[0]:
            error_consulta = True
        elif tipo_id[1] == "rango" and len(identificador) not in range(1,tipo_id[0]):
            error_consulta = True

        if error_consulta:
            raise HTTPException(status_code=400, detail=f"{nombre_id}: ({identificador}) no valido")
        
        try:
            cursor_obj.execute(sql,(identificador,))
            rows = cursor_obj.fetchall()
            if not rows:
                raise HTTPException(status_code=400, detail=f"{nombre_id}:: ({identificador}) no encontrado")
            return rows
        except mariadb.Error as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")
    def post(self, protocolos:dict, *valores):
        HTTPException = protocolos['HTTPException']
        cursor_obj = protocolos['cursor_obj']
        mariadb = protocolos['mariadb']
        cc = protocolos['cc']

        columnas = []
        columnas.append(list(self.id.keys())[0])
        columnas.extend(list(self.atributos.keys()))

        sql = com_sql.insertar_datos(self.tabla,columnas)

        try:
            cursor_obj.execute(sql,valores)
            cc.commit()
            return f"Se registro en {self.tabla}: {valores[0]} exitosamente"
        except mariadb.Error as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")
    def put(self, protocolos:dict, identificador, **atr_valores):
        HTTPException = protocolos['HTTPException']
        cursor_obj = protocolos['cursor_obj']
        mariadb = protocolos['mariadb']
        cc = protocolos['cc']

        (nombre_id, tipo_id), = self.id.items()
        tupla_identificador = (nombre_id,identificador)

        sql, valores = com_sql.actualizar_datos(self.tabla,tupla_identificador,atr_valores)
        sql_consulta = com_sql.consulta_por_identificador(self.tabla,nombre_id)        
        
        error_consulta = False
        if tipo_id[1] == "fijo" and len(identificador) != tipo_id[0]:
            error_consulta = True
        elif tipo_id[1] == "rango" and len(identificador) not in range(1,tipo_id[0]):
            error_consulta = True

        if error_consulta:
            raise HTTPException(status_code=400, detail=f"{nombre_id}: ({identificador}) no valido")

        try:
            cursor_obj.execute(sql_consulta,(identificador,))
            rows = cursor_obj.fetchall()
            if not rows:
                raise HTTPException(status_code=400, detail=f"{nombre_id}: ({identificador}) no encontrado")
            cursor_obj.execute(sql, tuple(valores))
            cc.commit()
            cursor_obj.execute(sql_consulta,(identificador,))
            rows = cursor_obj.fetchall()
            return f"Se actualizo en {self.tabla}: {rows[0]}"
        except mariadb.Error as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")
    def delete(self, protocolos:dict, identificador):
        HTTPException = protocolos['HTTPException']
        cursor_obj = protocolos['cursor_obj']
        mariadb = protocolos['mariadb']
        cc = protocolos['cc']

        (nombre_id, tipo_id), = self.id.items()
        
        sql_consultar = com_sql.consulta_por_identificador(self.tabla,nombre_id)
        sql_eliminar = com_sql.eliminar_por_identificador(self.tabla,nombre_id)
        
        error_consulta = False
        if tipo_id[1] == "fijo" and len(identificador) != tipo_id[0]:
            error_consulta = True
        elif tipo_id[1] == "rango" and len(identificador) not in range(1,tipo_id[0]):
            error_consulta = True

        if error_consulta:
            raise HTTPException(status_code=400, detail=f"{nombre_id}: ({identificador}) no valido")
        
        try:
            cursor_obj.execute(sql_consultar,(identificador,))
            rows = cursor_obj.fetchall()
            if not rows:
                raise HTTPException(status_code=400, detail=f"{nombre_id}: ({identificador}) no encontrado")
            cursor_obj.execute(sql_eliminar,(identificador,))
            cc.commit()
            return f"Se elimino en {self.tabla}: {rows}"
        except mariadb.Error as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")
