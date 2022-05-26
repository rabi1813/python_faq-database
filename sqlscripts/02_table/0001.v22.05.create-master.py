from yoyo import step

step(
    """CREATE TABLE `master` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `master_id` VARCHAR(45) NOT NULL,
    `type` VARCHAR(45) NULL,
    `query` VARCHAR(500) NULL,
    `answer` VARCHAR(500) NULL,
    PRIMARY KEY (`id`, `master_id`));
"""
)