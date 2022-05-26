"""
Main Deployment script
"""
import os
import uuid
import globalvar

from yoyo import read_migrations
from yoyo import get_backend
from yoyo import backends
from yoyo import migrations


db_host = globalvar.db_host
db_application_name = globalvar.db_name
db_user = globalvar.db_user
db_password = globalvar.db_password
path_query_file = globalvar.path_query_file
path_db_scripts = globalvar.path_db_scripts
db_default_name = 'sys'

migrations_all = migrations.MigrationList()
migrations_db = read_migrations(f'{path_db_scripts}/01_database')
migrations_yoyo = read_migrations(f'{path_db_scripts}/00_yoyo_setup')

migrations_all = read_migrations(f'{path_db_scripts}/00_yoyo_setup')
migrations_all.extend(read_migrations(f'{path_db_scripts}/02_table'))
# migrations_all.extend(read_migrations(f'{path_db_scripts}/03_index'))
# migrations_all.extend(read_migrations(f'{path_db_scripts}/04_view'))
# migrations_all.extend(read_migrations(f'{path_db_scripts}/05_function'))
# migrations_all.extend(read_migrations(f'{path_db_scripts}/06_storedprocedure'))
# migrations_all.extend(read_migrations(f'{path_db_scripts}/07_referencedata'))
# migrations_all.extend(read_migrations(f'{path_db_scripts}/08_custom'))


def get_application_migration_ids(backend:backends.DatabaseBackend) -> migrations.MigrationList:
    return backend.to_apply(migrations_all)


def store_application_migration_ids_in_file(miglist:migrations.MigrationList, backend:backends.DatabaseBackend):
    queries = []
    unique_id = uuid.uuid4()

    for m in miglist:
        queries.append(f"Insert into `y_custom_version`(`version`,`migration_id`) values ('{unique_id}','{m.id}')\n")

    with open(path_query_file, 'w') as query_file:
        query_file.write("".join(queries))

    if (len(queries) > 0):
        print(f"Version : {unique_id}")


def apply_migrations(miglist:migrations.MigrationList, backend:backends.DatabaseBackend, force=False):
    with backend.lock():
        try:
            backend.begin()
            backend.apply_migrations(miglist, force)
            backend.commit()
        except Exception as e:
            print("Exception occured during migration. Rolling back...")
            print(str(e))
            backend.rollback()


def reapply(version:str):
    backend = get_backend(f"mysql://{db_user}:{db_password}@{db_host}/{db_application_name}")
    migrations = get_migrations_for_version(version, backend)
    apply_migrations(migrations, backend, True)
    print(f"Version: {version} has been reapplied.")

def get_migrations_for_version(version:str, backend:backends.DatabaseBackend) -> migrations.MigrationList:
    rows_version = []
    rows = list(backend.execute(f"select migration_id from y_custom_version where `version` = '{version}'"))
    for row in rows:
        rows_version.append(row[0])
    return migrations_all.filter(lambda x: x.id in rows_version)

def apply_db_level_migration(backend_db:backends.DatabaseBackend):
    with backend_db.lock():
        backend_db.apply_migrations(backend_db.to_apply(migrations_db))

def rollback_version(version:str,backend:backends.DatabaseBackend):
    rollbacks = get_migrations_for_version(version, backend)

    with backend.lock():
        try:
            backend.begin()
            backend.rollback_migrations(rollbacks)
            backend.commit()
        except Exception as e:
            print("Exception occured during migration. Rolling back...")
            print(str(e))
            backend.rollback()

def rollback(version:str):
    backend = get_backend(f"mysql://{db_user}:{db_password}@{db_host}/{db_application_name}")
    rollback_version(version, backend)
    print(f"Rollback of Version: {version} performed.")

def cleanup():
    try:
        os.remove(path_query_file)
    except:
        print(f'Warning: The file {path_query_file} does not exist or the program is unable to delete the file.')

def deploy():
    #Connect to MySQL's sys database for creating/altering database
    backend_db = get_backend(f"mysql://{db_user}:{db_password}@{db_host}/{db_default_name}")
    apply_db_level_migration(backend_db=backend_db)

    #Connect to application database for creating/altering resources inside the database
    backend = get_backend(f"mysql://{db_user}:{db_password}@{db_host}/{db_application_name}")

    miglist = get_application_migration_ids(backend)

    if len(miglist) == 0:
        print("Nothing to deploy. The Database is already up to date.")
    else:
        store_application_migration_ids_in_file(miglist, backend)
        apply_migrations(miglist, backend)
        cleanup()


deploy()
