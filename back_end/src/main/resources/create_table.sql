CREATE TABLE `conversation` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `userId` bigint NOT NULL,
    `name` varchar(255) NOT NULL,
    `ifUseLib` tinyint(1) NOT NULL,
    `libId` bigint DEFAULT NULL,
    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `robotId` bigint DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=230 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `file` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `libId` bigint NOT NULL,
    `fileName` varchar(255) NOT NULL,
    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `size` double(10,2) NOT NULL,
    `type` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `lib` (
   `id` bigint NOT NULL AUTO_INCREMENT,
   `userId` bigint NOT NULL,
   `name` varchar(255) NOT NULL,
   `size` double(10,2) NOT NULL,
   `description` text NOT NULL,
   PRIMARY KEY (`id`),
   UNIQUE KEY `userId` (`userId`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `message` (
   `id` bigint NOT NULL AUTO_INCREMENT,
   `conversationId` bigint NOT NULL,
   `isPerson` tinyint(1) NOT NULL,
   `content` text NOT NULL,
   `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=851 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `robot` (
     `id` bigint NOT NULL AUTO_INCREMENT,
     `userId` bigint NOT NULL,
     `name` varchar(255) NOT NULL,
     `prompt` text NOT NULL,
     `intro` text,
     PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `user` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `salt` varchar(255) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci