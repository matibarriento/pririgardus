#models.view.py
from wtforms import (
    Form, IntegerField, FieldList, FormField, HiddenField, validators,
    TextField, PasswordField)
from flask.ext.admin import BaseView, expose, AdminIndexView
from flask.ext.admin.actions import action
from flask.ext.login import current_user
# from flask.ext.admin.model import BaseModelView
from flask.ext.admin.contrib.sqla import ModelView
#from wtforms.validators import InputRequired, NumberRange
from models.constantes import VOTO_NAME_PREFIX
from models.models import (db, PlanillaMesa, Cargo, TipoCargo,
                           Usuario, Roles, Lista)


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
        self.voto.label = votolista.lista.descripcion
        self.voto.data = votolista.votos if (
            votolista.votos is not None) else 0


class CargarPlanilla(Form):

    """docstring for CargarPlanilla"""
    planilla_id = HiddenField()
    nulos = IntegerField(label="Votos Nulos", default=0)
    blancos = IntegerField(label="Votos Blancos", default=0)
    impugnados = IntegerField(label="Votos Impugnados", default=0)
    total_votantes = IntegerField(label="Total Votantes", default=0)
    votos_listas = FieldList(
        FormField(VotoLista, default=lambda: AttrDict(voto='')))

    def __init__(self, planilla):
        super(CargarPlanilla, self).__init__(obj=planilla)
        self.planilla_id.data = planilla.id
        self.mesa_numero = planilla.mesa.numero
        self.titulo = "{0} {1}".format(
            str.upper(planilla.mesa.escuela.descripcion),
            repr(planilla.mesa.escuela.circuito))
        self.cargo = repr(planilla.cargo.tipo_cargo)
        self.cargo_id = planilla.cargo_id
        self.nulos.data = planilla.nulos if (
            planilla.nulos is not None) else 0
        self.blancos.data = planilla.blancos if (
            planilla.blancos is not None) else 0
        self.impugnados.data = planilla.impugnados if (
            planilla.impugnados is not None) else 0
        self.total_votantes.data = planilla.total_votantes if (
            planilla.total_votantes is not None) else 0
        for votolista in planilla.votos.join(Lista).order_by(
                Lista.posicionFrente, Lista.posicionLista).all():
            self.votos_listas.entries.append(VotoLista(votolista))
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
        return current_user.tieneRol(Roles.Administrador) and current_user.is_authenticated()


class UsuarioMV(ModelView):

    column_exclude_list = ("contraseña")

    def is_accessible(self):
        return current_user.tieneRol(Roles.Administrador) and current_user.is_authenticated()

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

    column_exclude_list = ("nulos", "blancos", "impugnados", "total_votantes")

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
        'nulos', 'blancos', 'impugnados', 'total_votantes', 'votos')

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
        return current_user.tieneRol(Roles.Administrador) and current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        super(PlanillaMV, self).__init__(PlanillaMesa, session, **kwargs)


class LoginForm(Form):

    usuario = TextField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])

    def validate_login(self):
        usuario = self.get_user()
        if usuario is None:
            raise validators.ValidationError('Invalid user')
        if not usuario.contraseña == self.password.data:
            raise validators.ValidationError('Invalid password')
        return True

    def get_user(self):
        return db.session.query(Usuario).filter(
            Usuario.usuario == self.usuario.data).first()
