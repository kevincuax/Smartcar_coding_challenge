from flask import Flask, abort, request, jsonify
import json
import Smartcar
import logging

app = Flask("Smartcar API")

#Route to get vehicle info
@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle_info(id):
  if(request.method == 'GET'):
    try:
      res = Smartcar.get_vehicle_info(id)
      return jsonify(res)
    except ValueError as e:
      print(e, "EEEEEEE")
      if str(e) == '404':
        abort(404, 'Vehicle info not found')
      else:
        abort(400, e)
  else:
    abort(405, 'Wrong method')

#route for door info
@app.route('/vehicles/<int:id>/doors', methods=['GET'])
def get_door_status(id):
  if(request.method == 'GET'):
    try:
      res = Smartcar.get_door_info(id)
      return jsonify(res)
    except ValueError as e:
      print(e, "EEEEEEE")
      if str(e) == '404':
        abort(404, 'Vehicle info not found')
      else:
        abort(400, e.message)
  else:
    abort(405, 'Wrong method')
		
#route to get fuel info
@app.route('/vehicles/<int:id>/fuel', methods=['GET'])
def get_fuel_range(id):
  if(request.method == 'GET'):
    try:
      res = Smartcar.get_fuel_range(id)
      return jsonify(res)
    except ValueError as e:
      print(e, "EEEEEEE")
      if str(e) == '404':
        abort(404, 'Vehicle info not found')
      else:
        abort(400, e.message)
  else:
    abort(405, 'Wrong method')

#route to get battery info
@app.route('/vehicles/<int:id>/battery', methods=['GET'])
def get_battery_range(id):
  if(request.method == 'GET'):
    try:
      res = Smartcar.get_battery_range(id)
      return jsonify(res)
    except ValueError as e:
      print(e, "EEEEEEE")
      if str(e) == '404':
        abort(404, 'Vehicle info not found')
      else:
        abort(400, e.message)
  else:
    abort(405, 'Wrong method')
    
#route to start or stop vehicle
@app.route('/vehicles/<int:id>/engine', methods=['POST'])
def access_engine(id):
  if request.method =='POST':
    request_json = request.get_json()
    action = request_json.get('action')
    
    try:
      res = Smartcar.access_engine(id, action)
    except ValueError as e:
      if str(e)== '404':
        abort(404, 'Vehicle info not found')
      else:
        print(e)
        abort(400, e)
    return jsonify(res)
  else:
    abort(405, 'Wrong method')

if __name__ == '__main__':
  app.run(debug=True)
