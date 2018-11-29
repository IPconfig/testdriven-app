# services/plc/project/api/models.py

from project import db, ma
from sqlalchemy.dialects.postgresql import ARRAY, INET
from marshmallow import fields, Schema, post_load


# --- MODELS --- #
class Plc(db.Model):
    __tablename__ = "plc"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(INET, unique=True, nullable=False)
    rack = db.Column(db.Integer, nullable=False)
    slot = db.Column(db.Integer, nullable=False)
    reactors = db.relation('Reactor', backref='plc', lazy=True)
    plc_db = db.relation('Plc_db', backref='plc', lazy=True)

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


class Plc_db(db.Model):
    __tablename__ = "plc_db"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tubes_per_row = db.Column(ARRAY(db.Integer), nullable=False)
    tube_ROW = db.Column(ARRAY(db.Integer), nullable=False)
    tube_number_in_row = db.Column(ARRAY(db.Integer), nullable=False)
    tube_state = db.Column(ARRAY(db.Integer), nullable=False)
#    tube_state_client = db.Column(ARRAY(db.Integer), nullable=True)
    total_tubes = db.Column(db.Integer, nullable=False)
    counter = db.Column(db.Integer, nullable=False)
    debounce = db.Column(db.Boolean, nullable=False)
    total_rows = db.Column(db.Integer, nullable=False)
    coppycounter = db.Column(db.Integer, nullable=False)
    overviewcoppied = db.Column(db.Integer, nullable=False)
    plc_id = db.Column(db.Integer, db.ForeignKey('plc.id'), nullable=False)


# --- SCHEMAS --- #
class PLCDBSchema2(Schema):
    tubes_per_row = fields.List(fields.Int())
    tube_ROW = fields.List(fields.Int())
    tube_number_in_row = fields.List(fields.Int())
    tube_state = fields.List(fields.Int())
    tube_state_client = fields.List(fields.List(fields.Int()))
    total_tubes = fields.Int()
    counter = fields.Int()
    debounce = fields.Bool()
    total_rows = fields.Int()
    coppycounter = fields.Int()
    overviewcoppied = fields.Int()


class PLCDBSchema(ma.ModelSchema):
    # SQLAlchemy doesn't care if there are lists in a list
    # the generated field needs to be overwritten
    # else we'll get a validation error
 #   tube_state_client = fields.List(fields.List(fields.Int()))

    class Meta:
        model = Plc_db  # Bind the schema to the DB model

    @post_load
    def make_plc_db(self, data):
        return Plc_db(**data)


class PlcSchema(ma.ModelSchema):
    class Meta:
        model = Plc
