# services/plc/project/api/base.py

from sqlalchemy import exc
from flask import Blueprint, jsonify, render_template

from project import db
from project.api.models import Plc, Reactor
from project.api.util_db import DB
from project.api.plc import read_plc
from project.api.utils import plc_connect, plc_read_values


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
        if not plc:
            response_object['message'] = 'Could not connect to plc'
            return jsonify(response_object), 400
        else:
            response = plc_read_all(plc)
            response
            if not response:
                response_object['message'] = 'Could not retrieve data from plc'
                return jsonify(response_object), 400
            else:
                try:
                    for row_array, values in enumerate(response):
                        row = row_array + 1  # arrays are 0-indexed
                        response_object['row'] = row
                        response_object['values'] = values

                        #  read row and data from db
#                        reactor_row = Reactor.query.filter_by(
#                                                        reactor_id=1,
#                                                        row=row,
#                                                        plc=client).first()
                        
                        #  save to database or update exisiting row
 #                       if (reactor_row == row and plc == client):
 #                           reactor_row.values = values  # update values
 #                       else:
 #                           db.session.add(Reactor(
 #                               reactor_id=1,
 #                               row=row,
 #                               values=values,
 #                               plc=client,
 #                           ))
 #                   db.session.commit()
                    response_object['status'] = 'success'
                    response_object['message'] = 'Successfully put data in db.'
 #                   response_object['reactor row'] = reactor_row
                    return jsonify(response_object), 200
                except (exc.IntegrityError, ValueError) as e:
                    db.session.rollback()
                    return jsonify(response_object), 400
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
