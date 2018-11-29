# services/plc/project/tests/utils.py

from project import db
from project.api.models import Plc, Reactor, Plc_db


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


def add_plc_to_db(tubes_per_row, tube_ROW, tube_number_in_row, tube_state,
                  total_tubes, counter, debounce, total_rows, coppycounter,
                  overviewcoppied, plc):
    dbo = Plc_db(
            tubes_per_row=tubes_per_row,
            tube_ROW=tube_ROW,
            tube_number_in_row=tube_number_in_row,
            tube_state=tube_state,
            total_tubes=total_tubes,
            counter=counter,
            debounce=debounce,
            total_rows=total_rows,
            coppycounter=coppycounter,
            overviewcoppied=overviewcoppied,
            plc=plc,
    )
    db.session.add(dbo)
    db.session.commit()
    return dbo
