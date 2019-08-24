#/bin/bash

docker stack rm youtubeparty && \
docker build -t youtubeparty:0.1 . && \
docker stack deploy -c docker-compose.yml youtubeparty
