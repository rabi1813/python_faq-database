from yoyo import step
import globalvar

step(
    f"CREATE DATABASE {globalvar.db_name}",
    f"DROP DATABASE {globalvar.db_name}"
)
