#logica.py
from models.models import (db, PlanillaMesa, VotoListaMesa, Cargo, Frente)
from models.constantes import VOTO_NAME_PREFIX, VALIDACION_PLANILLA


def parsearPlanilla(planilla_id, planilla_form):
    pf = dict(planilla_form)
    planilla = db.session.query(PlanillaMesa).filter(
        PlanillaMesa.id == planilla_id).first()
    if not validarForm(planilla, planilla_form):
        raise Exception("Planilla invalida")
    for item in VALIDACION_PLANILLA:
        setattr(planilla, item, int(pf[item][0]))
    for keys, value in pf.items():
        if keys.__contains__(VOTO_NAME_PREFIX):
            voto_id = keys.replace(VOTO_NAME_PREFIX, '')
            voto = planilla.votos.filter(VotoListaMesa.id == voto_id).first()
            voto.votos = int(value[0])
            db.session.add(voto)
    planilla.escrutada = True
    db.session.add(planilla)
    db.session.commit()


def validarForm(planilla, planilla_form):

    pf = dict(planilla_form)
    cant_votos_form = (
        len([
            (keys, value)
            for keys, value in pf.items()
            if keys.__contains__(VOTO_NAME_PREFIX)
        ]) == len(planilla.votos.all()))
    if not cant_votos_form:
        return cant_votos_form
    for item in VALIDACION_PLANILLA:
        if not pf.keys().__contains__(item):
            return False
    return True
    pass


def exportarPlanilla(cargo_id):
    pass
    # cargo = Cargo.query.filter(Cargo.id == 2).first()


def cantidadMesasExcrutadas(cargo_id):
    cargo = Cargo.query.filter(Cargo.id == cargo_id).first()
    totales = cargo.planillas.count()
    escrutadas = cargo.planillas.filter(PlanillaMesa.escrutada).count()

    if totales == 0 or escrutadas == 0:
        return 0
    else:
        return round(escrutadas / totales, 3)


def datosInforme(tipo_cargo_id, cargo_id, frente_id):
    if frente_id == 0:
        pass
    else:
        frente = Frente.query.get(frente_id)
        listas_frente = frente.listas.join(
            Cargo).filter(Cargo.id == cargo_id).all()
        return [
            (str(lista.descripcion), lista.Votos_Lista())
            for lista in listas_frente]
