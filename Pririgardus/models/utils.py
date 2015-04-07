# models.constantes

VOTO_NAME_PREFIX = "voto-"
VALIDACION_PLANILLA = ['nulos', 'blancos', 'impugnados', 'recurridos']
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

