# Smartcar Backend Challenge

## How to Use
This project uses Flask and contains all routes contained in the challenge. Currently, the app must be ran locally.
To run, run `python app.py` and open 'localhost:5000/$route in browser e.g. http://localhost:5000/vehicles/1234
example response:
```json{
"color": "Metallic Silver",
"doorCount": 4,
"driveTrain": "v8",
"vin": "123123412412"
}
```

## Test Cases
I wrote unit tests in test.py. These tests validate things like error codes, correct input/output, data types, etc.
One thing I didn't get a chance to do but should have is validating format for parameters, e.g. making sure ID is int.
