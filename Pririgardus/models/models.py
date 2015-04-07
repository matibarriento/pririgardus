#models.models.py
from flask.ext.sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()


class Pais(db.Model):

    """docstring for Pais"""

    __tablename__ = "Pais"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20), unique=True)
    # propiedad 'provincias' para obtener sus hijas

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
    # propiedad 'departamentos' para obtener sus hijas

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
    # propiedad 'localidades' para obtener sus hijas

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

    def getFullRepr(self):
        return "{0} - {1}".format(self.provincia.descripcion, self.descripcion)


class Localidad(db.Model):

    """docstring for Localidad"""

    __tablename__ = "Localidad"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    departamento_id = db.Column(db.Integer, db.ForeignKey('Departamento.id'))
    departamento = db.relationship('Departamento', backref=db.backref(
        'localidades', lazy='dynamic'))
    # propiedad 'seccionales' para obtener sus hijas

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

    def getFullRepr(self):
        return "{0} - {1}".format(
            self.departamento.provincia.descripcion, self.descripcion)


class Seccional(db.Model):

    """docstring for Seccional"""

    __tablename__ = "Seccional"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20))
    localidad_id = db.Column(db.Integer, db.ForeignKey('Localidad.id'))
    localidad = db.relationship('Localidad', backref=db.backref(
        'seccionales', lazy='dynamic'))
    # propiedad 'circuitos' para obtener sus hijas

    def __init__(self, numero='', localidad=''):
        self.numero = numero
        self.localidad = localidad

    def __repr__(self):
        return str.upper(
            'Seccional Nro {0} - {1}'.format(self.numero, self.localidad))

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
    # propiedad 'escuelas' para obtener sus hijas

    def __init__(self, descripcion='', seccional=''):
        self.descripcion = descripcion
        self.seccional = seccional

    def __repr__(self):
        return str.upper(
            'Circuito {0} - {1}'.format(self.descripcion, self.seccional))

    def getMesas(self):
        mesas = []
        for esc in self.escuelas.all():
            mesas.extend(esc.getMesas())
        return mesas


class Escuela(db.Model):

    """docstring for Escuela"""

    __tablename__ = "Escuela"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20))
    circuito_id = db.Column(db.Integer, db.ForeignKey('Circuito.id'))
    circuito = db.relationship('Circuito', backref=db.backref(
        'escuelas', lazy='dynamic'))
    # propiedad 'mesas' para obtener sus hijas

    def __init__(self, descripcion='', circuito=''):
        self.descripcion = descripcion
        self.circuito = circuito

    def __repr__(self):
        return str.upper('Escuela {0} - {1}'.format(
                         self.descripcion,
                         self.circuito.seccional.localidad.descripcion))

    def getMesas(self):
        return self.mesas.all()


class Mesa(db.Model):

    """docstring for Mesa"""

    __tablename__ = "Mesa"
    numero = db.Column(db.Integer, primary_key=True)
    escuela_id = db.Column(db.Integer, db.ForeignKey('Escuela.id'))
    escuela = db.relationship('Escuela', backref=db.backref(
        'mesas', lazy='dynamic'))
    # propiedad 'planillas' para obtener sus hijas

    def __init__(self, numero='', escuela=''):
        self.numero = numero
        self.escuela = escuela
        self.Actualizar_Planillas()

    def __repr__(self):
        return str(self.numero)

    def Actualizar_Planillas(self):
        cargos = self.getCargos()
        if(len(cargos) > 0):
            for cargo in cargos:
                planilla = db.session.query(
                    PlanillaMesa).filter(
                    PlanillaMesa.mesa == self,
                    PlanillaMesa.cargo == cargo).first()
                if not planilla:
                    db.session.add(PlanillaMesa(mesa=self, cargo=cargo))

    def getCargos(self):
        cargos = []
        localidad = self.escuela.circuito.seccional.localidad
        for lugar in [localidad,
                      localidad.departamento,
                      localidad.departamento.provincia,
                      localidad.departamento.provincia.pais]:
            cargos.extend(lugar.cargos)
        return cargos


class AlcanceCargo(Enum):

    """docstring for AlcanceCargo"""

    Cargo_Local = 1
    Cargo_Departamental = 2
    Cargo_Provincial = 3
    Cargo_Nacional = 4


class TipoCargo(db.Model):

    """docstring for TipoCargo"""

    __tablename__ = "TipoCargo"
    id = db.Column(db.Integer, primary_key=True)
    alcance_cargo = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    # propiedad 'cargos' para obtener sus hijas

    def __init__(self, descripcion='', alcance_cargo=''):
        self.descripcion = descripcion
        try:
            self.alcance_cargo = alcance_cargo.name
        except KeyError:
            raise Exception

    def __repr__(self):
        return str.upper(self.descripcion)


