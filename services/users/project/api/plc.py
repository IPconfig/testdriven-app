import snap7.client
import snap7.util
import snap7.snap7types
from snap7.snap7exceptions import Snap7Exception

from flask import Blueprint, jsonify, render_template

#    plc = connect_plc('192.168.0.1', 0, 0)
#    data = read_plc(plc, 7, 0, 2002, 42002)

plc_blueprint = Blueprint('plc', __name__, template_folder='./templates')


def connect_plc(adress, rack, slot):
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


def read_plc(client, db_num, db_offset_start, db_offset_end, db_values_offset):
    #   client = snap7.client.Client()
    #   client.connect('192.168.0.1', 0, 0)
    """
    Read data from a S7 Server

    Parameters
    ----------
    plc : plc
        plc client
    db_num : Int
        database to be read
    db_offset_start : Int
        start of the tubes_per_row offset
    db_offset_end : Int
        end of the tubes_per_row offset
    db_values_offset : Int
        Offset on which data values appear, after the tubes per row are defined
    """
    tubes_data = client.db_read(db_num, db_offset_start, db_offset_end)
    decoded_tubes_per_row = [int.from_bytes(
        tubes_data[i:i + 2], byteorder='big')
                            for i in range(0, len(tubes_data), 2)
                            if int.from_bytes(
                                tubes_data[i:i + 2], byteorder='big') != 0]
#   total_pipes = sum(decoded_tubes_per_row)
#   print('tubes_per_row {}'.format(decoded_tubes_per_row))
#   print('total pipes: {}'.format(total_pipes))

    tubestate_start = db_values_offset  # actual values start from here
    tube_row_no = 1
    data = []
    for tubes in decoded_tubes_per_row:

        tubestate_size = tubes * 2
        tubestate_data = client.db_read(
            db_num, tubestate_start, tubestate_size
            )
        decoded_tubestate_data = [int.from_bytes(
            tubestate_data[i:i + 2], byteorder='big')
                                for i in range(0, len(tubestate_data), 2)]
#       print('row {}: {}'.format(tube_row_no, decoded_tubestate_data))
        tubestate_start = tubestate_start + tubestate_size
        tube_row_no = tube_row_no + 1
        data.append(decoded_tubestate_data)
    client.disconnect()
    return data
#   print(data)


@plc_blueprint.route('/plc', methods=['GET'])
def get_status():
    plc = connect_plc('192.168.0.1', 0, 0)
    data = read_plc(plc, 7, 0, 2002, 6002)
    response_object = {
        'status': 'success',
        'data': {'rows': data}
    }
#    plc = connect_plc('62.194.129.29', 0, 0
#   data = read_plc(plc, 7, 0, 2002, 6002))
#    return render_template('overview.html', {'rows': data})
    return jsonify(response_object), 200


@plc_blueprint.route('/plc/overview', methods=['GET'])
def overview():
    plc = connect_plc('192.168.0.1', 0, 0)
    data = read_plc(plc, 7, 0, 2002, 42002)
    return render_template('overview.html', {'rows': data})
