import os

NOMBRE_BASE_DATOS = 'pririgardus.db'
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
LOGGER_NAME = 'PRG'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = "pririgardus-elektoj"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + NOMBRE_BASE_DATOS
