# models.models.py
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
from enum import Enum

db = SQLAlchemy()


class Pais(db.Model):

    """docstring for Pais"""

    __tablename__ = "Pais"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20), unique=True)
    # propiedad 'provincias' para obtener sus hijas

    def __init__(self, descripcion=None):
        self.descripcion = descripcion

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        return db.session.query(
            Mesa).join(Escuela).join(Circuito).join(Seccional).join(
            Localidad).join(Departamento).join(Provincia).join(Pais).filter(
            Provincia.pais == self).all()

    def getNumerosMesas(self):
        return [m[0] for m in db.session.query(Mesa.numero).join(
            Escuela).join(Circuito).join(Seccional).join(
            Localidad).join(Departamento).join(Provincia).join(Pais).filter(
            Provincia.pais == self).all()]


class Provincia(db.Model):

    """docstring for Provincia"""

    __tablename__ = "Provincia"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20), unique=True)
    pais_id = db.Column(db.Integer, db.ForeignKey('Pais.id'))
    pais = db.relationship('Pais', backref=db.backref(
                           'provincias', lazy='dynamic'))
    # propiedad 'departamentos' para obtener sus hijas

    def __init__(self, descripcion=None, pais=None):
        self.descripcion = descripcion
        self.pais = pais

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        return db.session.query(
            Mesa).join(Escuela).join(Circuito).join(Seccional).join(
            Localidad).join(Departamento).join(Provincia).filter(
            Departamento.provincia == self).all()

    def getNumerosMesas(self):
        return [m[0] for m in db.session.query(Mesa.numero).join(
            Escuela).join(Circuito).join(Seccional).join(
            Localidad).join(Departamento).join(Provincia).filter(
            Departamento.provincia == self).all()]


class Departamento(db.Model):

    """docstring for Departamento"""

    __tablename__ = "Departamento"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    provincia_id = db.Column(db.Integer, db.ForeignKey('Provincia.id'))
    provincia = db.relationship('Provincia', backref=db.backref(
        'departamentos', lazy='dynamic'))
    # propiedad 'localidades' para obtener sus hijas

    def __init__(self, descripcion=None, provincia=None):
        self.descripcion = descripcion
        self.provincia = provincia

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        return db.session.query(
            Mesa).join(Escuela).join(Circuito).join(Seccional).join(
            Localidad).join(Departamento).filter(
            Localidad.departamento == self).all()

    def getNumerosMesas(self):
        return [m[0] for m in db.session.query(Mesa.numero).join(
            Escuela).join(Circuito).join(Seccional).join(
            Localidad).join(Departamento).filter(
            Localidad.departamento == self).all()]

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

    def __init__(self, descripcion=None, departamento=None):
        self.descripcion = descripcion
        self.departamento = departamento

    def __repr__(self):
        return str.upper(self.descripcion)

    def getMesas(self):
        return db.session.query(
            Mesa).join(Escuela).join(Circuito).join(Seccional).join(
            Localidad).filter(Seccional.localidad == self).all()

    def getNumerosMesas(self):
        return [m[0] for m in db.session.query(Mesa.numero).join(
            Escuela).join(Circuito).join(Seccional).join(
            Localidad).filter(Seccional.localidad == self).all()]

    def getFullRepr(self):
        return "{0} - {1}".format(
            self.descripcion, self.departamento.provincia.descripcion)


class Seccional(db.Model):

    """docstring for Seccional"""

    __tablename__ = "Seccional"
    # id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), primary_key=True)
    localidad_id = db.Column(db.Integer, db.ForeignKey('Localidad.id'))
    localidad = db.relationship('Localidad', backref=db.backref(
        'seccionales', lazy='dynamic'))
    # propiedad 'circuitos' para obtener sus hijas

    def __init__(self, numero=None, localidad=None):
        self.numero = numero
        self.localidad = localidad

    def __repr__(self):
        return str.upper(
            'SEC.{0} - {1}'.format(self.numero, self.localidad))

    def getMesas(self):
        return db.session.query(
            Mesa).join(Escuela).join(Circuito).join(Seccional).filter(
            Circuito.seccional == self).all()

    def getNumerosMesas(self):
        return [m[0] for m in db.session.query(Mesa.numero).join(
            Escuela).join(Circuito).join(Seccional).filter(
            Circuito.seccional == self).all()]


