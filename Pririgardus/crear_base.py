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

administrador = Rol(Roles.Administrador.name)
dataEntry = Rol(Roles.DataEntry.name)
prensa = Rol(Roles.Prensa.name)

db.session.add_all([administrador, dataEntry, prensa])
db.session.commit()

sudo = Usuario(usuario='SU', passw='prilektoj')
sudo.roles.extend([administrador, dataEntry, prensa])

db.session.add(sudo)

db.session.commit()
