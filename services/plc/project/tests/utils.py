# services/plc/project/tests/utils.py

from project import db
from project.api.models import Plc, Reactor


def add_plc(ip, rack, slot):
    plc = Plc(
        ip=ip,
        rack=rack,
        slot=slot,
    )
    db.session.add(plc)
    db.session.commit()
    return plc


def add_reactor(reactor_id, row, values, plc):
    reactor = Reactor(
        reactor_id=reactor_id,
        row=row,
        values=values,
        plc=plc,
    )
    db.session.add(reactor)
    db.session.commit()
    return reactor
