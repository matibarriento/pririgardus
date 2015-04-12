# pririgardus
Pririgardus es un apliación para llevar los computos de comicios
===

##Requerimientos de software
```
$ sudo apt-get install python3.4 python3.4-dev nginx supervisor virtualenv git 
```

##Descargar

###Estando en la carpeta desde donde se quiera usar.
```
$ git clone https://github.com/matibarriento/pririgardus.git
$ cd Pririgardus
```

##Instalación

### NO CREES EL VIRTUALENV, EL SCRIPT LO HACE POR TI.

###Dentro de la carpeta creada
```
$ sudo chmod +x install.sh
$ ./install.sh
```
## Iniciar

### Dentro de Pririgardus

```
$ source bin/activate                       #para activar el virtualenv
$ python crear_base.py                      #para crear la base y los datos iniciales
$ python cargar_datos_rosario_muestra.py    #o tu propio script de datos
$ deactivate

```

##Deployar
```
$ sudo supervisorctl reload 
$ sudo supervisorctl start pririgardus

$ sudo service nginx status
$ sudo service nginx start
```



