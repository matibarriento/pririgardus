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

echo "Puerto de ejecucion (Asegurese de que este libre Ej. 5000):"
read puertoE

echo "Puerto de acceso (Asegurese de que esta libre Ej. 8080)" 
read puertoA

echo "Usuario que ejecuta el servicio (Asegurese que exista y tenga los permisos)"
read usuario

if [ ! -d "$BASE_DIR/logs" ]; then
    mkdir "logs"
fi

if [ ! -d "$BASE_DIR/conf" ]; then
    mkdir "conf"
fi

if [ ! -f "$BASE_DIR/conf/pririgardus.supervisor.conf" ]; then
    echo "Creando SUPERVISOR"
    printf "[program:pririgardus]
command = %s/bin/gunicorn -w %i -b 0.0.0.0:%i pririgardus:app
directory = %s/Pririgardus/
user = %s" "$BASE_DIR" "$workers" "$puertoE" "$BASE_DIR" "$usuario" >> "$BASE_DIR/conf/pririgardus.supervisor.conf"

fi

if [ ! -f "/etc/supervisor/conf.d/pririgardus.conf" ]; then
    sudo rm "/etc/supervisor/conf.d/pririgardus.conf"
fi

sudo ln -s "$BASE_DIR/conf/pririgardus.supervisor.conf" "/etc/supervisor/conf.d/pririgardus.conf"

if [ ! -f "$BASE_DIR/conf/pririgardus" ]; then
    echo "Creando NGINX"
    printf "server {
        
        listen %i;
        
        #server_name pririgardus

        location / {
            proxy_pass http://localhost:%i;
        }

        location /static {
            alias  %s/Pririgardus/static/;
        }

    }" "$puertoA" "$puertoE" "$BASE_DIR" >> "$BASE_DIR/conf/pririgardus"

fi

if [ ! -f "/etc/nginx/sites-available/pririgardus" ]; then

    sudo rm "/etc/nginx/sites-available/pririgardus"

fi

if [ ! -f "/etc/nginx/sites-enabled/pririgardus" ]; then

    sudo rm "/etc/nginx/sites-enabled/pririgardus"

fi

sudo ln -s "$BASE_DIR/conf/pririgardus" "/etc/nginx/sites-available/pririgardus"
sudo ln -s "/etc/nginx/sites-available/pririgardus" "/etc/nginx/sites-enabled/pririgardus"
        

sudo iptables -I INPUT -p tcp --dport ${portA} -j ACCEPT

