#models.viewmodels.py
#from wtforms import Form, BooleanField, TextField, PasswordField, validators


class DatosMesa(object):

    """docstring for DatosMesa"""

    def __init__(self, mesa_numero, circuito, escuela, cargos):
        super(DatosMesa, self).__init__()
        self.mesa_numero = mesa_numero
        self.circuito = circuito
        self.escuela = escuela
        self.cargos = cargos
