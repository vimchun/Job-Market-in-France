#!/bin/bash

# Permet de redémarrer tous les services Docker si ceux-ci ne sont plus fonctionnels
#  (peut faire fonctionner la conf, sinon réexécuter le script "docker_compose_down_up.sh")

docker ps -a
docker restart $(docker ps -aq)
