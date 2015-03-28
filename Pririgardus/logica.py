#logica.py
from models.models import db, PlanillaMesa, VotoListaMesa, Cargo, Mesa
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
    cargo = Cargo.query.filter(Cargo.id == 2).first()
