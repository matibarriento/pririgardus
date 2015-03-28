#models.view.py
from wtforms import (Form, IntegerField, FieldList, FormField, HiddenField)
from flask.ext.admin import BaseView, expose
# from flask.ext.admin.model import BaseModelView
from flask.ext.admin.contrib.sqla import ModelView
#from wtforms.validators import InputRequired, NumberRange
from models.constantes import VOTO_NAME_PREFIX
from models.models import PlanillaMesa, Cargo, TipoCargo, db


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
        for votolista in planilla.votos.all():
            self.votos_listas.entries.append(VotoLista(votolista))
        self.escrutada = planilla.escrutada


class Exportar(BaseView):

    @expose('/')
    def index(self):
        tiposCargo = db.session.query(TipoCargo).join(
            TipoCargo.cargos).order_by(Cargo.id.desc()).all()
        return self.render('exportar.html', tiposCargo=tiposCargo)


class PlanillaMV(ModelView):
    can_create = False
    can_delete = False

    column_sortable_list = (
        ('mesa', PlanillaMesa.mesa_numero),
        ('cargo', PlanillaMesa.cargo_id),
        ('escrutada', PlanillaMesa.escrutada)
    )

    column_exclude_list = ("nulos", "blancos", "impugnados", "total_votantes")
    
    # column_searchable_list = (PlanillaMesa.mesa_numero)

    column_filters = ('mesa_numero', 'escrutada')

    # column_choices = {
    #     'cargo': [
    #         ('db_value', 'display_value'),
    #     ]
    # }

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

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(PlanillaMV, self).__init__(PlanillaMesa, session, **kwargs)
