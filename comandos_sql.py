def consulta_paginada(nombretabla:str,pagina:int):
    return f"""
SELECT * FROM {nombretabla} LIMIT 20 OFFSET {(pagina-1)*20};
"""
def consulta_por_identificador(tabla:str,identificador:str):
    return f"""
SELECT * FROM {tabla} WHERE {identificador}=?;
"""
def eliminar_por_identificador(tabla:str,identificador:str):
    return f"""
DELETE FROM {tabla} WHERE {identificador}=?;
"""
def insertar_datos(tabla:str,columnas:list):
    return f"""
INSERT INTO {tabla} ({",".join(columnas)})
VALUES ({",".join(["?"]*len(columnas))});
"""
def actualizar_datos(tabla:str,identificador:tuple,atributos:dict):
    datos_filtrados = {}
    for clave, valor in atributos.items():
        if valor not in ["",0]:
            datos_filtrados[clave] = valor
    datos_formateados = []
    for atributo in list(datos_filtrados.items()):
        datos_formateados.append(f"{atributo[0]} = ?")
        # if type(atributo[1]) is str:
        #     datos_formateados.append(f"{atributo[0]} = '{atributo[1]}'")
        # elif type(atributo[1]) is int:
        #     datos_formateados.append(f"{atributo[0]} = {atributo[1]}")
    atributos_actualizar = ", ".join(datos_formateados)
    valores = list(datos_filtrados.values())
    valores.append(identificador[1])
    return f"""
UPDATE {tabla}
SET {atributos_actualizar}
WHERE {identificador[0]} = ?;
""", valores