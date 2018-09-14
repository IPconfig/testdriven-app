# services/plc/project/api/base.py

from sqlalchemy import exc
from flask import Blueprint, jsonify, render_template

from project import db
from project.api.models import Plc, PLCDBSchema, Plc_db
from project.api.utils import plc_connect, plc_read_values, read_plc


plc_blueprint = Blueprint('plc', __name__, template_folder='./templates')


@plc_blueprint.route('/plc', methods=['GET'])
def get_status():
    response_object = {
        'status': 'fail',
        'message': 'An error occured.'
    }
    try:
        client = Plc.query.first()
        plc = plc_connect(adress=client.ip, rack=client.rack, slot=client.slot)
        if not client:
            response_object['message'] = 'No PLC connfigured in database'
            return jsonify(response_object), 400
        if not plc:
            response_object['message'] = 'Could not connect to plc'
            return jsonify(response_object), 400
        else:
            dbo = read_plc(plc)
            if not dbo:
                response_object['message'] = 'Could not retrieve data from plc'
                return jsonify(response_object), 400
            else:
                try:
                    reactor = Plc_db.query.filter_by(plc_id=client.id).first()
                    if not reactor:
                        dbo.plc_id = client.id  # add plc id as FK to dataset
                        db.session.add(dbo)
                        db.session.commit()
                        plcdb_schema = PLCDBSchema()
                        result = plcdb_schema.dump(dbo)
                        response_object['status'] = 'success'
                        response_object['message'] = 'PLC data saved in db'
                        response_object['plc db'] = result
                        return jsonify(response_object), 200
                    else:
                        # update values with new readings
                        reactor.tube_state_client = dbo.tube_state_client
                        db.session.add(reactor)
                        db.session.commit()
                        response_object['status'] = 'success'
                        response_object['message'] = 'PLC data updated in db'
                        plcdb_schema = PLCDBSchema()
                        result = plcdb_schema.dump(reactor)
                        response_object['plc db'] = result
                        return jsonify(response_object), 200
                except (exc.IntegrityError, ValueError, Exception) as e:
                    # db.session.rollback()
                    response_object['error'] = e
                    return jsonify(response_object), 400
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
#         dbo = Plc_db.query.filter_by(plc_id=1).first()
#         plcdb_schema = PLCDBSchema()
#         result = plcdb_schema.dump(dbo)
#         response_object['status'] = 'success'
#         response_object['message'] = 'PLC data retrieved from db'
#         response_object['result'] = result
#         return jsonify(response_object), 200

#     except (exc.IntegrityError, ValueError, Exception) as e:
#         response_object['error'] = e
#         return jsonify(response_object), 400


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
            response = plc_read_values(plc)
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
