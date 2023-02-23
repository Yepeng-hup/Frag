-- Server version       5.7.37

DROP TABLE IF EXISTS `event`;
CREATE TABLE `event` (
  `event_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_date` varchar(30) NOT NULL,
  `event_info` text NOT NULL,
  `event_name` varchar(10) NOT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `hefu`;
CREATE TABLE `hefu` (
  `hefu_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hefu_date` varchar(30) NOT NULL,
  `hefu_time` varchar(30) NOT NULL,
  `hefu_info` text NOT NULL,
  `hefu_name` varchar(10) NOT NULL,
  PRIMARY KEY (`hefu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `maintain`;
CREATE TABLE `maintain` (
  `maintain_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `maintain_date` varchar(30) NOT NULL,
  `maintain_time` varchar(30) NOT NULL,
  `maintain_info` varchar(250) NOT NULL,
  `maintain_name` varchar(10) NOT NULL,
  PRIMARY KEY (`maintain_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `server`;
CREATE TABLE `server` (
  `server_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `server_date` varchar(30) NOT NULL,
  `server_name` varchar(100) NOT NULL,
  `server_dataBackup` varchar(100) NOT NULL,
  `server_status` varchar(30) NOT NULL,
  `server_policeNum` varchar(10) NOT NULL,
  `server_info` text NOT NULL,
  `server_userName` varchar(6) NOT NULL,
  PRIMARY KEY (`server_id`),
  FULLTEXT KEY `info_index` (`server_info`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(20) NOT NULL,
  `user_passwd` varchar(250) NOT NULL,
  `user_identity` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES (1,'2023-01-21 01:43:09','admin','pbkdf2:sha256:260000$NQBjKalxy3oVONTX$f49934dbae72530411cea3fdf6cde524fc9a6a8ab37dedf4084351ba904226d8','Admin');
UNLOCK TABLES;