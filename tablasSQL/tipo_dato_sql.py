"""
Equivalencia a los tipos de datos de SQL
"""

class Char:
    """
    CHAR
    """
    def __init__(self,longitud:int):
        self.longitud = longitud
    def __str__(self):
        return f"CHAR({self.longitud})"

class Varchar:
    """
    VARCHAR(n)
    """
    def __init__(self,longitud:int):
        self.longitud = longitud
    def __str__(self):
        return f"VARCHAR({self.longitud})"

class Text:
    """
    TEXT
    """
    def __init__(self):
        pass
    def __str__(self):
        return f"TEXT"

class Int:
    """
    INT | INT(n)
    """
    def __init__(self,digitos:int=None):
        self.digitos = digitos
    def __str__(self):
        if self.digitos is not None:
            return f"INT({self.digitos})"
        else:
            return f"INT"

class Decimal:
    """
    DECIMAL(n,d)
    """
    def __init__(self,digitos:int,decimales:int=2):
        self.digitos = digitos
        self.decimales = decimales
    def __str__(self):
        return f"DECIMAL({self.digitos},{self.decimales})"

class Date:
    """
    DATE
    """
    def __init__(self):
        pass
    def __str__(self):
        return f"DATE"

class Time:
    """
    TIME
    """
    def __init__(self):
        pass
    def __str__(self):
        return f"TIME"

class Bool:
    """
    TINYINT(1)
    """
    def __init__(self):
        pass
    def __str__(self):
        return f"TINYINT(1)"