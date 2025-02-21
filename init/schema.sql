-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS nota_assignment;
USE nota_assignment;

-- user 테이블 생성
CREATE TABLE IF NOT EXISTS `user` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `created_at` timestamp(6) NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` timestamp(6) NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 이메일 인증 테이블 생성
CREATE TABLE IF NOT EXISTS `email_verification` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `code` varchar(255) NOT NULL,
  `retry_count` int NOT NULL DEFAULT '0',
  `success` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `user_email_UNIQUE_email_verification` (`email`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 회사 테이블 생성
CREATE TABLE IF NOT EXISTS `company` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 프로젝트 테이블 생성
CREATE TABLE IF NOT EXISTS `project` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `owner_id` int NOT NULL,
  `description` varchar(50) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `owner_UNIQUE_project` (`owner_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 프로젝트 사용자 역할 테이블 생성
CREATE TABLE IF NOT EXISTS `project_user_role` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `user_id` int NOT NULL,
  `role` enum('OWNER','EDITOR','VIEWER') NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `idx_project_user` (`project_id`,`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 업무 테이블 생성
CREATE TABLE IF NOT EXISTS `task` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `manager_id` int NOT NULL,
  `description` varchar(255) NOT NULL,
  `is_completed` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 사용자 세션 테이블 생성
CREATE TABLE IF NOT EXISTS `user_session` (
  `id` varchar(64) NOT NULL,
  `user_id` int NOT NULL,
  `ip` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `expires_at` datetime(6) NOT NULL,
  `last_active` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `user_UNIQUE_session` (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `company` (name)
VALUES 
  ('CompanyA')

INSERT INTO `user` (name, role, email, company_id, password) 
VALUES 
  ('TestMember', 'MEMBER', 'testmember@example.com', 1, "$2b$12$vGBP2FaDluPJfKYlJuPaAe8xVnW9waTuPWp.wKKnyt9/F1niDh1IG"), 
  ('TestAdmin', 'ADMIN', 'testadmin@example.com', 1, "$2b$12$vGBP2FaDluPJfKYlJuPaAe8xVnW9waTuPWp.wKKnyt9/F1niDh1IG"), 
  ('TestProjectOwner', 'PROJECT_OWNER', 'testprojectowner@example.com', 1, "$2b$12$vGBP2FaDluPJfKYlJuPaAe8xVnW9waTuPWp.wKKnyt9/F1niDh1IG"), 

INSERT INTO `email_verification` (email, code, retry_count, success) 
VALUES 
  ('testmember@example.com', 'code1', 1, 1), 
  ('testadmin@example.com', 'code2', 1, 1), 
  ('testprojectowner@example.com', 'code3', 1, 1);