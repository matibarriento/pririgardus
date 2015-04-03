#pririgardus.py

import logging
#import argparse
from flask import (Flask, render_template, jsonify, request, url_for, redirect)
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.admin import Admin
from flask.ext.login import (
    LoginManager, login_required, login_user, logout_user)
from logica import parsearPlanilla, exportarPlanilla
from models.models import (db, Mesa, PlanillaMesa, TipoCargo, AlcanceCargo,
                           Cargo, Frente, Lista, Usuario, Roles)
from models.views import (
    DatosMesa, CargarPlanilla, Exportar,
    PlanillaMV, LoginForm, UsuarioMV, Administrador)
from helpers import requires_roles

# NOMBRE_BASE_DATOS = 'pririgardus.db'
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
db.app = app
# base_template="_layout.html"
admin = Admin(app)#, index_view=Administrador, endpoint=None)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
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
app.jinja_env.globals['roles'] = Roles

###########################################################################

# Para configuraciones ###


@login_manager.user_loader
def load_user(userid):
    return db.session.query(Usuario).filter(
        Usuario.id == userid).first()

admin.add_view(Exportar(
    name='Exportar', endpoint='exportarPlanilla', category='Planilla'))
admin.add_view(PlanillaMV(
    db.session,
    name='Planillas', endpoint='listaPlanillas', category='Planilla'))

admin.add_view(UsuarioMV(
   db.session,
   name='Usuarios', endpoint='Usuarios', category='Usuarios'))

###########################################################################

# Para autocompetados ###


@app.route("/getMesas")
def getMesas():
    return jsonify([
        (str(num.numero), str(num.numero)) for num in Mesa.query.all()])


@app.route("/getAlcanceTipoCargo")
@app.route("/getAlcanceTipoCargo/<tipo_cargo_id>")
def getAlcanceTipoCargo(tipo_cargo_id):
    tipoCargo = db.session.query(TipoCargo).filter(
        TipoCargo.id == tipo_cargo_id).first()
    if tipoCargo is not None:
        cargo = tipoCargo.cargos.all()
        if(tipoCargo.alcance_cargo == AlcanceCargo.Cargo_Local.name):
            return jsonify([
               (str(c.id), str(c.alcance.getFullRepr())) for c in cargo])
        elif(tipoCargo.alcance_cargo == AlcanceCargo.Cargo_Departamental.name):
            return jsonify([
               (str(c.id), str(c.alcance.getFullRepr())) for c in cargo])
        elif(tipoCargo.alcance_cargo == AlcanceCargo.Cargo_Provincial.name):
            return jsonify([
               (str(c.id), str(c.alcance.descripcion)) for c in cargo])
        elif(tipoCargo.alcance_cargo == AlcanceCargo.Cargo_Nacional.name):
            return jsonify([
               (str(c.id), str(c.alcance.descripcion)) for c in cargo])
    else:
        return jsonify([])


@app.route("/getFrentesCargo")
@app.route("/getFrentesCargo/<cargo_id>")
def getFrentesCargo(cargo_id):
    frentes = db.session.query(Frente).join(
        Frente.listas).filter(Lista.cargo_id == 1).all()
    response = [(0, "Todos")]
    for frente in frentes:
        response.append((frente.id, frente.descripcion))
    return jsonify(response)


@app.route("/getListasFrenteCargo")
@app.route("/getListasFrenteCargo/<frente_id>/<cargo_id>")
def getListasFrenteCargo(frente_id, cargo_id):
    listas = db.session.query(Lista).filter(
        Lista.cargo_id == cargo_id, Lista.frente_id == frente_id).all()
    response = [(0, "Todas")]
    for lista in listas:
        response.append((lista.id, lista.descripcion))
    return jsonify(response)

###########################################################################

# Para renderizar helpers ###


@app.route("/getDatosMesa/<numero_mesa>")
def getDatosMesa(numero_mesa):
    mesa = db.session.query(Mesa).filter(Mesa.numero == numero_mesa).first()
    datosMesa = DatosMesa(mesa)
    return render_template("helpers/_datosMesa.html", datosMesa=datosMesa)

###########################################################################

# Pantallas y submits ###


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method in ('GET', None):
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.form)
        if(form.validate_login()):
            usuario = form.get_user()
            login_user(usuario)
            return redirect(request.args.get("next") or url_for("index"))
    return render_template("index.html", form=form)


@login_required
@app.route("/mesas", methods=['GET', 'POST'])
@requires_roles(Roles.DataEntry.name)
def mesas():
    return render_template("mesas.html")


@login_required
@app.route("/administrador")
@requires_roles(Roles.Administrador.name)
def administrador():
    return redirect("/admin")


@login_required
@app.route("/informes", methods=['GET', 'POST'])
@requires_roles(Roles.Prensa.name)
def informes():
    tiposCargo = db.session.query(TipoCargo).join(
        TipoCargo.cargos).order_by(Cargo.id.desc()).all()
    return render_template("helpers/_informe.html", tiposCargo=tiposCargo)


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
            if(len(datosMesa.planillas) > 0):
                return render_template("helpers/_datosMesa.html",
                                       datosMesa=datosMesa, botonSalir=True)
        except Exception as e:
            logger.log(logging.ERROR, e)
        return redirect(url_for("index"))


@app.route("/Exportar")
@app.route("/Exportar/<tipo_cargo_id>/<cargo_id>", methods=['POST'])
def ExportarPlanilla(cargo_id):
    exportarPlanilla(cargo_id)


@app.route("/Filtrar")
@app.route("/Filtrar/<tipo_cargo_id>/<cargo_id>", methods=['POST'])
def Filtrar(cargo_id):
    exportarPlanilla(cargo_id)


@login_required
@app.route("/salir")
def salir():
    logout_user()
    form = LoginForm()
    return render_template("index.html", form=form)

###########################################################################


app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    debugging = True
    # port = int(os.environ.get("PORT", argv.port))
    try:
        app.run(host='0.0.0.0', debug=debugging)
    except OSError as ose:
        pass
        # print(
        #     "Puerto en uso,por favor selecione
        #     uno usando -p [port] excepto {0}".format(
        #         argv.port))
        # print("Tal vez apreto Ctrl+Z para detener el servidor
        #       ...si no lo sabe usted xD")
