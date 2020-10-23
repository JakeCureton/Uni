CREATE DATABASE `atm`;
CREATE TABLE `customers` (
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `card_id` varchar(20) DEFAULT NULL,
  `last_withdraw` int(3) DEFAULT 0 NULL,
  `card_pin` INT(4) DEFAULT NULL,
  `balance` FLOAT(200) DEFAULT NULL,
  `pin_tries` INT(1) DEFAULT 0 NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
INSERT INTO `customers` VALUES ("John","Smith","4751280038571937","0","1234","500000.00","0");
INSERT INTO `customers` VALUES ("Vera","Jones","4751280038571938","0","1234","2375.28","0");

