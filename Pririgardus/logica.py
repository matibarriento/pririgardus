# logica.py

from flask.ext.login import current_user
from sqlalchemy import func, or_
from models.models import (
    db, PlanillaMesa, VotoListaMesa, Cargo, Frente, Lista, ListaCargo,
    Mesa, Escuela, Circuito)
from models.utils import (VOTO_NAME_PREFIX, VALIDACION_PLANILLA, TOTAL_PLANILLA,
                          PlanillaEscrutada, PlanillaInvalida)


def parsearPlanilla(planilla_id, planilla_form):
    pf = dict(planilla_form)
    planilla = db.session.query(PlanillaMesa).filter(
        PlanillaMesa.id == planilla_id).first()
    if planilla.escrutada:
        raise PlanillaEscrutada("La planilla ya fue escrutada")
    if not validarForm(planilla, planilla_form):
        raise PlanillaInvalida("Hubo un error al carcar la planilla")
    if current_user.otros_votos:
        for item in VALIDACION_PLANILLA:
            setattr(planilla, item, int(pf[item][0]))
    setattr(planilla, TOTAL_PLANILLA, int(pf[TOTAL_PLANILLA][0]))
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
        if voto.lista.lista.frente in current_user.frentes or
        len(current_user.frentes) == 0])
    if not cant_votos_form == cant_votos_frente_usuario:
        return False
    if current_user.otros_votos:
        for item in VALIDACION_PLANILLA:
            if not pf.keys().__contains__(item):
                return False
    return True


def exportarPlanilla(cargo_id):
    pass
    # cargo = Cargo.query.filter(Cargo.id == 2).first()


def cantidadMesasExcrutadas(cargo_id, secc_num):
    cargo = Cargo.query.filter(Cargo.id == cargo_id).first()
    totales = cargo.planillas.count()
    escrutadas = cargo.planillas.join(
        Mesa).join(
        Escuela).join(
        Circuito).filter(or_(Circuito.seccional_id == secc_num,
                             secc_num is None),
                         PlanillaMesa.escrutada).count()
    if totales == 0:
        resultado = 0
    else:
        resultado = round(escrutadas / totales * 100, 3)
    return "{0}% = {1} mesas".format(resultado, escrutadas)


def totalVotosCargo(cargo_id, frente_id, secc_num):

    total = 0
    totales = db.session.query(
        PlanillaMesa.votantes).join(
        VotoListaMesa).join(
        ListaCargo).join(
        Lista).join(
        Mesa).join(
        Escuela).join(
        Circuito).filter(or_(Circuito.seccional_id == secc_num,
                             secc_num is None),
                         or_(Lista.frente_id == frente_id,
                             frente_id == 0),
                         PlanillaMesa.escrutada,
                         ListaCargo.cargo_id == cargo_id).group_by(
        PlanillaMesa.id).all()
    for tot in totales:
        total += tot[0]
    return total
    # if frente_id == 0:
    #     total = 0
    #     total += db.session.query(func.sum(VotoListaMesa.votos)).join(
    #         PlanillaMesa).join(
    #         Mesa).join(
    #         Escuela).join(
    #         Circuito).filter(or_(Circuito.seccional_id == secc_num,
    #                              secc_num is None),
    #                          PlanillaMesa.cargo_id == cargo_id).scalar()
    #     total += db.session.query(
    #         func.sum(PlanillaMesa.blancos) +
    #         func.sum(PlanillaMesa.recurridos) +
    #         func.sum(PlanillaMesa.nulos) +
    #         func.sum(PlanillaMesa.impugnados)
    #     ).join(
    #         Mesa).join(
    #         Escuela).join(
    #         Circuito).filter(or_(Circuito.seccional_id == secc_num,
    #                              secc_num is None),
    #                          PlanillaMesa.cargo_id == cargo_id).scalar()

    #     return total
    # else:
    #     frente = Frente.query.get(frente_id)
    #     return frente.Votos_Frente(cargo_id, secc_num)


def datosInforme(cargo_id, secc_num, frente_id):
    # sorted(info, key=lambda fren: fren[1], reverse=True)
    if frente_id == 0:
        frentes = Frente.query.join(Lista).join(ListaCargo).filter(
            ListaCargo.cargo_id == cargo_id).all()
        return sorted([
            (str(frente.descripcion), frente.Votos_Frente(cargo_id, secc_num))
            for frente in frentes], key=lambda fren: fren[1], reverse=True)
    else:
        listas_frente_cargo = db.session.query(ListaCargo).join(
            Lista).join(
            Frente).filter(
            Frente.id == frente_id,
            ListaCargo.cargo_id == cargo_id)
        return sorted([(str(lista.lista.descripcion), lista.Votos_Lista(secc_num))
                       for lista in listas_frente_cargo],
                      key=lambda fren: fren[1], reverse=True)
