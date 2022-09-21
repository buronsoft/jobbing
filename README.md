# Swagger generated server

## Overview
Backend for 'Jalisco con Empleo' application.

Documentation:
[Flask](https://flask.palletsprojects.com/en/2.0.x/)
[Connexion](https://github.com/zalando/connexion)
[OpenAPI](https://swagger.io/specification/)

## Requirements
Python 3.5.2+

## Virtual environment
To create a virtual environment on Windows, use:
```
python3 -m venv venv
venv\Scripts\activate
```

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt

set FLASK_ENV=development
set FLASK_DEBUG=1
flask run
```

and open your browser to here:

```
http://localhost:8080/ui/
```

Your Swagger definition lives here:

```
http://localhost:8080/swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## DB 
Following variable should be defined as system environment:

- **JOBBING_DB_PWD**. The password phrase for the database

### DB migrations

Flask-migrate workflow consists of two consequent commands which generates the migration:
```
flask db migrate
```
and which applies the migration
```
flask db upgrade
```

## Importing data

Executin seeds:
```
flask seed list
flask seed run <listedSeeder>
```
If NoModuleNamed error, run (for Windows):
```
set PYTHONPATH=.
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t jobbing .

# starting up a container
docker run -p 8080:8080 jobbing
```

## Creating a docker with Postgres
```
docker run --name postgresql-container -p 5432:5432 -e POSTGRES_PASSWORD=admin -d postgres
psql -h localhost -p 5432 -d postgres -U postgres --password`
```


TODOS:
- Add find provider by skill
- Check created at that sets a value for default
- Check ID for save operation that sets a value for default
