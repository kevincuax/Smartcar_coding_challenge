import requests
import json

""" 
This file contains functions to implement Smartcar API.
Uses data obtained from GM API and returns data in suggested format
"""


#use GM API to get vehicle info
def get_vehicle_info(id):
  """ 
  Get vehicle info based on ID
  params: id(int) used to identify car
  returns: res, a json object with vehicle info
  """

  headers = {
    'Content-Type' : 'application/json'
  }
  params = {
    'id': id,
    'responseType': 'JSON'
  }

  response= requests.post('http://gmapi.azurewebsites.net/getVehicleInfoService', headers=headers, json=params)

  res = {}
  print(response.status_code, "STATS")
  if not response.ok:
    raise ValueError('404')
  response = response.json()

  if 'data' in response:
    data = response['data']
  else:
    raise ValueError('404')

  if 'vin' in data:
    vin = data['vin']['value']
  else:
    raise ValueError('no VIN')
    
  if 'color' in data:
    color = data['color']['value']
  else:
    raise ValueError('no color')

  #check if 2 door or 4 door car
  door_count = 0
  if 'fourDoorSedan' in data and 'twoDoorCoupe' in data:
    if data['fourDoorSedan']['value'] == 'True':
      door_count = 4
    elif data['twoDoorCoupe']['value'] == 'True':
      door_count = 2


    if 'driveTrain' in data:
      drive_train = data['driveTrain']['value']
    else:
      raise ValueError('no drive rain')
      
    
    res = {
      'vin': vin,
      'color': color,
      'doorCount': door_count,
      'driveTrain': drive_train
    }
    print(res)

  return res

#use GM API to get door info
def get_door_info(id):
  """ 
  function to get door info
  params: id(int), used to identify car
  returns: res, json object with door info
  """
  headers = {
    'Content-Type' : 'application/json'
  }

  params = {
    'id': id,
    'responseType': 'JSON'
  }

  response = requests.post('http://gmapi.azurewebsites.net/getSecurityStatusService', headers= headers, json=params)

  res = []

  #check if response code below 400
  if response.ok:
    response = response.json()

    if 'data' in response:
      data = response['data']
    else:
      raise ValueError('404')
    
    #check if expected data is there
    if 'doors' in data and 'values' in data['doors']:
        entries = data['doors']['values']
        for entry in entries:
          if entry['locked']['value'] == 'True':
            locked = True 
          elif entry['locked']['value'] == 'False':
            locked = False

          info = {
            'location': entry['location']['value'],
            'locked': locked
          }
          res.append(info)
    else:
        raise ValueError('No door info')
  else:
    response.raise_for_status()
  return res

def get_fuel_range(id):
  """  
  function to get fuel range based on ID
  params: id(int), used to identify car
  returns: res, json object with info on fuel for car
  """
  headers = {
    'Content-Type' : 'application/json'
  }
  params = {
    'id': id,
    'responseType': 'JSON'
  }

  response = requests.post('http://gmapi.azurewebsites.net/getEnergyService', headers=headers, json=params)
  res = {
    'percent': ''
  }

  #check if response code below 400
  if response.ok:
    response = response.json()
    if 'data' in response:
      data = response['data']
    else:
      raise ValueError('404')

    if 'tankLevel' in data and 'value' in data['tankLevel']:
      if data['tankLevel']['value'] != 'null':
        res['percent'] = float(data['tankLevel']['value'])
      else:
        res['percent'] = data['tankLevel']['value']
    else:
      raise ValueError('404')
  else:
    response.raise_for_status()
  
  return res

def get_battery_range(id):
  """ 
  function to get battery range for vehicle based on id
  params: id(int), ID used to identify vehicle
  return: res, a JSON object with info on battery percentage
  """
  headers = {
    'Content-Type': 'application/json',
  }
  params = {
    'id': id,
    'responseType': 'JSON'
  }

  response = requests.post('http://gmapi.azurewebsites.net/getEnergyService', headers= headers, json=params)
  res = {
    'percent':''
  }

  #check if response code below 400
  if response.ok:
    response = response.json()
    if 'data' in response:
      data = response['data']
    else:
      raise ValueError('404')
    
    if 'batteryLevel' in data and 'value' in data['batteryLevel']:
      if data['batteryLevel']['value'] != 'null':
        res['percent'] = float(data['batteryLevel']['value'])
      else:
        res['percent'] = data['batteryLevel']['value']
      
    else:      
      raise ValueError('404')
  else:
    response.raise_for_status()

  return res


def access_engine(id, command):
  """ 
  function to access engine
  params: id(int), used to identify vehicle
  returns: res, json object with info on if action worked
  """
  if command == 'START':
    command = 'START_VEHICLE'
  elif command == 'STOP':
    command = 'STOP_VEHICLE'
  else:
    raise ValueError('404')

  headers = {
    'Content-Type': 'application/json'
  }

  params = {
    'id': id,
    'command': command,
    'responseType': 'JSON'
  }

  response = requests.post('http://gmapi.azurewebsites.net/actionEngineService', headers=headers, json=params)

  res = {
    'status': '',
  }

  #check if response code below 400
  if response.ok:
    data = response.json() 
    print(data)
    if 'actionResult' in data:
      if data['actionResult']['status'] == 'EXECUTED':
        res['status'] = 'success'
      elif data['actionResult']['status'] == 'FAILED':
        res['status'] = 'error'
    else:
      raise ValueError('404')
  else:
    response.raise_for_status()
  return res