class Circuito(db.Model):

    """docstring for Circuito"""

    __tablename__ = "Circuito"
    # id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), primary_key=True)
    seccional_id = db.Column(db.String(10), db.ForeignKey('Seccional.numero'))
    seccional = db.relationship('Seccional', backref=db.backref(
        'circuitos', lazy='dynamic'))
    # propiedad 'escuelas' para obtener sus hijas

    def __init__(self, numero=None, numSeccional=None):
        self.numero = numero
        self.seccional_id = numSeccional

    def __repr__(self):
        return str.upper(
            'Circuito {0} - {1}'.format(self.numero, self.seccional))

    def getMesas(self):
        return db.session.query(
            Mesa).join(Escuela).join(Circuito).filter(
            Escuela.circuito == self).all()

    def getNumerosMesas(self):
        return [m[0] for m in db.session.query(Mesa.numero).join(
            Escuela).join(Circuito).filter(
            Escuela.circuito == self).all()]


class Escuela(db.Model):

    """docstring for Escuela"""

    __tablename__ = "Escuela"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20))
    circuito_id = db.Column(db.Integer, db.ForeignKey('Circuito.numero'))
    circuito = db.relationship('Circuito', backref=db.backref(
        'escuelas', lazy='dynamic'))
    # propiedad 'mesas' para obtener sus hijas

    def __init__(self, descripcion=None, numCircuito=None,
                 mesaDesde=None, mesaHasta=None):
        self.descripcion = descripcion
        self.circuito_id = numCircuito
        self.CrearMesas(mesaDesde, mesaHasta)

    def __repr__(self):
        return str.upper('Escuela {0} - {1}'.format(
                         self.descripcion,
                         self.circuito))

    def getMesas(self):
        return self.mesas.all()

    def getNumerosMesas(self):
        return [m[0] for m in db.session.query(Mesa.numero).join(
            Escuela).filter(
            Mesa.escuela == self).all()]

    def CrearMesas(self, mesaDesde, mesaHasta):
        for mesanum in range(mesaDesde, mesaHasta + 1):
            db.session.add(Mesa(mesanum, self))


class Mesa(db.Model):

    """docstring for Mesa"""

    __tablename__ = "Mesa"
    numero = db.Column(db.Integer, primary_key=True)
    escuela_id = db.Column(db.Integer, db.ForeignKey('Escuela.id'))
    escuela = db.relationship('Escuela', backref=db.backref(
        'mesas', lazy='dynamic'))
    # propiedad 'planillas' para obtener sus hijas

    def __init__(self, numero=None, escuela=None):
        self.numero = numero
        self.escuela = escuela

    def __repr__(self):
        return str(self.numero)

    def Actualizar_Planillas(self):
        cargos_mesa = db.session.query(Cargo).outerjoin(
                           PlanillaMesa).filter(
                           PlanillaMesa.mesa == self)
        cargos_faltantes = [cargo for cargo in self.getCargos()
                            if cargo not in cargos_mesa]

        if(len(cargos_faltantes) > 0):
            planillaCargo = [{
                    'mesa_numero': self.numero,
                    'cargo_id': cargo.id} for cargo in cargos_faltantes]
            db.session.execute(db.insert(PlanillaMesa), planillaCargo)
            db.session.commit()

    def getCargos(self):
        cargos = []
        localidad = self.escuela.circuito.seccional.localidad
        for lugar in [localidad.departamento.provincia.pais,
                      localidad.departamento.provincia,
                      localidad.departamento,
                      localidad
                      ]:
            cargos.extend(lugar.cargos.all())
        return cargos

    def getIDCargos(self):
        cargos = self.getCargos()
        return [cargo.id for cargo in cargos]

    def estaEscrutada(self):
        for planilla in self.planillas:
            if planilla.escrutada is False:
                return False
        return True


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

    def __init__(self, descripcion=None, alcance_cargo=None):
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

    def __init__(self, id=None, descripcion=None):
        if(id):
            self.id = int(id)
        self.descripcion = descripcion

    def __repr__(self):
        return str.upper(self.descripcion)

    def Votos_Frente(self, cargo_id):
        total = db.session.query(func.sum(
                VotoListaMesa.votos)).join(
                ListaCargo).join(
                Lista).join(
                Frente).filter(
                Frente.id == self.id,
                ListaCargo.cargo_id == cargo_id).scalar()
        return total


