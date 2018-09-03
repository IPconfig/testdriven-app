
from sqlalchemy.exc import IntegrityError

from project import db

from project.api.models import Plc, Reactor
from project.tests.base import BaseTestCase
from project.tests.utils import add_plc, add_reactor


class TestPlcModel(BaseTestCase):
    def test_add_plc(self):
        plc = add_plc('10.10.1.1', 0, 0)
        self.assertTrue(plc.id)
        self.assertEqual(plc.ip, '10.10.1.1')
        self.assertEqual(plc.rack, 0)
        self.assertEqual(plc.slot, 0)

    def test_add_plc_duplicate_ip(self):
        add_plc('10.10.1.1', 0, 0)
        duplicate_plc = Plc(
            ip='10.10.1.1',
            rack='0',
            slot='0'
        )
        db.session.add(duplicate_plc)
        self.assertRaises(IntegrityError, db.session.commit)


class TestReactorModel(BaseTestCase):
    '''
    represents the pipes and their values of a reactor
    '''
    def test_add_reactor(self):
        plc = add_plc('10.10.1.1', 0, 0)
        reactor = add_reactor(reactor_id=1, row=1, values=[1, 2, 3], plc=plc)
        self.assertTrue(reactor.id)
        self.assertEqual(reactor.reactor_id, 1)
        self.assertEqual(reactor.row, 1)
        self.assertEqual(reactor.plc.id, 1)

    def test_multiple_reactor_rows(self):
        plc = add_plc('10.10.1.1', 0, 0)
        add_reactor(reactor_id=1, row=1, values=[1, 2, 3], plc=plc)
        add_reactor(reactor_id=1, row=2, values=[4, 1, 4], plc=plc)
        reactor = Reactor.query.filter_by(reactor_id=1).all()
        self.assertTrue(reactor[0].id)
        self.assertEqual(reactor[0].reactor_id, 1)
        self.assertEqual(reactor[0].row, 1)
        self.assertEqual(reactor[0].values, [1, 2, 3])
        self.assertEqual(reactor[0].plc.id, 1)
        self.assertTrue(reactor[1].id)
        self.assertEqual(reactor[1].reactor_id, 1)
        self.assertEqual(reactor[1].row, 2)
        self.assertEqual(reactor[1].values, [4, 1, 4])
        self.assertEqual(reactor[1].plc.id, 1)
