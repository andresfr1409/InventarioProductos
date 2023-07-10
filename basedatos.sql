CREATE DATABASE coltis_productos;
USE coltis_productos;

CREATE TABLE producto (
  codigo int(6) AUTO_INCREMENT PRIMARY KEY,
  nombre varchar(100) NOT NULL,
  precio decimal(10,2) NOT NULL
);