class Lista(db.Model):

    """docstring for Lista"""

    __tablename__ = "Lista"
    id = db.Column(db.String(10), primary_key=True)
    descripcion = db.Column(db.String(50))
    frente_id = db.Column(db.Integer, db.ForeignKey('Frente.id'))
    frente = db.relationship('Frente', backref=db.backref(
        'listas', lazy='dynamic'))
    # propidad 'cargos' para obtener sus hijos

    def __init__(self, id=None, descripcion=None, idFrente=None, frente=None):
        if(id):
            self.id = id
        self.descripcion = descripcion
        if idFrente:
            self.frente_id = idFrente
        else:
            self.frente = frente

    def __repr__(self):
        return str.upper(self.frente.descripcion + ' - ' + self.descripcion)

    def Votos_Lista(self, cargo_id):
        total = db.session.query(func.sum(
                VotoListaMesa.votos)).join(
                ListaCargo).join(
                Lista).filter(
                Lista.id == self.id,
                ListaCargo.cargo_id == cargo_id).scalar()
        return total


class ListaCargo(db.Model):

    """docstring for ListaCargo"""

    __tablename__ = "ListaCargo"
    id = db.Column(db.Integer, primary_key=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey('Cargo.id'))
    cargo = db.relationship('Cargo', backref=db.backref(
        'listas', lazy='dynamic'))
    lista_id = db.Column(db.String(10), db.ForeignKey('Lista.id'))
    lista = db.relationship('Lista', backref=db.backref(
        'cargos', lazy='dynamic'))
    candidato_principal = db.Column(db.String(50))
    # propidad 'votos' para obtener sus hijos

    def __init__(self, idLista=None, cargo=None,
                 candidatoPrincipal=None, lista=None):
        self.cargo = cargo
        if idLista:
            self.lista_id = idLista
        else:
            self.lista = lista
        self.candidato_principal = candidatoPrincipal

    def __repr__(self):
        return str.upper("{0} - {1}".format(
            self.lista.descripcion, self.cargo.descripcion))

    def Votos_Lista(self):
        total = 0
        for voto in self.votos:
            total += voto.votos
        return total

    def Actualizar_VotoLista(self):
        mesas = self.cargo.alcance.getNumerosMesas()
        # planillas de la mesa
        planillas = db.session.query(PlanillaMesa).filter(
            PlanillaMesa.mesa_numero.in_(mesas),
            PlanillaMesa.cargo == self.cargo)
        # planillas que no tienen el VotoLista
        planillas = planillas.except_(
            planillas.outerjoin(
                VotoListaMesa).filter(
                VotoListaMesa.lista == self))
        if(planillas.count() > 0):
            # VotoLista a crear
            votoLista = [{
                    'planilla_mesa_id': planilla.id,
                    'lista_id': self.id,
                    'descripcion': repr(self)} for planilla in planillas]
            db.session.execute(db.insert(VotoListaMesa), votoLista)
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

    def __init__(self, tipo_cargo=None):
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

    def __init__(self, localidad=None, tipo_cargo=None):
        super(Cargo_Local, self).__init__(tipo_cargo)
        self.alcance = localidad
        self.descripcion = str.upper(self.tipo_cargo.descripcion +
                                     ' - ' + self.alcance.descripcion)

    def __repr__(self):
        return self.descripcion


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

    def __init__(self, departamento=None, tipo_cargo=None):
        super(Cargo_Departamental, self).__init__(tipo_cargo)
        self.alcance = departamento
        self.descripcion = str.upper(self.tipo_cargo.descripcion +
                                     ' - ' + self.alcance.descripcion)

    def __repr__(self):
        return self.descripcion


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

    def __init__(self, provincia=None, tipo_cargo=None):
        super(Cargo_Provincial, self).__init__(tipo_cargo)
        self.alcance = provincia
        self.descripcion = str.upper(self.tipo_cargo.descripcion +
                                     ' - ' + self.alcance.descripcion)

    def __repr__(self):
        return self.descripcion


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

    def __init__(self, pais=None, tipo_cargo=None):
        super(Cargo_Nacional, self).__init__(tipo_cargo)
        self.alcance = pais
        self.descripcion = str.upper(self.tipo_cargo.descripcion +
                                     ' - ' + self.alcance.descripcion)

    def __repr__(self):
        return self.descripcion


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

    def __init__(self, mesa=None, cargo=None):
        self.mesa = mesa
        self.cargo = cargo

    def __repr__(self):
        return str.upper('Planilla de mesa ' +
                         str(self.mesa.numero) +
                         ' - ' + self.cargo.descripcion)

    def Total_Votos(self):
        total = self.nulos + self.blancos + self.impugnados + self.recurridos
        for voto in self.votos:
            total += voto.votos
        return total

    def Total_Votos_Afirmativos_Validos(self):
        total = 0
        for voto in self.votos:
            total += voto.votos
        return total

    def Total_Votos_Validos(self):
        total = self.blancos
        for voto in self.votos:
            total += voto.votos
        return total

    def getFrentes(self):
        frentes = []
        [frentes.append(voto.lista.lista.frente)
            for voto in self.votos.join(
                                        ListaCargo).join(
                                        Lista).order_by(
                                        Lista.id)
            if voto.lista.lista.frente not in frentes and
            voto.lista.lista.frente is not None]

        return frentes


