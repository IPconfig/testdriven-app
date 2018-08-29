# services/plc/project/tests/utils.py

from project import db
from project.api.models import Reactor


def add_reactor(
            ip='10.10.1.1',
            test_row=1,
            test_values=[1, 2, 3, 4]):
    reactor = Reactor(
        ip=ip,
        test_row=test_row,
        test_values=test_values,
    )
    db.session.add(reactor)
    db.session.commit()
    return reactor
