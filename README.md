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

###Dentro de la carpeta Pririgardus
```
$ sudo chmod +x install.sh
$ ./install.sh
```
##Deployar
```
$ sudo supervisorctl reload 
$ sudo supervisorctl start pririgardus

$ sudo service nginx status
$ sudo service nginx start
```


