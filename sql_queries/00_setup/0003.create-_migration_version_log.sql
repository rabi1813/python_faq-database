CREATE TABLE IF NOT EXISTS `{db_name}`.`_migration_version_log` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `version_id` VARCHAR(45) NOT NULL,
    `file_name` VARCHAR(100) NULL,
    `query` VARCHAR(1000) NULL,
    `status` VARCHAR(10) NULL,
    `error` VARCHAR(1000) NULL,
    `execution_datetime` TIMESTAMP(6) NULL,
    `executed_by` VARCHAR(45) NULL,
    PRIMARY KEY (`id`, `version_id`),
    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);