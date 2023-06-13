from main import app
from flask import request, jsonify, Response, json
import requests as db

# Define Flask routes


@app.route("/")
def index():
    return "Hello from Colab!"


@app.route('/getVesselById', methods=['GET'])
def getVesselById():
    id = request.args.get('id', default=1, type=int)
    result = db.getVesselById(id)
    response = Response(result, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/getVessels', methods=['GET'])
def getVessels():
    result = db.getVessels()
    response = Response(result, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/getVesselPathById', methods=['GET'])
def getVesselPathById():
    id = request.args.get('id', default=1, type=int)
    timeframe_min = request.args.get('timeframe_min', default=1, type=int)
    current_time = request.args.get(
        'current_time', default='2022-03-13T12:00:00', type=str)
    result = db.getVesselPathById(id, timeframe_min, current_time)
    response = Response(result, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/getVesselsInElapsedTime', methods=['GET'])
def getVesselsInElapsedTime():
    timeframe_min = request.args.get('timeframe_min', default=10, type=int)
    current_time = request.args.get(
        'current_time', default='2022-03-13T12:00:00', type=str)
    result = db.getVesselsInElapsedTime(timeframe_min, current_time)
    response = Response(result, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/getAllVesselsInElapsedTime', methods=['GET'])
def getAllVesselsInElapsedTime():
    timeframe_min = request.args.get('timeframe_min', default=10, type=int)
    current_time = request.args.get(
        'current_time', default='2022-03-13T12:00:00', type=str)
    result = db.getAllVesselsInElapsedTime(timeframe_min, current_time)
    response = Response(result, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/uploadAreaJson', methods=['POST'])
def uploadAreaJson():
    areaJson = request.get_json(silent=True)
    if areaJson is None:
        areaJson = []
    db.uploadAreaJson(areaJson)
#  result = db.getVesselsInElapsedTime(timeframe_min, current_time)
    error = json.dumps({'error': "There is an error"})
    response = Response(error, status=200, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/summary')
def summary():
    data = {}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
