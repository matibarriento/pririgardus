from pririgardus import *
from models.models import *

db.create_all()

pais_arg = Pais(descripcion='Argentina')
prov_sta = Provincia(descripcion='Santa Fe', pais=pais_arg)
dep_ros = Departamento(descripcion='Rosario', provincia=prov_sta)
loc_ros = Localidad(descripcion='Rosario', departamento=dep_ros)
secc_15 = Seccional(numero='15', localidad=loc_ros)
cir_15 = Circuito(descripcion='Circuito', seccional=secc_15)
esc_para = Escuela(descripcion='Rep del Paraguay', circuito=cir_15)
mesa_1 = Mesa(numero=1, descripcion='', escuela=esc_para)
mesa_2 = Mesa(numero=2, descripcion='', escuela=esc_para)
mesa_3 = Mesa(numero=3, descripcion='', escuela=esc_para)


db.session.add(pais_arg)
db.session.add(prov_sta)
db.session.add(dep_ros)
db.session.add(loc_ros)
db.session.add(loc_ros)

db.session.add(secc_15)
db.session.add(cir_15)
db.session.add(esc_para)
db.session.add(mesa_1)
db.session.add(mesa_2)
db.session.add(mesa_3)

db.session.commit()
