CREATE DATABASE IF NOT EXISTS `tictactoe`;
USE `tictactoe`;

CREATE TABLE IF NOT EXISTS `results` (
    `jogo` int NOT NULL AUTO_INCREMENT,
    `jogador1` int DEFAULT 0,
    `jogador2` int DEFAULT 0,
    `velha` int DEFAULT 0,
    PRIMARY KEY (`jogo`)
)