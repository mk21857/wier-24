# Connect to Flask API

import requests
from IPython.display import display, HTML

AUTH = ("admin", "admin") # Development authentication
ENDPOINT = "https://api:5000" # Accessible inside Docker network

def test_connection():
    response = requests.get(ENDPOINT + "/test_connection", verify = False, auth = AUTH)
    return response.json()

def get_frontier():
    return requests.get(ENDPOINT + "/get_frontier_pages", verify = False, auth = AUTH).json()['data']

# data = {
#     "url": 'https://example.com/page'
# }
def insert_page_into_frontier(data):
    return requests.post(ENDPOINT + "/insert_page_into_frontier", json=data, verify = False, auth = AUTH).json()

# data = {
#     "url": "https://example.com/page",
#     "page_type_code": "HTML",
#     "html_content": "<html><body>Sample HTML content</body></html>",
#     "http_status_code": 200,
#     "accessed_time": "2024-04-06T12:34:56"
# }
def update_page_data(data):
    return requests.post(ENDPOINT + "/update_page_data", json=data, verify = False, auth = AUTH).json()

def get_hashed_content():
    return requests.get(ENDPOINT + "/get_hashed_content", verify = False, auth = AUTH).json()['data']