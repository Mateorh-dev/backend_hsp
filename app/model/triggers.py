from sqlalchemy import event
from .models import Paciente, Tratamiento
from .hash import generar_hash

@event.listens_for(Paciente, "after_insert")
def crear_tratamiento_default(mapper, conection, target):
    conection.execute(
        Tratamiento.__table__.insert().values(
            codigoHash = generar_hash(7, target.primerNombre, target.primerApellido),
            nombreTratamiento = "No Definido",
            fk_numeroIdentificacion = target.numeroIdentificacion,
        )
    )
