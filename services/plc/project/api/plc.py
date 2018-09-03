from project.api.util_db import DB


# Byte index    Variable name  Datatype
layout = """

0           Tubes_per_row       FARRAY[1001]
2002        Tube_ROW            FARRAY[10000]
22002       Tube_number_in_row  FARRAY[10000]
42002       Tube_state          ARRAY[10000]
62002       Total_tubes         INT
62004       Counter             INT
62006       Debounce            BOOL
62008       Total_rows          INT
62010       Coppycounter        INT
62012       overviewcoppied     INT
"""


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
