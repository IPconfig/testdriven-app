# services/plc/project/api/base.py

from flask import Blueprint, jsonify, render_template

from project.api.models import Plc, PLCDBSchema
from project.api.utils import plc_connect, read_plc, write_database


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
            # return jsonify(response_object), 200
            dbo = read_plc(plc)
            if not dbo:
                response_object['message'] = 'Could not retrieve data from plc'
                return jsonify(response_object), 400
            else:
                result = write_database(response_object, dbo, client)
                return jsonify(result), 200
                plc.disconnect()
    except Exception as e:
        return jsonify(response_object), 400


@plc_blueprint.route('/plc/overview', methods=['GET'])
def overview():
    plc = plc_connect('192.168.0.1', 0, 0)
    response = read_plc(plc)
    plcdb_schema = PLCDBSchema(only=('tube_state_client'))
    result = plcdb_schema.dump(response)

    return render_template('overview.html', values=result)


# @plc_blueprint.route('/plc/restore', methods=['GET'])
# def restore_db():
#     response_object = {
#         'status': 'fail',
#         'message': 'An error occured.'
#     }
#     try:
#         client = Plc.query.first()
#       plc = plc_connect(adress=client.ip, rack=client.rack, slot=client.slot)
#         write_plc(plc)
#         plc.disconnect()

#         response_object['status'] = 'success'
#         response_object['message'] = 'dbo set to plc memory'
#         return jsonify(response_object), 200

#     except (exc.IntegrityError, ValueError, Exception) as e:
#         response_object['error'] = e
#         return jsonify(response_object), 400


# @plc_blueprint.route('/plc/new', methods=['GET'])
# def new():
#     response_object = {
#         'status': 'fail',
#         'message': 'An error occured.'
#     }
#     try:
#         plc = plc_connect('192.168.0.1', 0, 0)
#         if not plc:
#             response_object['message'] = 'Could not connect to plc'
#             return jsonify(response_object), 400
#         else:
#             response = plc_read_values(plc)
#             response_object['status'] = 'success'
#             response_object['message'] = 'Successfully scraped data.'
#             response_object['values'] = response
#             return jsonify(response_object), 200
#     except Exception as e:
#         return jsonify(response_object), 400


@plc_blueprint.route('/plc/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
