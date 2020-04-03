#!/bin/bash

# Script que ejecutara travis para hacer el deploy si el build pasa.

USER='PS'
IP='s7-rest.francecentral.cloudapp.azure.com'

FILE=$(mktemp tmpXXX)

echo $TRAVIS_RSA > $FILE

ssh -i $FILE $USER@$IP << EOF
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

rm $FILE