class Frente(db.Model):

    """docstring for Localidad"""

    __tablename__ = "Frente"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    # propiedad 'listas' para obtener sus hijas

    def __init__(self, id=None, descripcion=''):
        if(id):
            self.id = int(id)
        self.descripcion = descripcion

    def __repr__(self):
        return str.upper(self.descripcion)

    def Votos_Frente(self, cargo_id):
        total = 0
        for lista in self.listas:
            if lista.cargo_id == cargo_id:
                total += lista.Votos_Lista()
        return total


class Lista(db.Model):

    """docstring for Lista"""

    __tablename__ = "Lista"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    posicionFrente = db.Column(db.Integer)
    posicionLista = db.Column(db.Integer)
    frente_id = db.Column(db.Integer, db.ForeignKey('Frente.id'))
    frente = db.relationship('Frente', backref=db.backref(
        'listas', lazy='dynamic'))
    cargo_id = db.Column(db.Integer, db.ForeignKey('Cargo.id'))
    cargo = db.relationship('Cargo', backref=db.backref(
        'listas', lazy='dynamic'))
    # propidad 'votos' para obtener sus hijos

    def __init__(self, posicionFrente, posicionLista,
                 descripcion='', frente='', cargo=''):
        self.posicionFrente = int(posicionFrente)
        self.posicionLista = int(posicionLista)
        self.descripcion = descripcion
        self.frente = frente
        self.cargo = cargo
        self.Actualizar_VotoLista()

    def __repr__(self):
        return str.upper(self.frente.descripcion + ' - ' + self.descripcion)

    def Votos_Lista(self):
        total = 0
        for voto in self.votos:
            total += voto.votos
        return total

    def Actualizar_VotoLista(self):
        mesas = self.cargo.alcance.getMesas()
        planillas = []
        if(len(mesas) > 0):
            for mesa in mesas:
                planilla = db.session.query(
                    PlanillaMesa).filter(
                    PlanillaMesa.mesa == mesa,
                    PlanillaMesa.cargo == self.cargo).first()
                if planilla:
                    planillas.append(planilla)
            if(len(planillas) > 0):
                for planilla in planillas:
                    votolista = db.session.query(
                        VotoListaMesa).filter(
                        VotoListaMesa.planilla_mesa == planilla,
                        VotoListaMesa.lista == self).first()
                    if not votolista:
                        db.session.add(
                            VotoListaMesa(planilla=planilla, lista=self))
                db.session.commit()


class Cargo(db.Model):

    """docstring for Cargo"""

    __tablename__ = "Cargo"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    tipo_cargo_id = db.Column(db.Integer, db.ForeignKey('TipoCargo.id'))
    tipo_cargo = db.relationship('TipoCargo', backref=db.backref(
        'cargos', lazy='dynamic'))
    # propiedad 'listas' para obtener sus hijas
    # propiedad 'planillas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': 'Cargo',
        'polymorphic_on': type
    }

    def __init__(self, tipo_cargo=''):
        self.tipo_cargo = tipo_cargo


class Cargo_Local(Cargo):

    """docstring for Cargo_Local"""

    __tablename__ = AlcanceCargo.Cargo_Local.name
    id = db.Column(db.Integer, db.ForeignKey('Cargo.id'), primary_key=True)
    descripcion = db.Column(db.String(100))
    alcance_id = db.Column(db.Integer, db.ForeignKey('Localidad.id'))
    alcance = db.relationship('Localidad', backref=db.backref(
        'cargos', lazy='dynamic'))
    # propiedad 'listas' para obtener sus hijas
    # propiedad 'planillas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': AlcanceCargo.Cargo_Local.name,
    }

    def __init__(self, localidad='', tipo_cargo=''):
        super(Cargo_Local, self).__init__(tipo_cargo)
        self.alcance = localidad
        self.descripcion = str.upper(self.tipo_cargo.descripcion
                                     + ' - ' + self.alcance.descripcion)
        self.Actualizar_Planillas()

    def __repr__(self):
        return self.descripcion

    def Actualizar_Planillas(self):
        #planillas = []
        mesas = self.alcance.getMesas()
        if(len(mesas) > 0):
            for mesa in mesas:
                planilla = db.session.query(
                    PlanillaMesa).filter(
                    PlanillaMesa.mesa == mesa,
                    PlanillaMesa.cargo == self).first()
                if not planilla:
                    db.session.add(PlanillaMesa(mesa=mesa, cargo=self))


