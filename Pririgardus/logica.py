# logica.py

from flask.ext.login import current_user
from models.models import (
    db, PlanillaMesa, VotoListaMesa, Cargo, Frente, Lista)
from models.utils import VOTO_NAME_PREFIX, VALIDACION_PLANILLA


def parsearPlanilla(planilla_id, planilla_form):
    pf = dict(planilla_form)
    planilla = db.session.query(PlanillaMesa).filter(
        PlanillaMesa.id == planilla_id).first()
    if not validarForm(planilla, planilla_form):
        raise Exception("Planilla invalida")
    if len(current_user.frentes) == 0:
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
    cant_votos_form = len(
        [(keys, value)
            for keys, value
            in pf.items()
            if keys.__contains__(VOTO_NAME_PREFIX)])
    cant_votos_frente_usuario = len([
        voto
        for voto
        in planilla.votos.all()
        if voto.lista.frente in current_user.frentes or
        len(current_user.frentes) == 0])
    if not cant_votos_form == cant_votos_frente_usuario:
        return False
    if len(current_user.frentes) == 0:
        for item in VALIDACION_PLANILLA:
            if not pf.keys().__contains__(item):
                return False
    return True


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


def totalVotosCargo(cargo_id, frente_id):
    if frente_id == 0:
        planillas = PlanillaMesa.query.filter(
            PlanillaMesa.cargo_id == cargo_id).all()
        total = 0
        for planilla in planillas:
            total += planilla.Total_Votos()
        return total
    else:
        frente = Frente.query.get(frente_id)
        return frente.Votos_Frente(cargo_id)


def datosInforme(cargo_id, frente_id):
    if frente_id == 0:
        frentes = Frente.query.join(Lista).filter(
            Lista.cargo_id == cargo_id).all()
        return [
            (str(frente.descripcion), frente.Votos_Frente(cargo_id))
            for frente in frentes]
    else:
        frente = Frente.query.get(frente_id)
        listas_frente = frente.listas.join(
            Cargo).filter(Cargo.id == cargo_id).all()
        return [
            (str(lista.descripcion), lista.Votos_Lista())
            for lista in listas_frente]
