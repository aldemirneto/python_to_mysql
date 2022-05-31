DROP TABLE IF EXISTS `cliente`;
CREATE TABLE `cliente` (
  `IdCliente` int NOT NULL AUTO_INCREMENT,
  `PrimeiroNome` varchar(255) NOT NULL,
  `UltimoNome` varchar(255) NOT NULL,
  `Idade` int DEFAULT NULL,
  PRIMARY KEY (`IdCliente`)
) 


DROP TABLE IF EXISTS `plano`;
CREATE TABLE `plano` (
  `idplano` int NOT NULL AUTO_INCREMENT,
  `idcliente` int NOT NULL,
  `InicioPlano` date NOT NULL,
  `UltimoPagamento` date NOT NULL,
  PRIMARY KEY (`idplano`),
  KEY `idcliente` (`idcliente`),
  CONSTRAINT `plano_ibfk_1` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`IdCliente`) ON DELETE CASCADE
) 