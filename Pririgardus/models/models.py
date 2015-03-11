#models.models.py
from flask.ext.sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()


class Pais(db.Model):

    """docstring for Pais"""

    __tablename__ = "Pais"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20), unique=True)
    #propiedad 'provincias' para obtener sus hijas

    def __init__(self, descripcion=''):
        self.descripcion = descripcion

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        mesas = []
        for pro in self.provincias.all():
            mesas.extend(pro.getMesas())
        return mesas


class Provincia(db.Model):

    """docstring for Provincia"""

    __tablename__ = "Provincia"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20), unique=True)
    pais_id = db.Column(db.Integer, db.ForeignKey('Pais.id'))
    pais = db.relationship('Pais', backref=db.backref(
                           'provincias', lazy='dynamic'))
    #propiedad 'departamentos' para obtener sus hijas

    def __init__(self, descripcion='', pais=''):
        self.descripcion = descripcion
        self.pais = pais

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        mesas = []
        for dep in self.departamentos.all():
            mesas.extend(dep.getMesas())
        return mesas


class Departamento(db.Model):

    """docstring for Departamento"""

    __tablename__ = "Departamento"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    provincia_id = db.Column(db.Integer, db.ForeignKey('Provincia.id'))
    provincia = db.relationship('Provincia', backref=db.backref(
        'departamentos', lazy='dynamic'))
    #propiedad 'localidades' para obtener sus hijas

    def __init__(self, descripcion='', provincia=''):
        self.descripcion = descripcion
        self.provincia = provincia

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        mesas = []
        for loc in self.localidades.all():
            mesas.extend(loc.getMesas())
        return mesas


class Localidad(db.Model):

    """docstring for Localidad"""

    __tablename__ = "Localidad"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    departamento_id = db.Column(db.Integer, db.ForeignKey('Departamento.id'))
    departamento = db.relationship('Departamento', backref=db.backref(
        'localidades', lazy='dynamic'))
    #propiedad 'seccionales' para obtener sus hijas

    def __init__(self, descripcion='', departamento=''):
        self.descripcion = descripcion
        self.departamento = departamento

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        mesas = []
        for secc in self.seccionales.all():
            mesas.extend(secc.getMesas())
        return mesas


class Seccional(db.Model):

    """docstring for Seccional"""

    __tablename__ = "Seccional"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20))
    localidad_id = db.Column(db.Integer, db.ForeignKey('Localidad.id'))
    localidad = db.relationship('Localidad', backref=db.backref(
        'seccionales', lazy='dynamic'))
    #propiedad 'circuitos' para obtener sus hijas

    def __init__(self, numero='', localidad=''):
        self.numero = numero
        self.localidad = localidad

    def __repr__(self):
        return str.upper('Seccional Nro ' + self.numero)

    def getMesas(self):
        mesas = []
        for cir in self.circuitos.all():
            mesas.extend(cir.getMesas())
        return mesas


class Circuito(db.Model):

    """docstring for Circuito"""

    __tablename__ = "Circuito"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20))
    seccional_id = db.Column(db.Integer, db.ForeignKey('Seccional.id'))
    seccional = db.relationship('Seccional', backref=db.backref(
        'circuitos', lazy='dynamic'))
    #propiedad 'escuelas' para obtener sus hijas

    def __init__(self, descripcion='', seccional=''):
        self.descripcion = descripcion
        self.seccional = seccional

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        mesas = []
        for esc in self.escuelas.all():
            mesas.extend(esc.getMesas())
        return mesas


class Escuela(db.Model):

    """docstring for Escuela"""

    __tablename__ = "Escuela"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20), unique=True)
    circuito_id = db.Column(db.Integer, db.ForeignKey('Circuito.id'))
    circuito = db.relationship('Circuito', backref=db.backref(
        'escuelas', lazy='dynamic'))
    #propiedad 'mesas' para obtener sus hijas

    def __init__(self, descripcion='', circuito=''):
        self.descripcion = descripcion
        self.circuito = circuito

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        return self.mesas.all()


class Mesa(db.Model):

    """docstring for Mesa"""

    __tablename__ = "Mesa"
    numero = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20))
    escuela_id = db.Column(db.Integer, db.ForeignKey('Escuela.id'))
    escuela = db.relationship('Escuela', backref=db.backref(
        'mesas', lazy='dynamic'))

    def __init__(self, numero='', descripcion='', escuela=''):
        self.numero = numero
        self.descripcion = descripcion
        self.escuela = escuela

    def __repr__(self):
        return str.upper('Mesa Nro: ' + str(self.numero))


class TipoCargo(Enum):

    """docstring for TipoCargo"""

    Cargo_Local = 1
    Cargo_Departamental = 2
    Cargo_Provincial = 3
    Cargo_Nacional = 4


class Frente(db.Model):

    """docstring for Localidad"""

    __tablename__ = "Frente"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    #propiedad 'listas' para obtener sus hijas

    def __init__(self, descripcion=''):
        self.descripcion = descripcion

    def __repr__(self):
        return str.upper(self.descripcion)


