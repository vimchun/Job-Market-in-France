#!/bin/bash

# Script pour se connecter à la base de donnée "francetravail"
#  (la commande est fastidieuse à taper (même si on peut créer un alias...), d'où le script)

docker exec -it postgres psql -h localhost -U mhh -d francetravail
