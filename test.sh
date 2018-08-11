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
docker-compose -f docker-compose-dev.yml run client npm test -- --coverage
inspect $? client
docker-compose -f docker-compose-dev.yml down

# return proper code
if [ -n "${fails}" ]; then
    echo "\n"
    echo "Test failed: ${fails}"
    exit 1
else
    echo "Tests passed!"
    exit 0
fi