# models.constantes

import os

VOTO_NAME_PREFIX = "voto-"
VALIDACION_PLANILLA = ['nulos', 'blancos', 'impugnados',
                                'recurridos', 'votantes']
TOTAL_PLANILLA = 'votantes'
FLASH_ERROR = "alert-danger"
FLASH_EXITO = "alert-success"
FLASH_INFO = "alert-info"
FLASH_ALERTA = "alert-warning"


class PlanillaEscrutada(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PlanillaInvalida(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UsuarioInvalido(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PasswordInvalida(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def url_for_default(default, archivo=''):
    ruta_base = os.path.dirname(os.path.dirname(__file__))
    ruta_archivo = "{0}{1}".format(ruta_base, archivo)
    ruta_default = "{0}{1}".format(ruta_base, default)
    if(os.path.isfile(ruta_archivo)):
        return archivo
    elif(os.path.isfile(ruta_default)):
        return default
    else:
        return ""
