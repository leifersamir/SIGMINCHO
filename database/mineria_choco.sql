-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-08-2026 a las 23:04:57
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `mineria_choco`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes`
--

CREATE TABLE `reportes` (
  `id` int(11) NOT NULL,
  `municipio` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `evidencia` varchar(255) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(20) NOT NULL DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reportes`
--

INSERT INTO `reportes` (`id`, `municipio`, `descripcion`, `evidencia`, `fecha`, `estado`) VALUES
(2, 'Quibdó', 'no importa locass', '462ba1e1-c136-40f2-b630-fc675e825182_Captura_de_pantalla_2026-05-20_170739.png', '2026-08-07 01:11:36', 'Rechazado'),
(3, 'Puné', 'Mineria ilegal utilizando menores de edad', 'd3bc5f63-9831-4de2-a2b6-7518f8fb3a09_Captura_de_pantalla_2026-07-13_115001.png', '2026-08-07 17:17:53', 'Rechazado'),
(4, 'Quibdó', 'Prueba de funcionamiento del sistema de reportes.', 'ecd8ccac-6ed2-467d-98af-f43a3a9b9f84_Captura_de_pantalla_2026-06-19_154913.png', '2026-08-07 17:28:07', 'Aprobado'),
(5, 'Quibdó', 'http://127.0.0.1:5000', '83203b08-2c59-4b73-aabf-c5d86c883e9a_Captura_de_pantalla_2026-05-19_231052.png', '2026-08-07 17:46:28', 'Aprobado'),
(6, 'Buenaventura', 'Por cantar me mandan Pack', 'ba761bba-868d-41df-a35c-0cad14377193_Organizacion_4K.png', '2026-08-07 18:07:13', 'Aprobado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `usuario` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('admin','usuario') NOT NULL DEFAULT 'usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `usuario`, `correo`, `contraseña`, `rol`) VALUES
(1, 'Leifer', 'Samir', 'leifersamir@gmail.com', 'scrypt:32768:8:1$tKVidOX02fsGJ62n$eae5253dcda10186b12cb1eccfeb52b789c4931e6fcddc4433fef9ee583266a5569f30d2a4a2a24438d49eda35f5107b4dbd52a2bceda35c7d688805196d11b5', 'admin'),
(2, 'leifer samir', 'leifer', 'leifersamir@gmail.com', 'scrypt:32768:8:1$cyCVIJXTMNrUAufR$c9fda9ac846655dbd2ef8016360328c955124c627b52210f40841e66d13813a121867daca76bb1d7a09b2e831910e64dee7a05b72ca556af6e6a6f7fd9db3eab', 'admin'),
(4, 'Americano 4KT', '4KT', 'Ameri_4KT@gmail.com', 'scrypt:32768:8:1$ny5nXk7nMGm2tMO7$1f977ccbebb9b3ebfed813091451645741e24b2674dc4d4c20d6c12bfc4415eefc9869e7e62a8d272f857b02f83fe0aa6e922fa0b14b4a9a475b83a2fa1567e4', 'usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `reportes`
--
ALTER TABLE `reportes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
