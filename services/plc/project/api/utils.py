# services/plc/project/api/utils.py

import snap7.client
import snap7.util
import snap7.snap7types
from snap7.snap7exceptions import Snap7Exception

from project import db
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


def map_bytearray_with_layout(client, db_number, layout, _bytearray, size):
    """
    Read database, put in bytearray and turn it into an object
    Args:
        client (object): The client to use
        db_number (int): the database of the plc
        layout: layout specification
        _bytearray: bytearray from the plc
        size:
    """

    # _bytearray = client.db_read(7, 0, 62014)
    # size = 62012+2
    _db = DB(
        db_number,              # the db we use
        _bytearray,             # bytearray from the plc
        layout,                 # layout specification DB variable data
                                # A DB specification is the specification of a
                                # DB object in the PLC you can find it using
                                # the dataview option on a DB object in PCS7
        size,                   # size of the specification 17 is start
                                # of last value
                                # which is a DWORD which is 2 bytes,
        1,                      # number of row's / specifications
        id_field=None,          # field we can use to identify a row.
                                # default index is used
        layout_offset=0,        # sometimes specification does not start a 0
        db_offset=0             # At what point in '_bytearray' should we start
                                # reading. if could be that the specification
                                # does not start at 0
    )
    memObj = _db[0]             # remove the row array, since it's the only row
    return memObj


def map_memory_to_dbo(memObj, filtered_tubes):
    dbo = Plc_db(
            tubes_per_row=memObj["tubes_per_row"],
            tube_ROW=memObj["tube_ROW"],
            tube_number_in_row=memObj["tube_number_in_row"],
            tube_state=memObj["tube_state"],
            tube_state_client=filtered_tubes,
            total_tubes=memObj["total_tubes"],
            counter=memObj["counter"],
            debounce=memObj["debounce"],
            total_rows=memObj["total_rows"],
            coppycounter=memObj["coppycounter"],
            overviewcoppied=memObj["overviewcoppied"]
    )
    return dbo


def map_dbo_to_memory(dbo, memObj):
    memObj["tubes_per_row"] = dbo.tubes_per_row
    memObj["tube_ROW"] = dbo.tube_ROW
    memObj["tube_number_in_row"] = dbo.tube_number_in_row
    memObj["tube_state"] = dbo.tube_state
    # tube_state_client will not be written to plc memory
    memObj["total_tubes"] = dbo.total_tubes
    memObj["counter"] = dbo.counter
    memObj["debounce"] = dbo.debounce
    memObj["total_rows"] = dbo.total_rows
    memObj["coppycounter"] = dbo.coppycounter
    memObj["overviewcoppied"] = dbo.overviewcoppied
    return memObj


def plc_db_to_json(dbo):
    PLCDB_schema = PLCDBSchema()
    result = PLCDB_schema.dumps(dbo)
    return result


def plc_db_to_object(dbo):
    PLCDB_schema = PLCDBSchema()
    result = PLCDB_schema.dump(dbo)
    return result

# db_number, layout, _bytearray, size


def read_plc(client):
    '''
    Read memory of PLC and return a db object
    Args:
        client (object): Connected PLC object
    '''
    db_number = 7
    size = 62014
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

    _bytearray = client.db_read(db_number, 0, size)  # read plc data
    memObj = map_bytearray_with_layout(client, db_number,
                                       layout, _bytearray, size)
    state_filter = filter_tube_state(memObj)  # add filtered state to memObj
    dbo = map_memory_to_dbo(memObj, state_filter)
    return dbo


def write_plc(client):
    '''
    Read memory of PLC and return a db object
    Args:
        client (object): Connected PLC object
    '''
    db_number = 7
    size = 62014
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

    # read plc data, should be all zeroes after reboot
    _bytearray = client.db_read(db_number, 0, size)

    memObj = map_bytearray_with_layout(client, db_number,
                                       layout, _bytearray, size)
    dbo = Plc_db.query.filter_by(plc_id=1).first()
    memObj = map_dbo_to_memory(dbo, memObj)
    return memObj


def filter_tube_state(memObj):
    '''
    returns a list with a list of values per row
    Since the array is 10k elements originally,
    this will only list neccesary elements.
    This list will be passed to the client
    '''
    tubes_per_row = memObj["tubes_per_row"]
    tubes_row_values = memObj["tube_state"]
    result = []

    start = 0
    for tubes in tubes_per_row:
        _temp = [tubes_row_values[start:start + tubes]]
        start = start + tubes
        result.extend(_temp)
    return result


def write_database(response_object, dbo, client):
    reactor = Plc_db.query.filter_by(plc_id=client.id).first()
    if reactor is None:
        dbo.plc_id = client.id  # add plc id as FK to dataset
        db.session.add(dbo)
        db.session.commit()
        result = plc_db_to_object(dbo)
        response_object['status'] = 'success'
        response_object['message'] = 'PLC data saved in db'
        response_object['plc_db'] = result
    else:
        # update values with new readings
        dbo.plc_id = reactor.plc_id
        dbo.id = reactor.id

    #    reactor.tube_state_client = dbo.tube_state_client
        db.session.add(dbo)
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'PLC data updated in db'
        result = plc_db_to_object(dbo)
        response_object['plc_db'] = result
    return response_object
