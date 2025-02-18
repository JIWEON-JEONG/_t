CREATE DATABASE IF NOT EXISTS nota_assignment;
USE nota_assignment;

CREATE TABLE IF NOT EXISTS `user` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `created_at` timestamp(6) NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` timestamp(6) NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO user (name) VALUES ('TestTeacher01'), ('TestTeacher02'), ('TestTeacher03');
