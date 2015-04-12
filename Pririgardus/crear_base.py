from pririgardus import *
from models.models import *

db.create_all()

db.session.add(
    TipoCargo(
        descripcion='Presidencia',
        alcance_cargo=AlcanceCargo.Cargo_Nacional))
db.session.add(
    TipoCargo(
        descripcion='Diputado Nacional',
        alcance_cargo=AlcanceCargo.Cargo_Nacional))
db.session.add(
    TipoCargo(
        descripcion='Senado Provincial',
        alcance_cargo=AlcanceCargo.Cargo_Provincial))
db.session.add(
    TipoCargo(
        descripcion='Gobernación Provincial',
        alcance_cargo=AlcanceCargo.Cargo_Provincial))
db.session.add(
    TipoCargo(
        descripcion='Diputado Provincial',
        alcance_cargo=AlcanceCargo.Cargo_Provincial))
db.session.add(
    TipoCargo(
        descripcion='Senado Departamental',
        alcance_cargo=AlcanceCargo.Cargo_Departamental))
db.session.add(
    TipoCargo(
        descripcion='Intendencia',
        alcance_cargo=AlcanceCargo.Cargo_Local))
db.session.add(
    TipoCargo(
        descripcion='Concejo',
        alcance_cargo=AlcanceCargo.Cargo_Local))

administrador = Rol(Roles.Administrador)
dataEntry = Rol(Roles.DataEntry)
prensa = Rol(Roles.Prensa)

db.session.add_all([administrador, dataEntry, prensa])
db.session.commit()

sudo = Usuario(usuario='SU', passw='prilektoj')
sudo.roles.extend([administrador, dataEntry, prensa])

db.session.add(sudo)

db.session.commit()
