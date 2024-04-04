# Connect to Flask API

import requests
from IPython.display import display, HTML

AUTH = ("admin", "admin") # Development authentication
ENDPOINT = "https://api:5000" # Accessible inside Docker network

def test_connection():
    response = requests.get(ENDPOINT + "/test_connection", verify = False, auth = AUTH)
    # return response.json()
    return 'asdasdasd'