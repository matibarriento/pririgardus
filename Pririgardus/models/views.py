# models.view.py
from wtforms import (
    Form, IntegerField, FieldList, FormField, HiddenField,
    TextField, PasswordField)
from flask.ext.admin import BaseView, expose, AdminIndexView
from flask.ext.admin.actions import action
from flask.ext.login import current_user
# from flask.ext.admin.model import BaseModelView
from flask.ext.admin.contrib.sqla import ModelView
# from wtforms.validators import InputRequired, NumberRange
from models.utils import VOTO_NAME_PREFIX, UsuarioInvalido, PasswordInvalida
from models.models import (db, PlanillaMesa, Cargo, TipoCargo,
                           Usuario, Roles, Lista, ListaCargo)


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class DatosMesa(object):

    """docstring for DatosMesa"""

    def __init__(self, mesa, todas=True):
        super(DatosMesa, self).__init__()
        self.mesa_numero = mesa.numero
        self.circuito = repr(mesa.escuela.circuito)
        self.escuela = repr(mesa.escuela)
        if todas:
            self.planillas = [BotonPlanilla(planilla)
                              for planilla in mesa.planillas]
        else:
            self.planillas = [BotonPlanilla(planilla)
                              for planilla in mesa.planillas
                              if planilla.escrutada is False]


class BotonPlanilla(object):

    """docstring for BotonPlanilla"""

    def __init__(self, planilla):
        super(BotonPlanilla, self).__init__()
        self.id = planilla.id
        self.texto = planilla.cargo.tipo_cargo.descripcion
        self.habilitado = not planilla.escrutada


class VotoLista(Form):

    """docstring for VotoLista"""
    voto = IntegerField(default=0)

    def __init__(self, votolista):
        super(VotoLista, self).__init__(obj=votolista)
        self.voto.name = VOTO_NAME_PREFIX + str(votolista.id)
        self.voto.label = "{0} - {1}".format(
            votolista.lista.lista.id, votolista.lista.lista.descripcion)
        self.voto.data = votolista.votos


class VotoFrente(Form):

    """docstring for VotoFrente"""

    votos_listas = FieldList(
        FormField(VotoLista, default=lambda: AttrDict(voto='')))

    def __init__(self, frente, planilla):
        super(VotoFrente, self).__init__(obj=frente)
        self.frente = "{0} - {1}".format(frente.id, frente.descripcion)
        self.clase = frente.id
        for votolista in planilla.votos.join(ListaCargo).join(Lista).order_by(
                Lista.id):
            if votolista.lista.lista.frente == frente:
                self.votos_listas.entries.append(VotoLista(votolista))


class CargarPlanilla(Form):

    """docstring for CargarPlanilla"""
    planilla_id = HiddenField()
    nulos = IntegerField(label="Votos Nulos", default=0)
    blancos = IntegerField(label="Votos Blancos", default=0)
    impugnados = IntegerField(label="Votos Impugnados", default=0)
    recurridos = IntegerField(label="Votos Recurridos", default=0)
    votos_frentes = FieldList(
        FormField(VotoFrente, default=lambda: AttrDict(lista='')))

    def __init__(self, planilla):
        super(CargarPlanilla, self).__init__(obj=planilla)
        self.planilla_id.data = planilla.id
        self.mesa_numero = planilla.mesa.numero
        self.titulo = "{0} {1}".format(
            str.upper(planilla.mesa.escuela.descripcion),
            repr(planilla.mesa.escuela.circuito))
        self.cargo = repr(planilla.cargo.tipo_cargo)
        self.cargo_id = planilla.cargo_id
        self.nulos.data = planilla.nulos
        self.blancos.data = planilla.blancos
        self.impugnados.data = planilla.impugnados
        self.recurridos.data = planilla.recurridos
        for frente in planilla.getFrentes():
            if (
                frente in current_user.frentes or
                    len(current_user.frentes) == 0):
                self.votos_frentes.entries.append(VotoFrente(frente, planilla))
        # for votolista in planilla.votos.join(Lista).order_by(
        #         Lista.posicionFrente, Lista.posicionLista).all():
        #     self.votos_listas.entries.append(VotoLista(votolista))
        self.escrutada = planilla.escrutada


