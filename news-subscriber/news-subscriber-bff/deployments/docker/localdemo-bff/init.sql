USE `article_db0`;

CREATE TABLE IF NOT EXISTS `article_meta`(
    `id` INT AUTO_INCREMENT,
    `uid` BIGINT UNIQUE,
    `title` VARCHAR(150) NOT NULL,
    `tags` JSON,
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, -- ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;