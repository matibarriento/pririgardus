#models.view.py
#from wtforms import Form, BooleanField, TextField, PasswordField, validators


class DatosMesa(object):

    """docstring for DatosMesa"""

    def __init__(self, mesa):
        super(DatosMesa, self).__init__()
        self.mesa_numero = mesa.numero
        self.circuito = repr(mesa.escuela.circuito)
        self.escuela = repr(mesa.escuela)
        self.planillas = [BotonPlanilla(planilla)
                          for planilla in mesa.planillas]


class BotonPlanilla(object):

    """docstring for BotonPlanilla"""

    def __init__(self, planilla):
        super(BotonPlanilla, self).__init__()
        self.id = planilla.id
        self.texto = planilla.cargo.tipo_cargo.descripcion
        self.habilitado = not planilla.escrutada


class Planilla(object):

    """docstring for Planilla"""

    def __init__(self, planilla):
        super(Planilla, self).__init__()
        self.mesa_numero = planilla.mesa.numero
        self.titilo = "{0} {1}".format(
            repr(planilla.mesa.escuela.circuito) + repr(planilla.mesa.escuela))
