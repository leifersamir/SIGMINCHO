-- ============================================================
-- Base de datos: mineria_choco
-- Proyecto: SIGMINCHO - Reporte ciudadano de minería ilegal
-- ============================================================

CREATE DATABASE IF NOT EXISTS mineria_choco
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE mineria_choco;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT(11) NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('admin','usuario') NOT NULL DEFAULT 'usuario',
    PRIMARY KEY (id),
    UNIQUE KEY usuario (usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS reportes (
    id INT(11) NOT NULL AUTO_INCREMENT,
    municipio VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    evidencia VARCHAR(255) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Pendiente','Aprobado','Rechazado') NOT NULL DEFAULT 'Pendiente',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Para crear el primer administrador:
-- 1. Registra un usuario desde /registro.
-- 2. En phpMyAdmin ejecuta:
-- UPDATE usuarios SET rol='admin' WHERE usuario='TU_USUARIO';