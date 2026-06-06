# ==========================================
# Team Number: 3
# Variant Name: bridge.py
# Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
# ==========================================


import json
import os

url = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data")))

def load_buildings():

    urlInput = os.path.join(url, 'input.json')

    try:
        with open(urlInput, 'r') as file:
            data = json.load(file)
            return data.get('buildings', [])
        
    except FileNotFoundError:

        print(f"Error: The file {urlInput} was not found.")
        return []
    
def load_states():
    urlState = os.path.join(url, 'state.json')
    try:
        with open(urlState, 'r') as file:
            return json.load(file)
        
    except FileNotFoundError:

        print(f"Error: The file {urlState} was not found.")
        return {}
    