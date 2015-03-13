#pririgardus.py
import os
import logging
import argparse
from flask import (Flask, render_template, jsonify)
#from flask.ext.admin import Admin
from models.models import db, Mesa
from models.views import DatosMesa

NOMBRE_BASE_DATOS = 'pririgardus.db'
app = Flask(__name__)
app.config["STATIC_URL"] = '/static/'
app.config["STATIC_ROOT"] = '/static/'
app.config["BASE_DIR"] = os.path.dirname(os.path.dirname(__file__))
app.config["SECRET_KEY"] = "pririgardus-elektoj"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + NOMBRE_BASE_DATOS
db.init_app(app)
db.app = app
#admin = Admin(app)

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
app.config['LOGGER_NAME'] = logger.name
# admin.add_view(ModelView(Pais, db.session))
# admin.add_view(ModelView(Provincia, db.session))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/getMesas")
def getMesas():
    return jsonify([
        (str(num.numero), str(num.numero)) for num in Mesa.query.all()])


@app.route("/getdatosMesa/<numero_mesa>")
def getdatosMesa(numero_mesa):
    mesa = db.session.query(Mesa).filter(Mesa.numero == numero_mesa).first()
    escuela = mesa.escuela
    circuito = escuela.circuito
    cargos = [cargo for cargo in mesa.getCargos()]
    datosMesa = DatosMesa(
        mesa.numero, circuito, escuela.descripcion, cargos)
    return render_template("helpers/_datosMesa.html", datosMesa=datosMesa)


@app.route("/llenarPlanilla/<numero_mesa>/<cargo>")
def llenarPlanilla(numero_mesa, cargo):
    pass

if __name__ == "__main__":
    debugging = True
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
