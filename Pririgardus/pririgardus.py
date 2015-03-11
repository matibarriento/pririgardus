#pririgardus.py
import os
import logging
import argparse
from flask import (Flask)
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from models.models import db, Pais, Provincia

NOMBRE_BASE_DATOS = 'pririgardus.db'
app = Flask(__name__)
app.config["STATIC_URL"] = '/static/'
app.config["STATIC_ROOT"] = '/static/'
app.config["BASE_DIR"] = os.path.dirname(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + NOMBRE_BASE_DATOS
db.init_app(app)
db.app = app
admin = Admin(app)

parser = argparse.ArgumentParser(description='Pririgardus Arguments Parser')
parser.add_argument('-l', '--logging', help='logging', action='store_true')
parser.add_argument('-d', '--debug', help='debug', action='store_true')
parser.add_argument('-p', '--port', help='port', type=int, default=5000)
argv = parser.parse_args()

logger = logging.getLogger('PRG')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
if(argv.logging):
    logger.addHandler(handler)

# admin.add_view(ModelView(Pais, db.session))
# admin.add_view(ModelView(Provincia, db.session))

if __name__ == "__main__":
    debugging = argv.debug
    port = int(os.environ.get("PORT", argv.port))
    try:
        app.run(host='0.0.0.0', port=port, debug=debugging)
    except OSError as ose:
        print(
            "Puerto en uso,por favor selecione \
            uno usando -p [port] excepto {0}".format(
                argv.port))
        print("Tal vez apreto Ctrl+Z para detener el servidor\
              ...si no lo sabe usted xD")
