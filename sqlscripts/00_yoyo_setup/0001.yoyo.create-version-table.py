##Table to store versions for each deployment
# Do not delete this table or script.

from yoyo import step

step(
    "Create Table `y_custom_version` (`version_id` int auto_increment, `version` varchar(50), `migration_id` varchar(255), created_at_utc timestamp Default CURRENT_TIMESTAMP, PRIMARY KEY(`version_id`))",
    "DROP TABLE y_custom_version"
)