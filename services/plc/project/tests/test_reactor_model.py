from project.tests.base import BaseTestCase
from project.tests.utils import add_reactor


class TestReactorModel(BaseTestCase):
    def test_add_reactor(self):
        reactor = add_reactor()
        self.assertTrue(reactor.id)
        self.assertEqual(reactor.ip, '10.10.1.1')
        self.assertEqual(reactor.test_row, 1)
        self.assertEqual(reactor.test_values, [1, 2, 3, 4])
