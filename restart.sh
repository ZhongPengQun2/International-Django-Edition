# /bin/bash

docker-compose down
docker-compose build
docker-compose up -d --force-recreate


# pg_dump -h localhost -U postgres -d jiya -f /tmp/jiya-dump.sql
# psql -U postgres -p 6432 -h localhost -d jiya < jiya-dump.sql
