FROM python:3.7.7-alpine3.11

# Variables de entorno
ENV deployment true
ENV PYTHONUNBUFFERED 1

# Mantainer
label MANTAINER='pedro.tamargo.allue@gmail.com'

# Creamos el directorio de trabajos
RUN mkdir servidor
WORKDIR servidor
# Copiamos el repositorio al contenedor
COPY ../servidor .

# Instalamos dependencias
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev curl \
    libffi-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

# Para instalar django
#RUN pip3 install -r requirements.txt


# Exponemos el puerto 8000 (http)
EXPOSE 8000

# Exponemos el puerto 443 (https)
EXPOSE 443

# Iniciamos la aplicacion
ENTRYPOINT ["python3", "manage.py", "runserver"]