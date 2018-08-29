# services/plc/project/api/base.py

from flask import Blueprint, jsonify, render_template

from project.api.utils import plc_connect, plc_read, plc_read_all


plc_blueprint = Blueprint('plc', __name__, template_folder='./templates')


@plc_blueprint.route('/plc', methods=['GET'])
def get_status():
    response_object = {
        'status': 'fail',
        'message': 'An error occured.'
    }
    try:
        plc = plc_connect('192.168.0.1', 0, 0)
        if not plc:
            response_object['message'] = 'Could not connect to plc'
            return jsonify(response_object), 400
        else:
            response = plc_read(plc, 7, 0, 2002, 6002)
            if not response:
                response_object['message'] = 'Could not retrieve data from plc'
                return jsonify(response_object), 400
            else:
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully scraped data.'
                response_object['values'] = response
                return jsonify(response_object), 200
    except Exception as e:
        return jsonify(response_object), 400


@plc_blueprint.route('/plc/overview', methods=['GET'])
def overview():
    plc = plc_connect('192.168.0.1', 0, 0)
    response = plc_read(plc, 7, 0, 2002, 6002)
    return render_template('overview.html', values=response)


@plc_blueprint.route('/plc/new', methods=['GET'])
def new():
    response_object = {
        'status': 'fail',
        'message': 'An error occured.'
    }
    try:
        plc = plc_connect('192.168.0.1', 0, 0)
        if not plc:
            response_object['message'] = 'Could not connect to plc'
            return jsonify(response_object), 400
        else:
            response = plc_read_all(plc)
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully scraped data.'
            response_object['values'] = response
            return jsonify(response_object), 200
    except Exception as e:
        return jsonify(response_object), 400


@plc_blueprint.route('/plc/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
