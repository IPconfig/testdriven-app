# services/plc/project/api/base.py

from flask import Blueprint, jsonify, render_template

from project.api.models import Plc
from project.api.utils import (plc_connect, read_plc, write_plc,
                               save_to_db, filter_tube_state)


plc_blueprint = Blueprint('plc', __name__, template_folder='./templates')


@plc_blueprint.route('/plc', methods=['GET'])
def get_status():
    response_object = {
        'status': 'fail',
        'message': 'No PLC configured in database'
    }
    try:
        client = Plc.query.first()
        plc = plc_connect(adress=client.ip, rack=client.rack, slot=client.slot)
        if plc is None:
            response_object['message'] = 'Connection to PLC failed'
            return jsonify(response_object), 400
        else:
            response_object['message'] = 'hiep hiep'
            response_object['status'] = 'success'
            dbo = read_plc(plc)
            if not dbo:
                response_object['message'] = 'Could not retrieve data from plc'
                return jsonify(response_object), 400
            else:
                data = filter_tube_state(dbo.tubes_per_row,
                                         dbo.tube_state)
                response_object = save_to_db(client, dbo)
                response_object['tube_values_filtered'] = data
                return jsonify(response_object), 200
                plc.disconnect()
    except Exception:
        return jsonify(response_object), 400


@plc_blueprint.route('/plc/restore', methods=['GET'])
def restore_db():
    response_object = {
        'status': 'fail',
        'message': 'An error occured.'
    }
    try:
        client = Plc.query.first()
        plc = plc_connect(adress=client.ip, rack=client.rack, slot=client.slot)
        if plc is None:
            response_object['message'] = 'Connection to PLC failed'
            return jsonify(response_object), 400
        else:
            write_plc(plc)
            response_object['status'] = 'success'
            response_object['message'] = 'dbo set to plc memory'
            return jsonify(response_object), 200
    except Exception:
        return jsonify(response_object), 400


# Route to the old layout
@plc_blueprint.route('/plc/overview', methods=['GET'])
def overview():
    plc = plc_connect('192.168.0.1', 0, 0)
    response = read_plc(plc)
    data = filter_tube_state(response.tubes_per_row,
                             response.tube_state)
#    plcdb_schema = PLCDBSchema(only=['tube_state_client'])
#    result = plcdb_schema.dump(response)
#    result = result['tube_state_client']
#    response_object['status'] = 'success'
#    save_to_db(response, client)
    return render_template('overview.html', values=data)


@plc_blueprint.route('/plc/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
