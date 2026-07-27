# wmata_api

import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "49ca48ca0ecd4c6dbe64435c1807a184" # https://developer.wmata.com/demokey
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
  # create an empty list called 'incidents'
  incidents = []

  # use 'requests' to do a GET request to the WMATA Incidents API
  # retrieve the JSON from the response
  response = requests.get(INCIDENTS_URL, headers=headers)
  data = response.json()

  # iterate through the JSON response and retrieve all incidents matching 'unit_type'
  # unit_type param will be "elevators" or "escalators"; WMATA returns "ELEVATOR" or "ESCALATOR"
  unit_type_filter = unit_type.rstrip("s").upper()  # "elevators" -> "ELEVATOR", "escalators" -> "ESCALATOR"

  for incident in data.get("ElevatorIncidents", []):
    if incident.get("UnitType") == unit_type_filter:
      # create a dictionary containing the 4 fields from the Module 7 API definition
      incident_dict = {
        "StationCode": incident.get("StationCode"),
        "StationName": incident.get("StationName"),
        "UnitName": incident.get("UnitName"),
        "UnitType": incident.get("UnitType")
      }
      incidents.append(incident_dict)

  # return the list of incident dictionaries using json.dumps()
  return json.dumps(incidents)

if __name__ == '__main__':
    app.run(debug=True)