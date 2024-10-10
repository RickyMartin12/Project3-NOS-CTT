-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 08-Out-2024 às 15:52
-- Versão do servidor: 10.4.24-MariaDB
-- versão do PHP: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `concelho_distritos`
--

-- --------------------------------------------------------

create database concelho_distritos;

--
-- Estrutura da tabela `distrito_conc_post`
--

CREATE TABLE `distrito_conc_post` (
  `id` int(11) NOT NULL,
  `codigo_postal` varchar(255) DEFAULT NULL,
  `concelhos` varchar(255) DEFAULT NULL,
  `distritos` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Extraindo dados da tabela `distrito_conc_post`
--

INSERT INTO `distrito_conc_post` (`id`, `codigo_postal`, `concelhos`, `distritos`) VALUES
(1, '8700-141', 'Olhão', 'Faro'),
(2, '2520-193', 'Peniche', 'Leiria'),
(3, '8700-141', 'Olhão', 'Faro'),
(4, '8700-141', 'Olhão', 'Faro'),
(5, '8700-141', 'Olhão', 'Faro'),
(6, '2520-193', 'Peniche', 'Leiria'),
(7, '8700-143', 'Olhão', 'Faro'),
(8, '8700-145', 'Olhão', 'Faro');

--
-- Índices para tabelas despejadas
--


--
-- Índices para tabela `distrito_conc_post`
--
ALTER TABLE `distrito_conc_post`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de tabelas despejadas
--


--
-- AUTO_INCREMENT de tabela `distrito_conc_post`
--
ALTER TABLE `distrito_conc_post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
