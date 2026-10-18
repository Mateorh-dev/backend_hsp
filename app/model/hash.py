import secrets
import string

def generar_hash (longitud:int=5, *data_inicial:str):
    codigo_inicial = "".join(str(c).lower()[0] for c in data_inicial)

    caracter = string.digits + string.ascii_lowercase
    codigo_hash = "".join(secrets.choice(caracter) for _ in range(longitud))
    
    codigo_final = codigo_inicial + codigo_hash
    
    return codigo_final[:longitud]
