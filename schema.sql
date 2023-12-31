CREATE TABLE `email_sent_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email_sender` varchar(320) DEFAULT NULL,
  `email_receiver` varchar(320) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `email_contents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email_sent_log_id` int DEFAULT NULL,
  `email_subject` varchar(255) DEFAULT NULL,
  `email_message` text,
  PRIMARY KEY (`id`),
  KEY `fk_email_sent_log_contents` (`email_sent_log_id`),
  CONSTRAINT `fk_email_sent_log_contents` FOREIGN KEY (`email_sent_log_id`) REFERENCES `email_sent_log` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `email_attachments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email_sent_log_id` int DEFAULT NULL,
  `email_attachment_name` varchar(255) DEFAULT NULL,
  `mime_type` varchar(255) DEFAULT NULL,
  `attachment_size_bytes` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_email_sent_log_attachments` (`email_sent_log_id`),
  CONSTRAINT `fk_email_sent_log_attachments` FOREIGN KEY (`email_sent_log_id`) REFERENCES `email_sent_log` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `email_profanity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email_sent_log_id` int DEFAULT NULL,
  `filter_profanity_selected` tinyint(1) DEFAULT NULL,
  `subject_contains_profanity` tinyint(1) DEFAULT NULL,
  `message_contains_profanity` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_email_sent_log_profanity` (`email_sent_log_id`),
  CONSTRAINT `fk_email_sent_log_profanity` FOREIGN KEY (`email_sent_log_id`) REFERENCES `email_sent_log` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;