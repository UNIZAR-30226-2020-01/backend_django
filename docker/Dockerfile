FROM python:3.7.7-alpine3.11

# Variables de entorno
ENV deployment true
ENV PYTHONUNBUFFERED 1

# Mantainer
label MANTAINER='pedro.tamargo.allue@gmail.com'

# Creamos el directorio de trabajos
RUN mkdir servidor
WORKDIR servidor

# Copiamos el requirements.txt al contenedor
COPY servidor/requirements.txt .

# Instalamos dependencias
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev curl git \
    libffi-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt \
    && pip install gunicorn \
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

# Copiamos el repositorio al contenedor
COPY servidor .

# Exponemos el puerto 8000 (conexion interna)
EXPOSE 8000

# Iniciamos la aplicacion
#ENTRYPOINT ["python3", "manage.py", "runserver"]
