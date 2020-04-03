#!/bin/bash

# Script que ejecutara travis para hacer el deploy si el build pasa.

USER='PS'
IP='s7-rest.francecentral.cloudapp.azure.com'

FILE="../travis_rsa"

chmod 0600 $FILE

#yes | ssh -i $FILE $USER@IP 'pwd'
ssh -i $FILE -o 'StrictHostKeyChecking no' $USER@$IP << EOF
  cd ~ps/backend_django
  git pull origin master
  cd ~ps
  # Paramos el servicio
  sudo docker-compose down
  # Reconstruimos la imagen
  sudo docker-compose build
  # Levantamos el servicio
  sudo docker-compose up -d
EOF
