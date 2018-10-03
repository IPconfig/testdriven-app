#!/bin/bash

# create
docker-compose -f docker-compose-dev.yml run users python manage.py recreate-db
docker-compose -f docker-compose-dev.yml run plc python manage.py recreate-db
# seed
docker-compose -f docker-compose-dev.yml run users python manage.py seed-db
docker-compose -f docker-compose-dev.yml run plc python manage.py seed-db