# purely used to test in shell. delete when everything works

from project.api.util_db import DB
from project.api.utils import plc_read_values
from project.api.models import PLCDBSchema, PLCDBSchema2, Plc_db
import snap7.client
import project.api.util_db as util

client = snap7.client.Client()
client.connect('192.168.0.1', 0, 0)
# Byte index    Variable name  Datatype
layout = """

0           tubes_per_row       FARRAY[1001]    # number of tubes per row
2002        tube_ROW            FARRAY[10000]   # element position gives row#
22002       tube_number_in_row  FARRAY[10000]   # element position gives col#
42002       tube_state          ARRAY[10000]    # element position gives value
62002       total_tubes         INT             # number of total tubes
62004       counter             INT             # counter
62006.0     debounce            BOOL
62008       total_rows          INT             # number of total rows
62010       coppycounter        INT
62012       overviewcoppied     INT
"""

db_number = 7
all_data = client.db_read(7, 0, 62014)

db = DB(
    db_number,              # the db we use
    all_data,               # bytearray from the plc
    layout,                 # layout specification DB variable data
                            # A DB specification is the specification of a
                            # DB object in the PLC you can find it using
                            # the dataview option on a DB object in PCS7

    62014+2,                   # size of the specification 17 is start
                            # of last value
                            # which is a DWORD which is 2 bytes,

    1,                      # number of row's / specifications

    id_field=None,          # field we can use to identify a row.
                            # default index is used
    layout_offset=0,        # sometimes specification does not start a 0
    db_offset=0             # At which point in 'all_data' should we start
                            # reading. if could be that the specification
                            # does not start at 0
)

db = db[0]               # gives back multiple db rows. We only have one row
PLCDB_schema = PLCDBSchema()
PLCDB_schema2 = PLCDBSchema2()


tube_state_client = plc_read_values(client)

# TODO: make db1 into a real Plc_DB object.. 
# Then we can probably add varPLC_DB to the database

final_read = Plc_db(
        tubes_per_row=db["tubes_per_row"],
        tube_ROW=db["tube_ROW"],
        tube_number_in_row=db["tube_number_in_row"],
        tube_state=db["tube_state"],
        tube_state_client=tube_state_client,
        total_tubes=db["total_tubes"],
        counter=db["counter"],
        debounce=db["debounce"],
        total_rows=db["total_rows"],
        coppycounter=db["coppycounter"],
        overviewcoppied=db["overviewcoppied"]
)

result = PLCDB_schema.dumps(final_read)

# Convert object back to bytearray so we can upload this to the plc
dbo = Plc_db.query.filter_by(plc_id=1).first()
initial_write = DB(
        tubes_per_row=db["tubes_per_row"],
        tube_ROW=db["tube_ROW"],
        tube_number_in_row=db["tube_number_in_row"],
        tube_state=db["tube_state"],
        tube_state_client=tube_state_client,
        total_tubes=db["total_tubes"],
        counter=db["counter"],
        debounce=db["debounce"],
        total_rows=db["total_rows"],
        coppycounter=db["coppycounter"],
        overviewcoppied=db["overviewcoppied"]
)

test = final_read.tubes_per_row
for elem in test:
    _data += elem.to_bytes(2, byteorder='little')
msg = bytearray(final_read.tubes_per_row)
row = util.DB_Row(msg, layout)
row['tubes_per_row']


def read_plc(client):
    """
    Read database, put in bytearray and turn it into an object
    Args:
        client (object): The client to use
    """
    db_number = 7
    all_data = client.db_read(7, 0, 62014)

    db = DB(
        db_number,              # the db we use
        all_data,               # bytearray from the plc
        layout,                 # layout specification DB variable data
                                # A DB specification is the specification of a
                                # DB object in the PLC you can find it using
                                # the dataview option on a DB object in PCS7

        62014+2,                   # size of the specification 17 is start
                                # of last value
                                # which is a DWORD which is 2 bytes,

        1,                      # number of row's / specifications

        id_field=None,          # field we can use to identify a row.
                                # default index is used
        layout_offset=0,        # sometimes specification does not start a 0
        db_offset=0             # At which point in 'all_data' should we start
                                # reading. if could be that the specification
                                # does not start at 0
    )
    return db
