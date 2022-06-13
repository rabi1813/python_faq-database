CREATE TABLE IF NOT EXISTS  `query_table` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `query_id` VARCHAR(45) NOT NULL,
    `type` VARCHAR(45),
    `query` VARCHAR(500),
    `answer` VARCHAR(500),
    `create_datetime` TIMESTAMP,
    `create_by` VARCHAR(50),
    `mod_datetime` TIMESTAMP,
    `mod_by` VARCHAR(50),
    PRIMARY KEY (`id`, `query_id`));