from yoyo import step

step(
    """CREATE TABLE `master_seq` (
    `id` INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`id`));
"""
)