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