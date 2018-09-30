# project/tests/test_eval.py


import json

from project.tests.base import BaseTestCase


class TestBaseBlueprint(BaseTestCase):

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/plc/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])


# TODO: test when no client is set.
# TODO: Test when cant connect to plc
# TODO: Test when db can't be read
# TODO: Test add dbo to db; new row
# TODO: Test add dbo to db; update existing values
