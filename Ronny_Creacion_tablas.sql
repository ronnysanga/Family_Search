/* ==================== Base de datos ==================== */
DROP DATABASE IF EXISTS family_search;
CREATE DATABASE IF NOT EXISTS family_search;                
USE family_search;                                         

/* ==========================================================
   TABLA: usuario
   ========================================================== */
CREATE TABLE usuario (
  id_usuario INT NOT NULL AUTO_INCREMENT,                  
  nombres VARCHAR(100) NOT NULL,                          
  apellidos VARCHAR(100) NOT NULL,                       
  email VARCHAR(100) NOT NULL,                         
  password VARCHAR(255) NOT NULL,                          
  fecha_creacion_usuario TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_usuario),                                 /* PK del usuario */
  UNIQUE KEY uq_usuario_email (email)                       /* UNIQUE: evita duplicados de correo */
);

/* ==========================================================
   TABLA: persona
   ========================================================== */
CREATE TABLE persona (
  id_persona INT NOT NULL AUTO_INCREMENT,              
  id_usuario_creador INT NULL,                              /* FK autor: NULL si el usuario es borrado */
  nombres VARCHAR(100) NOT NULL,                     
  apellidos VARCHAR(100) NOT NULL,
  fecha_nacimiento DATE NULL,                            
  fecha_defuncion DATE NULL,                             
  sexo ENUM('masculino','femenino'),              
  lugar_nacimiento VARCHAR(225) NULL,                
  lugar_defuncion VARCHAR(225) NULL,
  biografia TEXT NULL,
  fecha_actualizacion TIMESTAMP NULL,                     
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_persona),
  CONSTRAINT fk_persona_creador
    FOREIGN KEY (id_usuario_creador) REFERENCES usuario(id_usuario)
      ON DELETE SET NULL                                    /* si borran al usuario, se anula el autor */
      ON UPDATE CASCADE,
  /* CHECK: coherencia temporal. Si existen ambas fechas, defunción >= nacimiento. */
  CONSTRAINT ck_persona_fechas
    CHECK (fecha_defuncion IS NULL
           OR fecha_nacimiento IS NULL
           OR fecha_defuncion >= fecha_nacimiento)
);

/* ==========================================================
   TABLA: relacion_familiar 
   ========================================================== */
CREATE TABLE relacion_familiar (
    id_relacion INT NOT NULL AUTO_INCREMENT,
    id_persona1 INT NOT NULL,                                 /* Persona origen */
    id_persona2 INT NOT NULL,                                 /* Persona destino */
    tipo_relacion ENUM('padre', 'madre', 'hijo', 'hija', 'esposo', 'esposa', 'hermano','hermana') NOT NULL, /* id_persona1 es tipo_relacion de id_persona2 */
    id_usuario_creador INT NULL,                              /* Autor de la relación; NULL en caso que el usuario sea borrado */
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_relacion),
    CONSTRAINT fk_rf_p1 FOREIGN KEY (id_persona1) REFERENCES persona(id_persona)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_rf_p2 FOREIGN KEY (id_persona2) REFERENCES persona(id_persona)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_rf_creador FOREIGN KEY (id_usuario_creador) REFERENCES usuario(id_usuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    INDEX ix_rf_p1 (id_persona1),
    INDEX ix_rf_p2 (id_persona2),
    UNIQUE KEY uq_rf (tipo_relacion, id_persona1, id_persona2)
);

-- Trigger para prevenir auto-relaciones
DELIMITER //
CREATE TRIGGER before_insert_relacion_familiar
BEFORE INSERT ON relacion_familiar
FOR EACH ROW
BEGIN
    IF NEW.id_persona1 = NEW.id_persona2 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'No se permite la auto-relación (id_persona1 no puede ser igual a id_persona2)';
    END IF;
END//

CREATE TRIGGER before_update_relacion_familiar
BEFORE UPDATE ON relacion_familiar
FOR EACH ROW
BEGIN
    IF NEW.id_persona1 = NEW.id_persona2 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'No se permite la auto-relación (id_persona1 no puede ser igual a id_persona2)';
    END IF;
END//
DELIMITER ;

/* ==========================================================
   TABLA: registro_historico
   ========================================================== */
CREATE TABLE registro_historico (
  id_registro_historico INT NOT NULL AUTO_INCREMENT,      
  descripcion TEXT NOT NULL,                                /* descricion  del documento */
  tipo_documento ENUM('acta_nacimiento','acta_matrimonio','acta_defuncion','titulo_academico','otra') DEFAULT 'otra',                                         /* Dominio con valor por defecto */
  url_documento TEXT NULL,                                  
  id_usuario_subida INT NULL,                               /* Autor de la subida; NULL si el usuario fue borrado */
  fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  fuente_validadora VARCHAR(45) NULL,                       /* Ej: "Registro Civil" para una acta_nacimiento, "Espol" para un titulo */
  PRIMARY KEY (id_registro_historico),
  INDEX fk_rh_usuario (id_usuario_subida),                  /* Índice para consultas */
  CONSTRAINT fk_rh_usuario
    FOREIGN KEY (id_usuario_subida) REFERENCES usuario(id_usuario)
      ON DELETE SET NULL /* mantener documento aunque el usuario que subio la data se borre */
      ON UPDATE CASCADE /* actualizacion en cascada de la id del usuario que hizo la subida */
);

/* ==========================================================
   TABLA: enlace (persona ↔ registro_historico) - se la creo para que no haya M:N 
   ========================================================== */
CREATE TABLE enlace (
  id_persona INT NOT NULL,                                  /* Persona referenciada */
  id_registro_historico INT NOT NULL,                       /* Documento referenciado */
  fecha_enlazamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  creacion_id_usuario INT NULL,                              /* Usuario que creó el enlace; NULL si se borra */
  PRIMARY KEY (id_persona, id_registro_historico),          /* Pk compuesto*/
  CONSTRAINT fk_enlace_persona
    FOREIGN KEY (id_persona) REFERENCES persona(id_persona)
      ON DELETE CASCADE         /* Borrado en cascada */                    
      ON UPDATE CASCADE,        /* Update en cascada */
  CONSTRAINT fk_enlace_registro
    FOREIGN KEY (id_registro_historico) REFERENCES registro_historico(id_registro_historico)
      ON DELETE CASCADE         /* Borrado en cascada */                        
      ON UPDATE CASCADE,        /* Update en cascada */
  CONSTRAINT fk_enlace_usuario
    FOREIGN KEY (creacion_id_usuario) REFERENCES usuario(id_usuario)
      ON DELETE SET NULL        /* al borrar usuario que creo ese enlace, el enlace sobrevive sin autor */
      ON UPDATE CASCADE         /* Update del id del usuario creador del enlace */
);

/* ==========================================================
   TABLA: historial_cambio (log)
   ========================================================== */
CREATE TABLE historial_cambio (
  id_cambio INT NOT NULL AUTO_INCREMENT,                    /* PK del cambio */
  id_usuario INT NULL,                                      /* Autor del cambio; NULL si el usuario fue borrado */
  tipo_entidad ENUM('persona','registro_historico','relacion_familiar') NOT NULL, /* entidades a la que se le modificara y generara un log */
  id_entidad INT NOT NULL,                                  /* ID espefico de la instancia de la entidad afectada */
  fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_cambio),
  INDEX fk_hc_usuario (id_usuario),                         
  INDEX ix_hc_target (tipo_entidad, id_entidad),        
  CONSTRAINT fk_hc_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
      ON DELETE SET NULL  /* conservar el log aunque el usuario se borre */
      ON UPDATE CASCADE   /* Update de id usuario ligado a ese log */
);
