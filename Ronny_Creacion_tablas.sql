
Use family_search;
/* ===================== 1) USUARIO (10) ===================== */
INSERT INTO usuario (id_usuario, nombres, apellidos, email, password) VALUES
(1,'Carlos','Pérez','carlos.perez@example.com','hash1'),
(2,'María','Gómez','maria.gomez@example.com','hash2'),
(3,'Juan','Pérez','juan.perez@example.com','hash3'),
(4,'Ana','Pérez','ana.perez@example.com','hash4'),
(5,'Luis','Gómez','luis.gomez@example.com','hash5'),
(6,'Carmen','Ruiz','carmen.ruiz@example.com','hash6'),
(7,'Pedro','Ruiz','pedro.ruiz@example.com','hash7'),
(8,'Laura','Torres','laura.torres@example.com','hash8'),
(9,'Diego','Ruiz','diego.ruiz@example.com','hash9'),
(10,'Sofía','Ruiz','sofia.ruiz@example.com','hash10');

/* ===================== 2) PERSONA (10) ===================== */
INSERT INTO persona
(id_persona, id_usuario_creador, nombres, apellidos, fecha_nacimiento, fecha_defuncion, sexo, lugar_nacimiento, lugar_defuncion, biografia, fecha_actualizacion) VALUES
(1,  1,'Carlos','Pérez','1970-05-10',NULL,'masculino','Guayaquil',NULL,'Ingeniero civil.', CURRENT_TIMESTAMP),
(2,  2,'María','Gómez','1972-08-22',NULL,'femenino','Quito',NULL,'Docente.', CURRENT_TIMESTAMP),
(3,  3,'Juan','Pérez','1995-03-15',NULL,'masculino','Guayaquil',NULL,'Analista de datos.', CURRENT_TIMESTAMP),
(4,  4,'Ana','Pérez','1998-07-30',NULL,'femenino','Guayaquil',NULL,'Diseñadora UX.', CURRENT_TIMESTAMP),
(5,  5,'Luis','Gómez','1945-01-12','2010-09-01','masculino','Riobamba','Guayaquil','Veterano de la fuerza pública.', CURRENT_TIMESTAMP),
(6,  6,'Carmen','Ruiz','1948-11-02','2015-02-20','femenino','Cuenca','Quito','Comerciante.', CURRENT_TIMESTAMP),
(7,  7,'Pedro','Ruiz','1975-04-18',NULL,'masculino','Cuenca',NULL,'Administrador.', CURRENT_TIMESTAMP),
(8,  8,'Laura','Torres','1976-12-05',NULL,'femenino','Loja',NULL,'Arquitecta.', CURRENT_TIMESTAMP),
(9,  9,'Diego','Ruiz','2005-06-10',NULL,'masculino','Quito',NULL,'Estudiante.', CURRENT_TIMESTAMP),
(10,10,'Sofía','Ruiz','2008-09-25',NULL,'femenino','Quito',NULL,'Estudiante.', CURRENT_TIMESTAMP);

/* ============ 3) RELACION_FAMILIAR (>=10, aquí 16) ============ */
INSERT INTO relacion_familiar
(id_relacion, id_persona1, id_persona2, tipo_relacion, id_usuario_creador) VALUES
-- Pareja 1
(1, 1, 2, 'esposo', 1),
(2, 2, 1, 'esposa', 2),
-- Hijos de Carlos y María
(3, 1, 3, 'padre', 1),
(4, 2, 3, 'madre', 2),
(5, 1, 4, 'padre', 1),
(6, 2, 4, 'madre', 2),
-- Abuelos maternos de María
(7, 5, 2, 'padre', 5),
(8, 6, 2, 'madre', 6),
-- Hermanos Juan y Ana
(9,  3, 4, 'hermano', 3),
(10, 4, 3, 'hermana', 4),
-- Pareja 2
(11, 7, 8, 'esposo', 7),
(12, 8, 7, 'esposa', 8),
-- Hijos de Pedro y Laura
(13, 7, 9, 'padre', 7),
(14, 8, 9, 'madre', 8),
(15, 7,10, 'padre', 7),
(16, 8,10, 'madre', 8);

/* ============ 4) REGISTRO_HISTORICO (10) ============ */
INSERT INTO registro_historico
(id_registro_historico, descripcion, tipo_documento, url_documento, id_usuario_subida, fuente_validadora) VALUES
(1,'Acta de nacimiento de Carlos Pérez','acta_nacimiento','https://docs.example.com/acta_carlos',1,'Registro Civil'),
(2,'Acta de nacimiento de María Gómez','acta_nacimiento','https://docs.example.com/acta_maria',2,'Registro Civil'),
(3,'Acta de nacimiento de Juan Pérez','acta_nacimiento','https://docs.example.com/acta_juan',3,'Registro Civil'),
(4,'Acta de nacimiento de Ana Pérez','acta_nacimiento','https://docs.example.com/acta_ana',4,'Registro Civil'),
(5,'Acta de nacimiento de Pedro Ruiz','acta_nacimiento','https://docs.example.com/acta_pedro',7,'Registro Civil'),
(6,'Acta de matrimonio de Carlos Pérez y María Gómez','acta_matrimonio','https://docs.example.com/mat_carlos_maria',2,'Registro Civil'),
(7,'Acta de defunción de Luis Gómez','acta_defuncion','https://docs.example.com/def_luis',5,'Registro Civil'),
(8,'Acta de defunción de Carmen Ruiz','acta_defuncion','https://docs.example.com/def_carmen',6,'Registro Civil'),
(9,'Acta de nacimiento de Laura Torres','acta_nacimiento','https://docs.example.com/acta_laura',8,'Registro Civil'),
(10,'Acta de nacimiento de Sofía Ruiz','acta_nacimiento','https://docs.example.com/acta_sofia',10,'Registro Civil');

/* ===================== 5) ENLACE (>=10) ===================== */
INSERT INTO enlace
(id_persona, id_registro_historico, creacion_id_usuario) VALUES
-- Nacimientos
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(7, 5, 7),
(8, 9, 8),   -- Laura: persona 8 ↔ doc 9
(10,10,10),  -- Sofía: persona 10 ↔ doc 10
-- Matrimonio Carlos & María
(1, 6, 2),
(2, 6, 2),
-- Defunciones
(5, 7, 5),
(6, 8, 6);

/* ===================== 6) HISTORIAL_CAMBIO (10) ===================== */
INSERT INTO historial_cambio
(id_cambio, id_usuario, tipo_entidad, id_entidad) VALUES
(1,  1,'persona',1),
(2,  2,'persona',2),
(3,  3,'persona',3),
(4,  4,'persona',4),
(5,  5,'registro_historico',7),
(6,  6,'registro_historico',8),
(7,  2,'registro_historico',6),
(8,  7,'relacion_familiar',13),
(9,  8,'relacion_familiar',16),
(10, NULL,'persona',9);
