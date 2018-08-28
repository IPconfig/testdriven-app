#!/bin/bash

fails=""

inspect() {
    if [ $1 -ne 0 ]; then
        fails="${fails} $2"
    fi
}

# run init and integration tests
docker-compose -f docker-compose-dev.yml up -d --build
docker-compose -f docker-compose-dev.yml run users python manage.py test
inspect $? users
docker-compose -f docker-compose-dev.yml run users flake8 project
inspect $? users-lint
docker-compose -f docker-compose-dev.yml run plc python manage.py test
inspect $? plc
docker-compose -f docker-compose-dev.yml run plc flake8 project
inspect $? plc-lint
docker-compose -f docker-compose-dev.yml run client npm test -- --coverage
inspect $? client
docker-compose -f docker-compose-dev.yml down

# run e2e tests
docker-compose -f docker-compose-prod.yml up -d --build
docker-compose -f docker-compose-prod.yml run users python manage.py recreate_db
./node_modules/.bin/cypress run --config baseUrl=http://localhost
inspect $? e2e
docker-compose -f docker-compose-prod.yml down

# return proper code
if [ -n "${fails}" ]; then
    echo "\n"
    echo "Test failed: ${fails}"
    exit 1
else
    echo "Tests passed!"
    exit 0
fi