class VotoListaMesa(db.Model):

    """docstring for VotoListaMesa"""

    __tablename__ = "VotoListaMesa"
    id = db.Column(db.Integer, primary_key=True)
    votos = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.String(100))
    planilla_mesa_id = db.Column(
        db.Integer, db.ForeignKey('PlanillaMesa.id'))
    planilla_mesa = db.relationship('PlanillaMesa', backref=db.backref(
        'votos', lazy='dynamic'))
    lista_id = db.Column(db.String(10), db.ForeignKey('ListaCargo.id'))
    lista = db.relationship('ListaCargo', backref=db.backref(
        'votos', lazy='dynamic'))

    def __init__(self, planilla=None, lista=None):
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
    otros_votos = db.Column(db.Boolean, default=True)

    def __init__(self, usuario=None, passw=None):
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

    def __init__(self, rol=None):
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


#############################################################################

# PARA INICIALIZAR

def Actualizar_Todas_Planillas():
    planillas_faltantes = []
    for mesa in Mesa.query.all():
        cargos_mesa = db.session.query(Cargo).outerjoin(
                           PlanillaMesa).filter(
                           PlanillaMesa.mesa == mesa)
        cargos_faltantes = [cargo for cargo in mesa.getCargos()
                            if cargo not in cargos_mesa]

        if(len(cargos_faltantes) > 0):
            planillaCargo = [{
                    'mesa_numero': mesa.numero,
                    'cargo_id': cargo.id} for cargo in cargos_faltantes]
            planillas_faltantes.extend(planillaCargo)
    db.session.execute(db.insert(PlanillaMesa), planillas_faltantes)
    db.session.commit()


def Actualizar_Todos_VotoLista():
    votoslistas_faltante = []
    for listacargo in ListaCargo.query.all():
        mesas = listacargo.cargo.alcance.getNumerosMesas()
        # planillas de la mesa
        planillas = db.session.query(PlanillaMesa).filter(
            PlanillaMesa.mesa_numero.in_(mesas),
            PlanillaMesa.cargo == listacargo.cargo)
        # planillas que no tienen el VotoLista
        planillas = planillas.except_(
            planillas.outerjoin(
                VotoListaMesa).filter(
                VotoListaMesa.lista == listacargo))
        if(planillas.count() > 0):
            # VotoLista a crear
            votoLista = [{
                    'planilla_mesa_id': planilla.id,
                    'lista_id': listacargo.id,
                    'descripcion': repr(listacargo)} for planilla in planillas]
            votoslistas_faltante.extend(votoLista)
    db.session.execute(db.insert(VotoListaMesa), votoslistas_faltante)
    db.session.commit()