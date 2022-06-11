CREATE TABLE IF NOT EXISTS `{db_name}`.`latest_version` (
    `version_number` INT NOT NULL AUTO_INCREMENT,
    `version_id` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`version_number`, `version_id`));
