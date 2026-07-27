# test_wmata_api.py

from wmata_api import app
import json
import unittest
 
class WMATATest(unittest.TestCase):
    # ensure both endpoints return a 200 HTTP code
    def test_http_success(self):
        escalator_response = app.test_client().get('/incidents/escalators').status_code
        self.assertEqual(escalator_response, 200)
 
        elevator_response = app.test_client().get('/incidents/elevators').status_code
        self.assertEqual(elevator_response, 200)
 
################################################################################
 
    # ensure all returned incidents have the 4 required fields
    def test_required_fields(self):
        required_fields = ["StationCode", "StationName", "UnitType", "UnitName"]
 
        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())
 
        for incident in json_response:
            for field in required_fields:
                self.assertIn(field, incident)
 
################################################################################
 
    # ensure all entries returned by the /escalators endpoint have a UnitType of "ESCALATOR"
    def test_escalators(self):
        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())
 
        for incident in json_response:
            self.assertEqual(incident["UnitType"], "ESCALATOR")
 
################################################################################
 
    # ensure all entries returned by the /elevators endpoint have a UnitType of "ELEVATOR"
    def test_elevators(self):
        response = app.test_client().get('/incidents/elevators')
        json_response = json.loads(response.data.decode())
 
        for incident in json_response:
            self.assertEqual(incident["UnitType"], "ELEVATOR")
 
################################################################################
 