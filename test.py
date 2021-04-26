import unittest
import Smartcar
import requests
from flask import abort

""" 
The purpose of this file is to test various API requests.
These tests will test the functions used for the requests and validate input/output
Make sure app is running before testing ('python app.py' to run app)
"""
class test_vehicle_info(unittest.TestCase):
    """ 
    Test get_vehicle_info function and validate input/output
    """

    #test for invalid input
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            Smartcar.get_vehicle_info(-1)
        with self.assertRaises(ValueError):
            Smartcar.get_vehicle_info('abc')
        with self.assertRaises(ValueError):
            Smartcar.get_vehicle_info('1234!')
        with self.assertRaises(ValueError):
            Smartcar.get_vehicle_info('.1234')
        with self.assertRaises(ValueError):
            Smartcar.get_vehicle_info('')
        with self.assertRaises(ValueError):
            Smartcar.get_vehicle_info('1 2 3')

    def test_valid_output(self):
        
        res = Smartcar.get_vehicle_info(1234)
        #check return values
        self.assertEqual(res['color'], 'Metallic Silver')
        self.assertEqual(res['doorCount'], 4)
        self.assertEqual(res['driveTrain'], 'v8')
        self.assertEqual(res['vin'], '123123412412')

        #check return types
        self.assertIs(type(res), dict)
        self.assertIs(type(res['color']), str)
        self.assertIs(type(res['doorCount']), int)
        self.assertIs(type(res['driveTrain']), str)
        self.assertIs(type(res['vin']), str)
        

class test_door_info(unittest.TestCase):
    """ 
    Test get_door_info and validate input/output
    """

    #test invalid input
    def test_validate_input(self):        
        with self.assertRaises(ValueError):
            Smartcar.get_door_info(-1)            
        with self.assertRaises(ValueError):
            Smartcar.get_door_info('abc')
        with self.assertRaises(ValueError):
            Smartcar.get_door_info('1234!')
        with self.assertRaises(ValueError):
            Smartcar.get_door_info('.1234')
        with self.assertRaises(ValueError):
            Smartcar.get_door_info('')
        with self.assertRaises(ValueError):
            Smartcar.get_door_info('1 2 3')

    def test_validate_output(self):        
        res = Smartcar.get_door_info(1234)
        #validating types
        self.assertIs(type(res), list)
        #check if correct amount of data returned
        self.assertEqual(len(res), 4)

        #check data types
        self.assertIs(type(res), list)
        for val in res:
            self.assertIs(type(val), dict)
            self.assertIs(type(val['locked']), bool)
            self.assertIs(type(val['location']), str)


class test_fuel(unittest.TestCase):
    """ 
    Test get_fueL_range and validate input/output
    """
    def test_validate_input(self):
        with self.assertRaises(ValueError):
            Smartcar.get_fuel_range(-1)
        with self.assertRaises(ValueError):
            Smartcar.get_fuel_range('abc')
        with self.assertRaises(ValueError):
            Smartcar.get_fuel_range('1234!')
        with self.assertRaises(ValueError):
            Smartcar.get_fuel_range('.1234')
        with self.assertRaises(ValueError):
            Smartcar.get_fuel_range('')
        with self.assertRaises(ValueError):
            Smartcar.get_fuel_range('1 2 3')
    
    def test_validate_output(self):
        #check if error raised for non fuel vehicle
        res = Smartcar.get_fuel_range(1234)
        #validate type
        self.assertIs(type(res['percent']), float)
        #check values returned
        self.assertGreaterEqual(res['percent'], 0)
        self.assertLessEqual(res['percent'], 100)

        #validate type and return value for 1234 vehicle
        res = Smartcar.get_fuel_range(1235)
        #str because null = str
        self.assertIs(type(res['percent']), str)
        self.assertEqual(res['percent'], 'null')


