
from sqlalchemy.exc import IntegrityError

from project import db

from project.api.models import Plc, Reactor
from project.tests.base import BaseTestCase
from project.tests.utils import add_plc, add_reactor, add_plc_to_db


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


class TestPlc_dbModel(BaseTestCase):
    '''
    Store the whole PLC memory into the database and check its correctness
    '''
    def test_add_plc_to_database(self):
        plc = add_plc('10.10.1.1', 0, 0)
        dbo = add_plc_to_db(tubes_per_row=[1, 2, 1], tube_ROW=[1, 2, 2, 3],
                            tube_number_in_row=[1, 1, 2, 1],
                            tube_state=[4, 2, 3, 1], total_tubes=4,
                            counter=1002, debounce=True, total_rows=3,
                            coppycounter=1, overviewcoppied=256, plc=plc)
        self.assertTrue(dbo.id)
        self.assertEqual(dbo.tubes_per_row, [1, 2, 1])
        self.assertEqual(dbo.tube_ROW, [1, 2, 2, 3])
        self.assertEqual(dbo.tube_number_in_row, [1, 1, 2, 1])
        self.assertEqual(dbo.tube_state, [4, 2, 3, 1])
        self.assertEqual(dbo.total_tubes, 4)
        self.assertEqual(dbo.counter, 1002)
        self.assertEqual(dbo.debounce, True)
        self.assertEqual(dbo.total_rows, 3)
        self.assertEqual(dbo.coppycounter, 1)
        self.assertEqual(dbo.overviewcoppied, 256)
        self.assertEqual(dbo.plc.id, 1)
        self.assertEqual(dbo.plc.ip, '10.10.1.1')
