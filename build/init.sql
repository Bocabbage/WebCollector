USE `mikanani`;

-- create tables

CREATE TABLE IF NOT EXISTS `anime_meta`(
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `uid` BIGINT UNIQUE,
    `name` VARCHAR(128) NOT NULL UNIQUE,
    `download_bitmap` BIGINT DEFAULT 0,
    `is_active` BOOLEAN NOT NULL DEFAULT FALSE,
    `tags` VARCHAR(256) DEFAULT NULL,
    INDEX id_idx (`uid`),
    INDEX name_idx (`name`)

) DEFAULT CHARSET=utf8;