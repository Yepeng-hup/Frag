-- Server version       5.7.37

-- CREATE DATABASE `frag` CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci';

CREATE TABLE `event` (
  `event_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_date` varchar(30) NOT NULL,
  `event_info` text NOT NULL,
  `event_name` varchar(10) NOT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `hefu` (
  `hefu_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hefu_date` varchar(30) NOT NULL,
  `hefu_time` varchar(30) NOT NULL,
  `hefu_info` text NOT NULL,
  `hefu_name` varchar(10) NOT NULL,
  PRIMARY KEY (`hefu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `maintain` (
  `maintain_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `maintain_date` varchar(30) NOT NULL,
  `maintain_time` varchar(30) NOT NULL,
  `maintain_info` varchar(250) NOT NULL,
  `maintain_name` varchar(10) NOT NULL,
  PRIMARY KEY (`maintain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(20) NOT NULL,
  `user_passwd` varchar(250) NOT NULL,
  `user_identity` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES (1,'2023-01-21 01:43:09','admin','pbkdf2:sha256:260000$NQBjKalxy3oVONTX$f49934dbae72530411cea3fdf6cde524fc9a6a8ab37dedf4084351ba904226d8','Admin');
UNLOCK TABLES;

CREATE TABLE `user_lock` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(20) NOT NULL,
  `user_locks` varchar(10) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `documents` (
  `documents_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `documents_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `documents_title` varchar(100) NOT NULL,
  `documents_label` varchar(50) NOT NULL,
  `documents_text` text NOT NULL,
  PRIMARY KEY (`documents_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `textLabel` (
  `textlabel_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `textlabel_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `textlabel_title` varchar(50) NOT NULL,
  PRIMARY KEY (`textlabel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `system`(
    `system_id` INT UNSIGNED AUTO_INCREMENT,
    `system_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
    `system_ResourcesName` VARCHAR(20) NOT NULL,
    `system_ResourcesNum` VARCHAR(20) NOT NULL,
    PRIMARY KEY ( `system_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `server_ssh_list`(
    `ssh_list_id` INT UNSIGNED AUTO_INCREMENT,
    `ssh_list_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
    `ssh_list_hostname` VARCHAR(50) NOT NULL,
    `ssh_list_hostip` VARCHAR(50) NOT NULL,
    `ssh_list_port` VARCHAR(10) NOT NULL,
    `ssh_list_user` VARCHAR(30) NOT NULL,
    `ssh_list_password` VARCHAR(250) NOT NULL,
    `ssh_list_system_user` VARCHAR(30) NOT NULL,
    PRIMARY KEY ( `ssh_list_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