class Cargo_Departamental(Cargo):

    """docstring for Cargo_Departamental"""

    __tablename__ = AlcanceCargo.Cargo_Departamental.name
    id = db.Column(db.Integer, db.ForeignKey('Cargo.id'), primary_key=True)
    descripcion = db.Column(db.String(100))
    alcance_id = db.Column(db.Integer, db.ForeignKey('Departamento.id'))
    alcance = db.relationship('Departamento', backref=db.backref(
        'cargos', lazy='dynamic'))
    # propiedad 'listas' para obtener sus hijas
    # propiedad 'planillas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': AlcanceCargo.Cargo_Departamental.name,
    }

    def __init__(self, departamento='', tipo_cargo=''):
        super(Cargo_Departamental, self).__init__(tipo_cargo)
        self.alcance = departamento
        self.descripcion = str.upper(self.tipo_cargo.descripcion
                                     + ' - ' + self.alcance.descripcion)
        self.Actualizar_Planillas()

    def __repr__(self):
        return self.descripcion

    def Actualizar_Planillas(self):
        #planillas = []
        mesas = self.alcance.getMesas()
        if(len(mesas) > 0):
            for mesa in mesas:
                planilla = db.session.query(
                    PlanillaMesa).filter(
                    PlanillaMesa.mesa == mesa,
                    PlanillaMesa.cargo == self).first()
                if not planilla:
                    db.session.add(PlanillaMesa(mesa=mesa, cargo=self))


class Cargo_Provincial(Cargo):

    """docstring for Cargo_Provincial"""

    __tablename__ = AlcanceCargo.Cargo_Provincial.name
    id = db.Column(db.Integer, db.ForeignKey('Cargo.id'), primary_key=True)
    descripcion = db.Column(db.String(100))
    alcance_id = db.Column(db.Integer, db.ForeignKey('Provincia.id'))
    alcance = db.relationship('Provincia', backref=db.backref(
        'cargos', lazy='dynamic'))
    # propiedad 'listas' para obtener sus hijas
    # propiedad 'planillas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': AlcanceCargo.Cargo_Provincial.name,
    }

    def __init__(self, provincia='', tipo_cargo=''):
        super(Cargo_Provincial, self).__init__(tipo_cargo)
        self.alcance = provincia
        self.descripcion = str.upper(self.tipo_cargo.descripcion
                                     + ' - ' + self.alcance.descripcion)
        self.Actualizar_Planillas()

    def __repr__(self):
        return self.descripcion

    def Actualizar_Planillas(self):
        mesas = self.alcance.getMesas()
        if(len(mesas) > 0):
            for mesa in mesas:
                planilla = db.session.query(
                    PlanillaMesa).filter(
                    PlanillaMesa.mesa == mesa,
                    PlanillaMesa.cargo == self).first()
                if not planilla:
                    db.session.add(PlanillaMesa(mesa=mesa, cargo=self))


class Cargo_Nacional(Cargo):

    """docstring for Cargo_Nacional"""

    __tablename__ = AlcanceCargo.Cargo_Nacional.name
    id = db.Column(db.Integer, db.ForeignKey('Cargo.id'), primary_key=True)
    descripcion = db.Column(db.String(100))
    alcance_id = db.Column(db.Integer, db.ForeignKey('Pais.id'))
    alcance = db.relationship('Pais', backref=db.backref(
        'cargos', lazy='dynamic'))
    # propiedad 'listas' para obtener sus hijas
    # propiedad 'planillas' para obtener sus hijas

    __mapper_args__ = {
        'polymorphic_identity': AlcanceCargo.Cargo_Nacional.name,
    }

    def __init__(self, pais='', tipo_cargo=''):
        super(Cargo_Nacional, self).__init__(tipo_cargo)
        self.alcance = pais
        self.descripcion = str.upper(self.tipo_cargo.descripcion
                                     + ' - ' + self.alcance.descripcion)
        self.Actualizar_Planillas()

    def __repr__(self):
        return self.descripcion

    def Actualizar_Planillas(self):
        mesas = self.alcance.getMesas()
        if(len(mesas) > 0):
            for mesa in mesas:
                planilla = db.session.query(
                    PlanillaMesa).filter(
                    PlanillaMesa.mesa == mesa,
                    PlanillaMesa.cargo == self).first()
                if not planilla:
                    db.session.add(PlanillaMesa(mesa=mesa, cargo=self))


