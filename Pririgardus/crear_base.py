from pririgardus import *
from models.models import *

db.create_all()

db.session.add(
    TipoCargo(
        descripcion='Presidencia',
        alcance_cargo=AlcanceCargo.Cargo_Nacional.name))
db.session.add(
    TipoCargo(
        descripcion='Diputado Nacional',
        alcance_cargo=AlcanceCargo.Cargo_Nacional.name))
db.session.add(
    TipoCargo(
        descripcion='Senado Provincial',
        alcance_cargo=AlcanceCargo.Cargo_Provincial.name))
db.session.add(
    TipoCargo(
        descripcion='Gobernación Provincial',
        alcance_cargo=AlcanceCargo.Cargo_Provincial.name))
db.session.add(
    TipoCargo(
        descripcion='Diputado Provincial',
        alcance_cargo=AlcanceCargo.Cargo_Provincial.name))
db.session.add(
    TipoCargo(
        descripcion='Senado Departamental',
        alcance_cargo=AlcanceCargo.Cargo_Departamental.name))
db.session.add(
    TipoCargo(
        descripcion='Intendencia',
        alcance_cargo=AlcanceCargo.Cargo_Local.name))
db.session.add(
    TipoCargo(
        descripcion='Concejo',
        alcance_cargo=AlcanceCargo.Cargo_Local.name))

pais_arg = Pais(descripcion='Argentina')
prov_sta = Provincia(descripcion='Santa Fe', pais=pais_arg)
dep_ros = Departamento(descripcion='Rosario', provincia=prov_sta)
loc_ros = Localidad(descripcion='Rosario', departamento=dep_ros)

db.session.add_all([pais_arg, prov_sta, dep_ros, loc_ros])

mesanum = 6000
esccir = [['Rep Paraguay', 'Malvinas', 'Normal 1'], ['Normal 3', 'Moreno']]
for secnum in range(1, 22):
    secc = Seccional(numero=str(secnum), localidad=loc_ros)
    db.session.add(secc)
    for cirnum in range(1, 2):
        circ = Circuito(descripcion='Circuito ' + str(cirnum), seccional=secc)
        db.session.add(circ)
        for escnom in esccir[cirnum - 1]:
            esc = Escuela(descripcion=escnom, circuito=circ)
            db.session.add(esc)
            for i in range(1, 3):
                mesa = Mesa(numero=mesanum, escuela=esc)
                mesanum += 1
                db.session.add(mesa)

tipocargos = TipoCargo.query.all()
con = tipocargos[7]
cl = Cargo_Local(loc_ros, con)
db.session.add(cl)
fren = Frente('FPCYS')
db.session.add(fren)
lis = Lista('Por los barrios', fren, cl)
lis2 = Lista('Jirardi', fren, cl)
db.session.add_all([lis, lis2])
inten = tipocargos[6]
ci = Cargo_Local(loc_ros, inten)
db.session.add(inten)
lis = Lista('Arriba Rosario', fren, ci)
lis2 = Lista('Fein', fren, ci)
db.session.add_all([lis, lis2])
db.session.commit()
