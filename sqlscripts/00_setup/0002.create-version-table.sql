CREATE TABLE IF NOT EXISTS `python_faq`.`_migration_version_log` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `version_id` VARCHAR(45) NOT NULL,
    `file_name` VARCHAR(100) NULL,
    `query` VARCHAR(1000) NULL,
    `status` VARCHAR(10) NULL,
    `error` VARCHAR(1000) NULL,
    `create_datetime` TIMESTAMP(30) NULL,
    `create_by` VARCHAR(45) NULL,
    PRIMARY KEY (`id`, `version_id`),
    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);