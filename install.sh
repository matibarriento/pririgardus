#!/bin/bash

BASE_DIR=$(pwd)

if [ ! -d "$BASE_DIR/bin" ]; then
    echo "Creando virtualenv"
    virtualenv . --python=python3.4
    echo "Virtualenv creada"
fi

echo "Instalando requirements"
$BASE_DIR/bin/pip install -r requirements.txt
echo "Requirements instalados"

echo "BIN in $BASE_DIR/bin"

echo "Numeros de workers (Ideal es 2xCPU + 1):"
read workers

echo "Puerto de ejecucion (Asegurese de que este libre):"
read puerto 

echo "Usuario que ejecuta el servicio (Asegurese que exista y tenga los permisos)"
read usuario


if [ ! -f "conf/pririgardus.supervisor.conf" ]; then
    echo "Creando SUPERVISOR"
    printf "[program:pririgardus]
    command = %s/bin/gunicorn -w %i -b 0.0.0.0:%i pririgardus:app
    directory = %s/Pririgardus/
    user = %s
    autostart=true
    autorestart=true" "$BASE_DIR" "$workers" "$puerto" "$BASE_DIR" "$usuario" >> "conf/pririgardus.supervisor.conf"

    sudo ln -s "conf/pririgardus.supervisor.conf" "/etc/supervisor/conf.d/pririgardus.conf"
fi

if [ ! -f "conf/pririgardus" ]; then
    echo "Creando NGINX"
    printf "server {

        location / {
            proxy_pass http://localhost:%i;
        }

        location /static {
            alias  %s/Pririgardus/static;
        }
        
    }" "$puerto" "$BASE_DIR" >> "conf/pririgardus"

    sudo ln -s "conf/pririgardus" "/etc/nginx/sites-available/pririgardus"
    sudo ln -s "/etc/nginx/sites-available/pririgardus" "/etc/nginx/sites-enabled/pririgardus"
fi
