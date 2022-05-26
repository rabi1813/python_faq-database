# Python FAQ Database Migration Scripts
The scripts in this repository are used to create Python FAQ Database. It makes use of a database schema
migration tool called [yoyo-migrations](https://pypi.org/project/yoyo-migrations/).

## Setup
To set up this repository in your local machine, do the following:

1. Clone this repository.
2. Open Windows command prompt.
3. Navigate to the repository's folder.
4. Run the following command:
```commandline
pip install -r requirements.txt --user
```

## Developing SQL Scripts
1. Prepare the migration and rollback script and test in your local database.
2. Once both scripts are tested, add the script to relevant folders under 'sqlscripts' folder. Make sure the name
of the files unique among all folders. Follow the example file naming conventions.

## Running Migration Scripts

Run the deploy.py script with deploy commented out. The version is the one that is printed during previous
deployment. The versions are also stored in y_custom_version table in your application database.
```
#deploy()
rollback("52a4327f-4299-4557-b31d-7a4c8955a9ef")
```

## Rolling back a version
Run the deploy.py script with deploy commented out. The version is the one that is printed during previous
deployment. The versions are also stored in y_custom_version table in your application database.
```
#deploy()
rollback("52a4327f-4299-4557-b31d-7a4c8955a9ef")
```

## Re-applying a version
Run the deploy.py script with reapply commented out. The version is the one that is printed during previous
deployment. The versions are also stored in y_custom_version table in your application database.
```
#deploy()
#rollback("52a4327f-4299-4557-b31d-7a4c8955a9ef")
reapply("52a4327f-4299-4557-b31d-7a4c8955a9ef")
```

