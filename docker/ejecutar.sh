#!/bin/bash

# Para compilar y ejecutar el servidor Django

docker='sudo docker'
image='django_prod_image'
name='django_prod'
flags='-p 8000:8000 -p 443:443/tcp --name '$name

# Eliminamos el contenedor anterior
$docker stop $name
$docker rm $name

# Eliminamos la imagen anterior
$docker rmi $image

# Compilamos la nueva imagen
$docker build -t $image .

# Ejecutamos el docker en segundo plano
$docker run $flags $image