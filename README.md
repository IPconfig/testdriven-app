# Microservices with Docker, Flask and React

Build on arm32v7 (armv7l) or arm32v6 (armv6) for rpi3+. arm64v8 (aarch6) doesn't work since Raspbian is still 32 bit
Not all containers are build for every architecture. Check the [postgres manifest](https://github.com/docker-library/official-images/blob/master/library/postgres) or the [python manifest](https://github.com/docker-library/official-images/blob/master/library/python) to see supported architectures.
For instance, alpine builds do not support arm32v7

To run these images on MacOS, no further actions are needed when Docker for Mac is installed.
For linux, see [here](https://lobradov.github.io/Building-docker-multiarch-images/)

[![Build Status](https://travis-ci.com/IPconfig/testdriven-app.svg?branch=master)](https://travis-ci.com/IPconfig/testdriven-app)

## Environment Variables

### Secret Key
This key should be truly random, so we'll set the key locally and pull it into the container at build time.
To create a key, open the Python shell and run:
```python
>>> import binascii
>>> import os
>>> binascii.hexlify(os.urandom(24))
'9cfb28d74d49ce5bf17b74780a4e0f5a9510c8a3fe086db0'
```
Exit the shell and set the key as an environment variable:
```bash
$ export SECRET_KEY=9cfb28d74d49ce5bf17b74780a4e0f5a9510c8a3fe086db0
```

## Workflow All Services
The following commands are for spinning up all the containers
### Start
Build the images:
```bash
docker-compose -f docker-compose-dev.yml build
```
Run the containers:
```bash
docker-compose -f docker-compose-dev.yml up -d
```
Create and seed the database:
```bash
$ docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db
$ docker-compose -f docker-compose-dev.yml run users python manage.py seed_db
```
Run the unit and integration tests:
```bash
$ docker-compose -f docker-compose-dev.yml run users python manage.py test
```
Lint:
```bash
$ docker-compose -f docker-compose-dev.yml run users flake8 project
```
Run the client-side tests:
```bash
$ docker-compose -f docker-compose-dev.yml run client npm test --verbose
```

### Stop
Stop the containers:
```bash
$ docker-compose -f docker-compose-dev.yml stop
```
Bring down the containers:
```bash
$ docker-compose -f docker-compose-dev.yml down
```
Remove images:
```bash
$ docker rmi $(docker images -q)
```
## Individual Services
The following commands are for spinning up individual containers
### Users DB
Build and run:
```bash
$ docker-compose -f docker-compose-dev.yml up -d --build users-db
```
Test:
```bash
$ docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres
```
### Users
Replace users for plc in the below commands to target PLC
Build and run:
```bash
$ docker-compose -f docker-compose-dev.yml up -d --build users
```
Create and seed the database:
```bash
$ docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db
$ docker-compose -f docker-compose-dev.yml run users python manage.py seed_db
```
Run the unit and integration tests:
```bash
$ docker-compose -f docker-compose-dev.yml run users python manage.py test
```
Lint:
```bash
$ docker-compose -f docker-compose-dev.yml run users flake8 project
```
### Client
Set env variable:
```bash
$ export REACT_APP_USERS_SERVICE_URL=http://localhost
$ export REACT_APP_PLC_SERVICE_URL=http://localhost
```
Build and run:
```bash
$ docker-compose -f docker-compose-dev.yml up -d --build web-service
```
To test, navigate to http://localhost:3007 in your browser
> Keep in mind that you won't be able to register or log in until Nginx is set up

Run the client-side tests:
```bash
$ docker-compose -f docker-compose-dev.yml run client npm test --verbose
```
### Nginx
Build and run
```bash
$ docker-compose -f docker-compose-dev.yml up -d --build nginx
```
To test, navigate to http://localhost in your browser. Also run the e2e tests:
```bash
$ ./node_modules/.bin/cypress open --config baseUrl=http://localhost
```
