CREATE DATABASE IF NOT EXISTS llm_messages
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
USE llm_messages;
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
