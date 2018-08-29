# services/plc/project/api/models.py

from project import db
from sqlalchemy.dialects.postgresql import ARRAY, INET


class Reactor(db.Model):
    __tablename__ = "reactors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(INET, nullable=False)
    test_row = db.Column(db.Integer, nullable=False)
    test_values = db.Column(ARRAY(db.Integer), nullable=False)

    def __init__(self, ip, test_row, test_values):
        self.ip = ip
        self.test_row = test_row
        self.test_values = test_values
    
    def to_json(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'test_row': self.test_row,
            'test_values': self.test_values
        }