class PlanillaMesa(db.Model):

    """docstring for PlanillaMesa"""

    __tablename__ = "PlanillaMesa"
    id = db.Column(db.Integer, primary_key=True)
    nulos = db.Column(db.Integer, default=0)
    blancos = db.Column(db.Integer, default=0)
    impugnados = db.Column(db.Integer, default=0)
    recurridos = db.Column(db.Integer, default=0)
    escrutada = db.Column(db.Boolean, default=False)
    mesa_numero = db.Column(db.Integer, db.ForeignKey('Mesa.numero'))
    mesa = db.relationship('Mesa', backref=db.backref(
        'planillas', lazy='dynamic'))
    cargo_id = db.Column(db.Integer, db.ForeignKey('Cargo.id'))
    cargo = db.relationship('Cargo', backref=db.backref(
        'planillas', lazy='dynamic'))
    # propiedad 'votos' para obtener sus hijas

    def __init__(self, mesa='', cargo=''):
        self.mesa = mesa
        self.cargo = cargo
        self.Actualizar_VotoLista()

    def __repr__(self):
        return str.upper('Planilla de mesa ' +
                         str(self.mesa.numero) +
                         ' - ' + self.cargo.descripcion)

    def Total_Votos(self):
        total = self.nulos + self.blancos + self.impugnados + self.recurridos
        for voto in self.votos:
            total += voto.votos
        return total

    def Total_Votos_Validos(self):
        total = self.blancos
        for voto in self.votos:
            total += voto.votos
        return total

    def Actualizar_VotoLista(self):
        listas = self.cargo.listas.all()
        if(len(listas) > 0):
            for lista in listas:
                votolista = db.session.query(
                    VotoListaMesa).filter(
                    VotoListaMesa.planilla_mesa == self).filter(
                    VotoListaMesa.lista == lista).first()
                if not votolista:
                    db.session.add(
                        VotoListaMesa(planilla=self, lista=lista))

    def getFrentes(self):
        frentes = []
        [frentes.append(voto.lista.frente)
            for voto in self.votos.join(Lista).order_by(Lista.posicionFrente)
            if voto.lista.frente not in frentes
            and voto.lista.frente is not None]

        return frentes


class VotoListaMesa(db.Model):

    """docstring for Lista"""

    __tablename__ = "VotoListaMesa"
    id = db.Column(db.Integer, primary_key=True)
    votos = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.String(100))
    planilla_mesa_id = db.Column(
        db.Integer, db.ForeignKey('PlanillaMesa.id'))
    planilla_mesa = db.relationship('PlanillaMesa', backref=db.backref(
        'votos', lazy='dynamic'))
    lista_id = db.Column(db.Integer, db.ForeignKey('Lista.id'))
    lista = db.relationship('Lista', backref=db.backref(
        'votos', lazy='dynamic'))

    def __init__(self, planilla='', lista=''):
        self.descripcion = repr(lista)
        self.planilla_mesa = planilla
        self.lista = lista

    def __repr__(self):
        return str.upper('Votos de {0}'.format(self.descripcion))


class Usuario(db.Model):

    """docstring for Usuario"""

    __tablename__ = "Usuario"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True)
    contraseña = db.Column(db.String(50))
    roles = db.relationship("Rol", secondary=lambda: UsuarioRoles)
    frentes = db.relationship(
        "Frente", secondary=lambda: UsuarioFrentes)

    def __init__(self, usuario='', passw=''):
        self.usuario = usuario
        self.contraseña = passw

    def __repr__(self):
        return self.usuario

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def tieneRol(self, rol):
        return rol.name in [r.descripcion for r in self.roles]


class Roles(Enum):

    """docstring for Roles"""

    Administrador = 1
    DataEntry = 2
    Prensa = 3


class Rol(db.Model):

    """docstring for Rol"""

    __tablename__ = "Rol"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), unique=True)

    def __init__(self, rol=''):
        try:
            self.id = rol.value
            self.descripcion = rol.name
        except KeyError:
            raise KeyError

    def __repr__(self):
        return self.descripcion


UsuarioRoles = db.Table(
    'UsuarioRoles', db.Model.metadata,
    db.Column('usuario_id',
              db.Integer,
              db.ForeignKey("Usuario.id"), primary_key=True),
    db.Column('rol_id',
              db.Integer,
              db.ForeignKey("Rol.id"), primary_key=True)
)

UsuarioFrentes = db.Table(
    'UsuarioFrentes', db.Model.metadata,
    db.Column('usuario_id',
              db.Integer,
              db.ForeignKey("Usuario.id"), primary_key=True),
    db.Column('frente_id',
              db.Integer,
              db.ForeignKey("Frente.id"), primary_key=True)
)
