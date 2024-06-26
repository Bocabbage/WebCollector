USE `mikanani`;

-- create tables

CREATE TABLE IF NOT EXISTS `anime_meta`(
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `uid` BIGINT UNIQUE,
    `name` VARCHAR(128) NOT NULL UNIQUE,
    `download_bitmap` BIGINT DEFAULT 0,
    `is_active` BOOLEAN NOT NULL DEFAULT FALSE,
    `episodes` INT NOT NULL DEFAULT 24,
    `tags` JSON,
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX name_idx (`name`)

) DEFAULT CHARSET=utf8;