CREATE SCHEMA `adminproyectos` ;

CREATE TABLE `adminproyectos`.`roles` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre_rol` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`));

insert into roles(id, nombre_rol) values (default, 'ANALISTA_FUNCIONAL');
insert into roles(id, nombre_rol) values (default, 'DEV_OPS');
insert into roles(id, nombre_rol) values (default, 'ADM_BASES_DATOS');
insert into roles(id, nombre_rol) values (default, 'LIDER_TECNICO');
insert into roles(id, nombre_rol) values (default, 'LIDER_AREA');

CREATE TABLE `adminproyectos`.`usuario` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `apellido` VARCHAR(50) NOT NULL,
  `genero` VARCHAR(10),
  `email` VARCHAR(100),
  `password` VARCHAR(256),
  `telefono` VARCHAR(15),
  `id_rol` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `roles_fk` FOREIGN KEY(`id_rol`) references `roles`(`id`) ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into usuario(id, nombre, apellido, genero, email, password, telefono, id_rol) values(default, 'NOMBRE_TEST1', 'APELLIDO_TEST1', 'M', 'EMAIL_TEST1@gmail.com', '123456', '4334444', 1);
insert into usuario(id, nombre, apellido, genero, email, password, telefono, id_rol) values(default, 'NOMBRE_TEST2', 'APELLIDO_TEST1', 'F', 'EMAIL_TEST2@gmail.com', '123456', '4443333', 6);
insert into usuario(id, nombre, apellido, genero, email, password, telefono, id_rol) values(default, 'NOMBRE_TEST3', 'APELLIDO_TEST1', 'M', 'EMAIL_TEST3@gmail.com', '123456', '4123333', 6);

CREATE TABLE `adminproyectos`.`proyectos` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `descripcion` VARCHAR(150) NOT NULL,
  `cantidad_integrantes` INT NOT NULL,
  `total_precio` FLOAT,
  `total_horas` FLOAT,
  `id_lider` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `lider_fk` FOREIGN KEY(`id_lider`) references `usuario`(`id`) ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into proyectos(id, nombre, descripcion, cantidad_integrantes, total_precio, total_horas, id_lider) values (default, 'PROYECTO1', 'Proyecto de prueba', 1, 100.0, 100.0, 4);
insert into proyectos(id, nombre, descripcion, cantidad_integrantes, total_precio, total_horas, id_lider) values (default, 'PROYECTO_TEST2', 'Proyecto de testing', 1, 100.0, 100.0, 4);

CREATE TABLE `adminproyectos`.`usuarios_proyectos` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `id_usuario` BIGINT NOT NULL,
  `id_proyecto` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `usuario_fk` FOREIGN KEY(`id_usuario`) references `usuario`(`id`) ON UPDATE CASCADE,
  CONSTRAINT `proyecto_fk` FOREIGN KEY(`id_proyecto`) references `proyectos`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into usuarios_proyectos(id, id_usuario, id_proyecto) values (default, 5, 1);
insert into usuarios_proyectos(id, id_usuario, id_proyecto) values (default, 6, 1);
insert into usuarios_proyectos(id, id_usuario, id_proyecto) values (default, 7, 2);

CREATE TABLE `adminproyectos`.`sprints` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `fecha_inicio` DATETIME NOT NULL,
  `fecha_fin` DATETIME NULL,
  `obs` VARCHAR(150),
  `estado` BOOLEAN,
  `id_proyecto` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `proyecto_sprint_fk` FOREIGN KEY(`id_proyecto`) references `proyectos`(`id`) ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into sprints(id, nombre, fecha_inicio, fecha_fin, obs, estado, id_proyecto) values (default, 'sprint1', '2020-12-01', '2020-12-31', 'observaciones', 1, 1);
insert into sprints(id, nombre, fecha_inicio, fecha_fin, obs, estado, id_proyecto) values (default, 'sprint2', '2021-01-01', '2021-01-31', 'observaciones', 0, 1);

CREATE TABLE `adminproyectos`.`requerimientos` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `cant_horas` INT(11),
  `fecha_inicio` DATETIME NULL,
  `fecha_fin` DATETIME NULL,
  `descripcion` VARCHAR(150) NOT NULL,
  `observacion` VARCHAR(100) NULL,
  `id_sprint` BIGINT NOT NULL,
  `id_usuario` BIGINT NULL,
  `id_proyecto` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `req_proyecto_fk` FOREIGN KEY(`id_proyecto`) references `proyectos`(`id`) ON UPDATE CASCADE,
  CONSTRAINT `req_usuario_fk` FOREIGN KEY(`id_usuario`) references `usuario`(`id`) ON UPDATE CASCADE,
  CONSTRAINT `req_sprint_fk` FOREIGN KEY(`id_sprint`) references `sprints`(`id`) ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;