class test_battery(unittest.TestCase):
    """ 
    Test get_battery_range and validate input/output
    """

    def test_validate_input(self):
        with self.assertRaises(ValueError):
            Smartcar.get_battery_range(-1)
        with self.assertRaises(ValueError):
            Smartcar.get_battery_range('abc')
        with self.assertRaises(ValueError):
            Smartcar.get_battery_range('1234!')
        with self.assertRaises(ValueError):
            Smartcar.get_battery_range('.1234')
        with self.assertRaises(ValueError):
            Smartcar.get_battery_range('')
        with self.assertRaises(ValueError):
            Smartcar.get_battery_range('1 2 3')

    def test_validate_output(self):
        #check if error raised for non fuel vehicle
        res = Smartcar.get_battery_range(1235)
        #validate type
        self.assertIs(type(res['percent']), float)
        #check values returned
        self.assertGreaterEqual(res['percent'], 0)
        self.assertLessEqual(res['percent'], 100)

        #validate type and return value for 1234 vehicle
        res = Smartcar.get_battery_range(1234)
        self.assertIs(type(res['percent']), str)
        self.assertEqual(res['percent'], 'null')

class test_engine(unittest.TestCase):
    """ 
    Test access_engine function for valid input, output
    """
    def test_validate_input(self):
        with self.assertRaises(ValueError):
            Smartcar.access_engine(-1, 'START')
        with self.assertRaises(ValueError):
            Smartcar.access_engine('abc', 'START')
        with self.assertRaises(ValueError):
            Smartcar.access_engine('1234!', 'START')
        with self.assertRaises(ValueError):
            Smartcar.access_engine('.1234', 'START')
        with self.assertRaises(ValueError):
            Smartcar.access_engine('', 'START')
        with self.assertRaises(ValueError):
            Smartcar.access_engine('1 2 3', 'START')

        with self.assertRaises(ValueError):
            Smartcar.access_engine(-1, 'start')


    def test_validate_output(self):
        res = Smartcar.access_engine(1234, 'START')

        #validate data types
        self.assertIs(type(res), dict)
        self.assertIs(type(res['status']), str)

class test_get_post(unittest.TestCase):

    def test_vehicle_info(self):
        #test for good GET request response
        res = requests.get('http://localhost:5000/vehicles/1234')
        self.assertEqual(res.status_code, 200)
        res = res.json()
        self.assertEqual(res['color'], 'Metallic Silver')
        self.assertEqual(res['doorCount'], 4)
        self.assertEqual(res['driveTrain'], 'v8')
        self.assertEqual(res['vin'], '123123412412')

        #test for bad get request
        response = requests.get('http://localhost:5000/vehicles/1000000000')
        self.assertEqual(response.status_code, 404)

        #test for bad type of request
        response = requests.post('http://localhost:5000/vehicles/1234')
        self.assertEqual(response.status_code, 405)
    
    #values returned are random..hard to test need to figure out how to test that
    def test_security(self):        
        res = requests.get('http://localhost:5000/vehicles/1234/doors')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        #check right amount of data
        self.assertEqual(len(data), 4)

        #check for bad get request
        res = requests.get('http://localhost:5000/vehicles/12/doors')
        self.assertEqual(res.status_code, 404)
        
        #check for bad type of request
        res = requests.post('http://localhost:5000/vehicles/1234/doors')
        self.assertEqual(res.status_code, 405)
    
    def test_fuel(self):
        res = requests.get('http://localhost:5000/vehicles/1234/fuel')
        self.assertEqual(res.status_code, 200)
        data = res.json()

        print
        #validate type of data
        self.assertIs(type(data['percent']), float)
        #validate data values
        self.assertGreaterEqual(data['percent'], 0.0)
        self.assertLessEqual(data['percent'], 100.0)

        #test bad get request
        response = requests.get('http://localhost:5000/vehicles/1/fuel')
        self.assertEqual(response.status_code, 404)

        #test bad tyep of request
        response = requests.post('http://localhost:5000/vehicles/1234/fuel')
        self.assertEqual(response.status_code, 405)
    
    def test_engine(self):

        #test post request for starting vehicle
        response = requests.post('http://localhost:5000/vehicles/1234/engine', json={'action': 'START'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(data['status'], ['success', 'error'])

        #test post request for stopping vehicle
        response = requests.post(
            'http://localhost:5000/vehicles/1234/engine', json={'action': 'STOP'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(data['status'], ['success', 'error'])

        #test for bad actions
        response = requests.post(
            'http://localhost:5000/vehicles/1234/engine', json={'action': 'start'})
        self.assertEqual(response.status_code, 404)

        #test for bad actions
        response = requests.post(
            'http://localhost:5000/vehicles/1234/engine', json={'action': '123'})
        self.assertEqual(response.status_code, 404)
      
if __name__ == '__main__':
    unittest.main()
