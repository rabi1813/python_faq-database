CREATE TABLE IF NOT EXISTS  `approval_table` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `master_id` VARCHAR(45) NOT NULL,
    `type` VARCHAR(45),
    `query` VARCHAR(500),
    `answer` VARCHAR(500),
    `create_datetime` TIMESTAMP,
    `create_by` VARCHAR(50),
    `mod_datetime` TIMESTAMP,
    `mod_by` VARCHAR(50),
    PRIMARY KEY (`id`, `master_id`));