class Administrador(AdminIndexView):

    """docstring for Administrador"""

    @expose('/')
    def index(self):
        return self.render('/admin')

    def is_accessible(self):
        return current_user.tieneRol(Roles.Administrador)

    def __init__(self, name=None, category=None,
                 endpoint=None, url=None,
                 template='admin/index.html'):
        super(Administrador, self).__init__(name=name, category=category,
                                            endpoint=endpoint, url=url,
                                            template=template)
        self.name = name
        self.category = category
        self.endpoint = endpoint
        self.url = url
        self.template = template


class Exportar(BaseView):

    @expose('/')
    def index(self):
        tiposCargo = db.session.query(TipoCargo).join(
            TipoCargo.cargos).order_by(Cargo.id.desc()).all()
        return self.render('exportar.html', tiposCargo=tiposCargo)

    def is_accessible(self):
        return (current_user.tieneRol(Roles.Administrador) and
                current_user.is_authenticated())


class UsuarioMV(ModelView):

    # column_exclude_list = ("contraseña")

    column_list = ("usuario", "roles", "frentes")

    column_display_all_relations = True

    @action("borrarFrentes", "Borrar Frentes")
    def borrarFrentes(self, listID):
        for usu in listID:
            usuario = db.session.query(Usuario).filter(
                Usuario.id == usu).first()
            if usuario:
                for fren in usuario.frentes:
                    usuario.frentes.remove(fren)
        db.session.commit()

    def is_accessible(self):
        return (current_user.tieneRol(Roles.Administrador) and
                current_user.is_authenticated())

    def __init__(self, session, **kwargs):
        super(UsuarioMV, self).__init__(Usuario, session, **kwargs)


class PlanillaMV(ModelView):
    can_create = False
    can_delete = False
    can_edit = False

    column_sortable_list = (
        ('mesa', PlanillaMesa.mesa_numero),
        ('cargo', PlanillaMesa.cargo_id),
        ('escrutada', PlanillaMesa.escrutada)
    )

    column_exclude_list = ("nulos", "blancos", "impugnados", "recurridos")

    column_filters = ('mesa_numero', 'escrutada')

    form_widget_args = {
        'mesa': {
            'disabled': True
        },
        'cargo': {
            'disabled': True
        }
    }

    form_excluded_columns = (
        'nulos', 'blancos', 'impugnados', 'recurridos', 'votos')

    @action("Desescrutar", "Desescrutar")
    def desescrutar(self, listID):
        for planilla_id in listID:
            planilla = db.session.query(PlanillaMesa).filter(
                PlanillaMesa.id == planilla_id).first()
            if planilla:
                planilla.escrutada = False
                db.session.add(planilla)
        db.session.commit()

    def is_accessible(self):
        return (current_user.tieneRol(Roles.Administrador) and
                current_user.is_authenticated())

    def __init__(self, session, **kwargs):
        super(PlanillaMV, self).__init__(PlanillaMesa, session, **kwargs)


class LoginForm(Form):

    usuario = TextField()
    password = PasswordField()

    def validate_login(self):
        usuario = self.get_user()
        if usuario is None:
            raise UsuarioInvalido("El usuario no existe")
        if not usuario.contraseña == self.password.data:
            raise PasswordInvalida("La contraseña es incorrecta")

    def get_user(self):
        return db.session.query(Usuario).filter(
            Usuario.usuario == self.usuario.data).first()


class MesaExportada(object):

    """docstring for MesaExportada"""

    def __init__(self, numeroMesa):
        super(MesaExportada, self).__init__()
        self.numeroMesa = numeroMesa
        self.listas = []
        self.cargos = []


class CargosMesa(object):

    """docstring for CargosMesa"""

    def __init__(self, descripcion):
        super(CargosMesa, self).__init__()
        self.descripcion = descripcion
        self.votoListas = []
