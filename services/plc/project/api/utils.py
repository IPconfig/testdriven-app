# services/plc/project/api/utils.py

import snap7.client
import snap7.util
import snap7.snap7types
from snap7.snap7exceptions import Snap7Exception


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
