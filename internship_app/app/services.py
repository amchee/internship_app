import requests

def get_data_from_external_api():
    response = requests.get('https://api.example.com/data')
    return response.json()
