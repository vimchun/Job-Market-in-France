#!/bin/bash

# Permet de redémarrer tous les services Docker si ceux-ci ne sont plus fonctionnels
#  (après un reboot du pc par exemple)

docker ps -a
docker restart $(docker ps -aq)
