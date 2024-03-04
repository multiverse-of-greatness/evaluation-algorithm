#!/bin/zsh

NAME="neo4j"
BIND_PATH=~/docker-bind/neo4j
IMAGE=neo4j:5.17.0-community

docker run -d --name $NAME \
    -p 7474:7474 -p 7687:7687 \
    -v $BIND_PATH/data:/data \
    -v $BIND_PATH/import:/import \
    -v $BIND_PATH/logs:/logs \
    -v $BIND_PATH/plugins:/plugins \
    $IMAGE