class Lista(db.Model):

    """docstring for Lista"""

    __tablename__ = "Lista"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    frente_id = db.Column(db.Integer, db.ForeignKey('Frente.id'))
    frente = db.relationship('Frente', backref=db.backref(
        'listas', lazy='dynamic'))
    cargo_id = db.Column(db.Integer, db.ForeignKey('Cargo.id'))
    cargo = db.relationship('Cargo', backref=db.backref(
        'listas', lazy='dynamic'))

    def __init__(self, descripcion='', frente='', cargo=''):
        self.descripcion = descripcion
        self.frente = frente
        self.cargo = cargo

    def __repr__(self):
        return str.upper(self.frente.descripcion + ' - ' + self.descripcion)


class Cargo(db.Model):

    """docstring for Cargo"""

    __tablename__ = "Cargo"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    #propiedad 'listas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': 'Cargo',
        'polymorphic_on': type
    }


class Cargo_Local(Cargo):

    """docstring for Cargo_Local"""

    __tablename__ = TipoCargo.Cargo_Local.name
    id = db.Column(db.Integer, db.ForeignKey('Cargo.id'), primary_key=True)
    descripcion = db.Column(db.String(50))
    localidad_id = db.Column(db.Integer, db.ForeignKey('Localidad.id'))
    localidad = db.relationship('Localidad', backref=db.backref(
        'cargos', lazy='dynamic'))
    #propiedad 'listas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': TipoCargo.Cargo_Local.name,
    }

    def __init__(self, descripcion='', localidad=''):
        super(Cargo_Local, self).__init__()
        self.descripcion = descripcion
        self.localidad = localidad

    def __repr__(self):
        return str.upper(self.descripcion + ' - ' + self.localidad.descripcion)


class Cargo_Departamental(Cargo):

    """docstring for Cargo_Departamental"""

    __tablename__ = TipoCargo.Cargo_Departamental.name
    id = db.Column(db.Integer, db.ForeignKey('Cargo.id'), primary_key=True)
    descripcion = db.Column(db.String(50))
    departamento_id = db.Column(db.Integer, db.ForeignKey('Departamento.id'))
    departamento = db.relationship('Departamento', backref=db.backref(
        'cargos', lazy='dynamic'))
    #propiedad 'listas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': TipoCargo.Cargo_Departamental.name,
    }

    def __init__(self, descripcion='', departamento=''):
        self.descripcion = descripcion
        self.departamento = departamento

    def __repr__(self):
        return str.upper(self.descripcion +
                         ' - ' + self.departamento.descripcion)


class Cargo_Provincial(Cargo):

    """docstring for Cargo_Provincial"""

    __tablename__ = TipoCargo.Cargo_Provincial.name
    id = db.Column(db.Integer, db.ForeignKey('Cargo.id'), primary_key=True)
    descripcion = db.Column(db.String(50))
    provincia_id = db.Column(db.Integer, db.ForeignKey('Provincia.id'))
    provincia = db.relationship('Provincia', backref=db.backref(
        'cargos', lazy='dynamic'))
    #propiedad 'listas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': TipoCargo.Cargo_Provincial.name,
    }

    def __init__(self, descripcion='', provincia=''):
        self.descripcion = descripcion
        self.provincia = provincia

    def __repr__(self):
        return str.upper(self.descripcion + ' - ' + self.provincia.descripcion)
####TODO
######## CARGOS_NACIONALES


class PlanillaMesa(db.Model):

    """docstring for PlanillaMesa"""

    __tablename__ = "PlanillaMesa"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    mesa_numero = db.Column(db.Integer, db.ForeignKey('Mesa.numero'))
    mesa = db.relationship('Mesa', backref=db.backref(
        'planillas', lazy='dynamic'))
    cargo_id = db.Column(db.Integer, db.ForeignKey('Cargo.id'))
    cargo = db.relationship('Cargo', backref=db.backref(
        'planillas', lazy='dynamic'))

    def __init__(self, descripcion='', mesa='', cargo=''):
        self.descripcion = descripcion
        self.mesa = mesa
        self.cargo = cargo

    def __repr__(self):
        return str.upper('Planilla de mesa ' +
                         self.mesa.numero + ' - ' + self.cargo.descripcion)


class VotoListaMesa(db.Model):

    """docstring for Lista"""

    __tablename__ = "VotoListaMesa"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    planilla_mesa_id = db.Column(
        db.Integer, db.ForeignKey('PlanillaMesa.id'))
    planilla_mesa = db.relationship('PlanillaMesa', backref=db.backref(
        'listas', lazy='dynamic'))
    lista_id = db.Column(db.Integer, db.ForeignKey('Lista.id'))
    lista = db.relationship('Lista', backref=db.backref(
        'votos', lazy='dynamic'))

    def __init__(self, descripcion='', mesa='', cargo=''):
        self.descripcion = descripcion
        self.mesa = mesa
        self.cargo = cargo

    def __repr__(self):
        return str.upper('Votos de mesa ' +
                         self.mesa.numero + ': ' + self.descripcion)
