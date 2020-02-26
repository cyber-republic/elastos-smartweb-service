#!/bin/bash

docker container stop smartweb-postgres-test || true && docker container rm -f smartweb-postgres-test || true

# start a postgres docker container
docker run -d --name smartweb-postgres-test \
    -v "$PWD/.postgres-data-test:/var/lib/postgresql/data"     \
    -e POSTGRES_DB=smartweb_test                             \
    -e POSTGRES_USER=gmu                                \
    -e POSTGRES_PASSWORD=gmu                            \
    -p 5436:5432                                        \
    postgres:11-alpine

# wait for database to start
sleep 7
# Copy .sql files to the running container
docker cp ../grpc_adenine/database/scripts/create_table_scripts.sql smartweb-postgres-test:/create_table_scripts.sql
docker cp ../grpc_adenine/database/scripts/reset_database.sql smartweb-postgres-test:/reset_database.sql

# Run the sql scripts
reset=${1-no}
if [ "$reset" == "yes" ]
then
  docker container exec -it smartweb-postgres-test psql -h 172.17.0.1 -d smartweb_test -U gmu -a -q -f /reset_database.sql
fi
docker container exec -it smartweb-postgres-test psql -h 172.17.0.1 -d smartweb_test -U gmu -a -q -f /create_table_scripts.sql


