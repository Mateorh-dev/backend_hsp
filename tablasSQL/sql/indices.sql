-- CREATE INDEX idx_nombre ON tabla(columna)

-- Indice compuesto
CREATE INDEX idx_tratamiento_cita ON citaportratamiento(fk_codigoTratamiento,fk_codigoCita);


-- CREATE INDEX idx_citaportratamiento ON citaportratamiento(codigoCitaPorTratamiento)
-- CREATE INDEX fk_codigoCita ON citaportratamiento(fk_codigoCita);
-- CREATE INDEX fk_codigoTratamiento ON citaportratamiento(fk_codigoTratamiento);
-- CREATE INDEX idx_paciente ON paciente(numeroIdentificacion)
-- CREATE INDEX idx_tratamiento ON tratamiento(codigoTratamiento)
-- CREATE INDEX idx_cita ON cita(codigoCita)
-- CREATE INDEX idx_estadocita ON estadocita(codigoEstado)
-- CREATE INDEX idx_imagen ON imagen(codigoImagen)
