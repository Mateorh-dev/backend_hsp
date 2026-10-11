DELIMITER //
CREATE TRIGGER crear_tratamiento_default
AFTER INSERT
ON paciente
FOR EACH ROW
BEGIN
INSERT INTO tratamiento (nombreTratamiento,fk_numeroIdentificacion)
VALUES ('No Definido',NEW.numeroIdentificacion);
END //
DELIMITER ;