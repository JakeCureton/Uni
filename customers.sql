CREATE TABLE `customers` (
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `card_id` varchar(20) DEFAULT NULL,
  `last_withdraw` varchar(1) DEFAULT NULL
  `card_pin` INT(20) DEFAULT NULL,
  `balance` FLOAT(200) DEFAULT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
INSERT INTO `customers` VALUES ("John","Smith","4751280038571937","1","1234","500000.00");

