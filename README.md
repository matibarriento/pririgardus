# pririgardus
Pririgardus es un apliación para llevar los computos de comicios
===

##Requerimientos de software
```
$ sudo apt-get install python3.4 python3.4-dev nginx supervisor python-pip git
$ sudo pip install virtualenv 
```

##Descargar

###Estando en la carpeta desde donde se quiera usar.
```
$ git clone https://github.com/matibarriento/pririgardus.git
$ cd pririgardus
```

##Instalación

### NO CREES EL VIRTUALENV, EL SCRIPT LO HACE POR TI.

###Dentro de la carpeta creada
```
$ cd pririgardus
$ sudo chmod +x install.sh
$ ./install.sh
```
## Iniciar

### Dentro de pririgardus

```
$ source bin/activate                       #para activar el virtualenv
$ python crear_base.py                      #para crear la base y los datos iniciales
$ python "tu propio script de datos"
$ ipython                                   # para hacer pruebas o cargas
$ deactivate

```

##Deployar
```
$ sudo supervisorctl reload 
$ sudo supervisorctl start pririgardus

$ sudo service nginx status
$ sudo service nginx start
```
##Usuario admin
usuario: SU
contraseña: prilektoj


#TODO

###ABM de Datos
###Mejorar documentación
###Informes más detallados
###Sistema D'Hondt
###Otros
 
