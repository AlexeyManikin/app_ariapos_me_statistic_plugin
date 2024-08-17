DROP TABLE IF EXISTS `bills`;
CREATE TABLE `bills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_create` DATETIME NOT NULL,
  `bills_id` int(11) NOT NULL,
  `bills_hash` varchar(32) NOT NULL,
  `operator` varchar(32) NOT NULL,
  `operator_code` varchar(32) NOT NULL,
  `paied_by` varchar(32) NOT NULL,
  `table_desc` varchar(32) NOT NULL,
  `total` FLOAT(10,2) NOT NULL,
  `total_discount` FLOAT(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`bills_id`),
  UNIQUE KEY (`bills_hash`),
  KEY (`operator`),
  KEY (`table_desc`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `dishes`;
CREATE TABLE `dishes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bills_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `item_count` int(11) NOT NULL,
  `price` FLOAT(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`name`),
  INDEX bills_id (bills_id),
    FOREIGN KEY (bills_id)
        REFERENCES bills(bills_id)
        ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;