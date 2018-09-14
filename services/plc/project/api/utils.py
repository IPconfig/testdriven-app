# services/plc/project/api/utils.py

import snap7.client
import snap7.util
import snap7.snap7types
from snap7.snap7exceptions import Snap7Exception
from project.api.models import Plc_db, PLCDBSchema
from project.api.util_db import DB


def plc_connect(adress, rack, slot):
    """
    Connect to a S7 server.

    Parameters
    ----------
    adress : IP adress
        IP adress of server
    rack : Int
        rack on server
    slot : Int
        slot on server
    """

    plc = snap7.client.Client()
    try:
        plc.connect(adress, rack, slot)  # ('IP-address', rack, slot)
        return plc
    except Snap7Exception as exc:
        print(exc)


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


def read_plc_memory(client):
    """
    Read database, put in bytearray and turn it into an object
    Args:
        client (object): The client to use
    """
    db_number = 7
    all_data = client.db_read(7, 0, 62014)

    _db = DB(
        db_number,              # the db we use
        all_data,               # bytearray from the plc
        layout,                 # layout specification DB variable data
                                # A DB specification is the specification of a
                                # DB object in the PLC you can find it using
                                # the dataview option on a DB object in PCS7

        62012+2,                # size of the specification 17 is start
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
    memObj = _db[0]                # remove the row array, since it's the only row
    return memObj


def map_memory_to_db(memObj, client):
    tube_state_client = plc_read_values(client)  # add filtered values

    dbo = Plc_db(
            tubes_per_row=memObj["tubes_per_row"],
            tube_ROW=memObj["tube_ROW"],
            tube_number_in_row=memObj["tube_number_in_row"],
            tube_state=memObj["tube_state"],
            tube_state_client=tube_state_client,
            total_tubes=memObj["total_tubes"],
            counter=memObj["counter"],
            debounce=memObj["debounce"],
            total_rows=memObj["total_rows"],
            coppycounter=memObj["coppycounter"],
            overviewcoppied=memObj["overviewcoppied"]
    )
    return dbo


def plc_db_to_json(dbo):
    PLCDB_schema = PLCDBSchema()
    result = PLCDB_schema.dumps(dbo)
    return result


def read_plc(client):
    memObj = read_plc_memory(client)
    dbo = map_memory_to_db(memObj, client)
    return dbo

def write_plc(data, client):
    """
    write database, put in bytearray and turn it into an object
    Args:
        data (object): data to put into the plc
        client (object): The client to write to
    """
    dbo = Plc_db.query.filter_by(plc_id=1).first()


# TODO: create a ['values_filtered'] for db obj
# TODO: Transform and add  db.session.add(Plc_db(
#            username=username, email=email, password=password))


def plc_read_values(client):
    # This function returns an array with an arrary of values per row
    # ex of 2 rows with 4 values each: [[1,2,2,3], [4,4,3,1]]
    tubes_per_row_raw = client.db_read(7, 0, 2002)
    # decoded_tubes_per_row is something like [10,10,10,10] for a 4x10 matrix
    # 0 values get filtered, so there should be no empty rows between elements
    tubes_per_row_decoded = [int.from_bytes(
        tubes_per_row_raw[i:i + 2], byteorder='big')
                            for i in range(0, len(tubes_per_row_raw), 2)
                            if int.from_bytes(
                                tubes_per_row_raw[i:i + 2],
                                byteorder='big') != 0]

    tubestate_start = 42002  # actual values start from this offset
    tube_row_no = 1
    tube_row_values = []

    for tubes in tubes_per_row_decoded:
        tubes_size = tubes * 2  # one element takes 2 bytes
        tube_row_values_raw = client.db_read(7, tubestate_start, tubes_size)
        # returns an array with all values per row
        tube_row_values_decoded = [int.from_bytes(
            tube_row_values_raw[i:i + 2], byteorder='big')
            for i in range(0, len(tube_row_values_raw), 2)]
#       print('row {}: {}'.format(tube_row_no, tube_row_values_decoded))

        tubestate_start = tubestate_start + tubes_size  # go to next row
        tube_row_no = tube_row_no + 1  # increase row number
        tube_row_values.append(tube_row_values_decoded)

    return tube_row_values
