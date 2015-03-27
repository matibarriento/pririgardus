#pririgardus.py
import os
import logging
#import argparse
from flask import (Flask, render_template, jsonify, request, url_for, redirect)
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.admin import Admin
from logica import parsearPlanilla
from models.models import db, Mesa, PlanillaMesa
from models.views import DatosMesa, CargarPlanilla, Exportar, PlanillaMV

NOMBRE_BASE_DATOS = 'pririgardus.db'
app = Flask(__name__)
app.config["STATIC_URL"] = '/static/'
app.config["STATIC_ROOT"] = '/static/'
app.config["LOGGER_NAME"] = 'PRG'
app.config["BASE_DIR"] = os.path.dirname(os.path.dirname(__file__))
app.config["SECRET_KEY"] = "pririgardus-elektoj"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + NOMBRE_BASE_DATOS
db.init_app(app)
db.app = app
admin = Admin(app)

# parser = argparse.ArgumentParser(description='Pririgardus Arguments Parser')
# parser.add_argument('-l', '--logging', help='logging', action='store_true')
# parser.add_argument('-d', '--debug', help='debug', action='store_true')
# parser.add_argument('-p', '--port', help='port', type=int, default=5000)
# argv = parser.parse_args()

logger = logging.getLogger('PRG')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
# if(argv.logging):
logger.addHandler(handler)
app.config['LOGGER_NAME'] = logger.name

admin.add_view(Exportar(
    name='Exportar', endpoint='ExportarPlanilla', category='Planilla'))
admin.add_view(PlanillaMV(
    db.session,
    name='Planillas', endpoint='ListaPlanillas', category='Planilla'))
# admin.add_view(ModelView(Provincia, db.session))


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/getMesas")
def getMesas():
    return jsonify([
        (str(num.numero), str(num.numero)) for num in Mesa.query.all()])


@app.route("/getDatosMesa/<numero_mesa>")
def getDatosMesa(numero_mesa):
    mesa = db.session.query(Mesa).filter(Mesa.numero == numero_mesa).first()
    datosMesa = DatosMesa(mesa)
    return render_template("helpers/_datosMesa.html", datosMesa=datosMesa)


@app.route("/Planilla/<planilla_id>", methods=['GET', 'POST'])
def Planilla(planilla_id):
    if request.method in ('GET', None):
        planilla = db.session.query(PlanillaMesa).filter(
            PlanillaMesa.id == planilla_id).first()
        form = CargarPlanilla(planilla)
        return render_template("planilla.html", form=form)
    elif request.method == 'POST':
        try:
            parsearPlanilla(planilla_id, request.form)
            mesa = db.session.query(PlanillaMesa).filter(
                PlanillaMesa.id == planilla_id).first().mesa
            datosMesa = DatosMesa(mesa, todas=False)
            return render_template("helpers/_datosMesa.html",
                                   datosMesa=datosMesa, botonSalir=True)
        except Exception as e:
            logger.log(logging.ERROR, e)
        return redirect(url_for("index"))

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    debugging = True
    # port = int(os.environ.get("PORT", argv.port))
    try:
        app.run(host='0.0.0.0', debug=debugging)
    except OSError as ose:
        pass
        # print(
        #     "Puerto en uso,por favor selecione \
        #     uno usando -p [port] excepto {0}".format(
        #         argv.port))
        # print("Tal vez apreto Ctrl+Z para detener el servidor\
        #       ...si no lo sabe usted xD")
