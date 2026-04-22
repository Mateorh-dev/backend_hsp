"""
COMPORTAMIENTO FUNCION
recorrer cada tabla
  recorrer cada valor
    contruir la linea
    comprobar si es fk
      NOTA:fk no se deben espefican valores, toma los de su referencia, omitiendo si es PK o AUTO
      Cada fk solo se creara si exite la tabla, en caso contrario debera de guardarse en una lisa para crearse al final
      En caso de no poderse crear, se enlista para mensaje de advertencia
"""

def DiccionarioSQL(diccionario:dict):

    def TraductorAcroTipos(valores:list):        
        atributos_titulo = []
            
        atributos_titulo.append(f"{valores[0]}")
        if "NN" in valores:
            atributos_titulo.append(f"NOT NULL")
        if "AUTO" in valores:
            atributos_titulo.append(f"AUTO_INCREMENT")
        if "PK" in valores:
            atributos_titulo.append(f"PRIMARY KEY")
        
        tipo_dato = " ".join(atributos_titulo)

        return tipo_dato
    def ConstruirTitulo(titulo:str, valores:list):
        tipo_dato = TraductorAcroTipos(valores)

        linea = f"    {titulo} {tipo_dato}"

        return linea
    def LigarLlaveForanea(tabla:str, titulo:str):
        linea = f"    FOREIGN KEY (fk_{titulo}) REFERENCES {tabla}({titulo})"

        return linea
    def AñadirTituloExtra(tabla:str, titulo:str, valores:list):
        tipo_dato = TraductorAcroTipos(valores)
        
        linea = f"ALTER TABLE {tabla}\n"
        linea += f"ADD COLUMN {titulo} {tipo_dato};"

        return linea
    def LigarLlaveForaneaExtra(tabla:str,fk_tabla:str,titulo:str):
        linea = f"ALTER TABLE {tabla}\n"
        linea += f"ADD CONSTRAINT fk_{titulo}\n"
        linea += f"FOREIGN KEY (fk_{titulo}) REFERENCES {fk_tabla}({titulo});"

        return linea

    tablas_creadas = {}    
    comandos_sql = []
    fk_pendientes = {}

    for tabla, contenido in diccionario.items():
        comandos_tabla = ""

        crear_tabla = f"CREATE TABLE {tabla} (\n"
        comandos_tabla += crear_tabla

        columnas = []

        for titulo, valores in contenido.items():

            if not "FK" in valores:
                columnas.append(ConstruirTitulo(titulo,valores))
            elif "FK" in valores:
                referencia = titulo.split(".")
                fk_tabla = referencia[0]
                fk_titulo = referencia[1]

                columnas_existentes = list(tablas_creadas.get(fk_tabla,{}))
                if fk_titulo in columnas_existentes:
                    valores = list(tablas_creadas.get(fk_tabla).get(fk_titulo))
                    if "PK" in valores:
                        valores.remove("PK")
                        valores.append("NN")
                    if "AUTO" in valores:
                        valores.remove("AUTO")

                    columnas.append(ConstruirTitulo(f"fk_{fk_titulo}",valores))
                    columnas.append(LigarLlaveForanea(fk_tabla,fk_titulo))
                else:
                    fk_pendientes[tabla] = titulo

        columnas_tabla = ",\n".join(columnas)
        comandos_tabla += columnas_tabla

        cierre_tabla = f"\n);"
        comandos_tabla += cierre_tabla

        comandos_sql.append(comandos_tabla)
        tablas_creadas[tabla] = contenido

    fk_no_creadas = {}
    comandos_tabla = ""
    columnas = []

    for tabla, titulo in fk_pendientes.items():
        referencia = titulo.split(".")
        fk_tabla = referencia[0]
        fk_titulo = referencia[1]

        columnas_existentes = list(tablas_creadas.get(fk_tabla,{}))
        if fk_titulo in columnas_existentes:
            valores = list(tablas_creadas.get(fk_tabla).get(fk_titulo))
            valores.remove("PK")
            valores.append("NN")

            columnas.append(AñadirTituloExtra(tabla,f"fk_{fk_titulo}",valores))
            columnas.append(LigarLlaveForaneaExtra(tabla,fk_tabla,fk_titulo))
        else:
            fk_no_creadas[tabla] = titulo
    comandos_tabla = "\n".join(columnas)
    comandos_sql.append(comandos_tabla)

    sql = "\n".join(comandos_sql)

    if fk_no_creadas:
        print(f"""
{"*"*50}
    No se puedieron crear las conexiones
    {fk_no_creadas}
{"*"*50}
""")

    return sql

"""
REFERENCIAS
      
CREATE TABLE cita (
    codigoCita CHAR(16) PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    patologias TEXT,
    tratamientoRecomendado TEXT,
    precio INT,
    observacion TEXT,
    fk_codigoEstado CHAR(3) NOT NULL
);
CREATE TABLE citaportratamiento (
    fk_codigoTratamiento CHAR(16) NOT NULL,
    fk_codigoCita CHAR(16) NOT NULL,
    FOREIGN KEY (fk_codigoTratamiento) REFERENCES Tratamiento(codigoTratamiento),
    FOREIGN KEY (fk_codigoCita) REFERENCES cita(codigoCita)
);
ALTER TABLE paciente
add CONSTRAINT fk_codigoMunicipio
FOREIGN KEY (fk_codigoMunicipio) REFERENCES municipio(codigoMunicipio);


ALTER TABLE Pedidos
ADD COLUMN id_cliente INT;

ALTER TABLE Pedidos
ADD CONSTRAINT fk_pedidos_clientes
FOREIGN KEY (id_cliente)
REFERENCES Clientes(id_cliente);
"""