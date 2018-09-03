# services/plc/project/api/models.py

from project import db
from sqlalchemy.dialects.postgresql import ARRAY, INET


class Plc(db.Model):
    __tablename__ = "plc"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(INET, unique=True, nullable=False)
    rack = db.Column(db.Integer, nullable=False)
    slot = db.Column(db.Integer, nullable=False)
    reactors = db.relation('Reactor', backref='plc', lazy=True)

    def __init__(self, ip, rack, slot):
        self.ip = ip
        self.rack = rack
        self.slot = slot

    def to_json(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'rack': self.rack,
            'slot': self.slot
        }


class Reactor(db.Model):
    __tablename__ = "reactors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reactor_id = db.Column(db.Integer, index=True, nullable=False)
    row = db.Column(db.Integer, nullable=False)
    values = db.Column(ARRAY(db.Integer), nullable=False)
    plc_id = db.Column(db.Integer, db.ForeignKey('plc.id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'row': self.row,
            'values': self.values
        }
