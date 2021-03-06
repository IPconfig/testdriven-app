# services/plc/project/api/base.py

from flask import Blueprint, jsonify, render_template, make_response

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
    headers = {'content-type': 'text/plain'}
    response = make_response('An error occured.', 400)
    response.headers = headers
    try:
        client = Plc.query.first()
        plc = plc_connect(adress=client.ip, rack=client.rack, slot=client.slot)
        if plc is None:
            headers = {'content-type': 'text/plain'}
            response = make_response('Connection to PLC failed', 400)
            response.headers = headers
            return response
        else:
            write_plc(plc)
            response = make_response('backup restored to PLC', 200)
            response.headers = headers
            return response
    except Exception:
        return response


# Route to the old layout
@plc_blueprint.route('/plc/overview', methods=['GET'])
def overview():
    client = Plc.query.first()
    plc = plc_connect(adress=client.ip, rack=client.rack, slot=client.slot)
    dbo = read_plc(plc)
    data = filter_tube_state(dbo.tubes_per_row,
                             dbo.tube_state)
    save_to_db(client, dbo)
    return render_template('overview.html', values=data)


@plc_blueprint.route('/plc/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
