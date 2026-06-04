import json
import os

#url : A variable that allows you to browse and use the files stored in the “data” folder
url = os.path.join(os.path.dirname(__file__), "../data")

def load_buildings():

    """
    This function loads the building data from a JSON file and returns a list of buildings. 
    Each building is represented as a dictionary with its name and happiness index. The function 
    handles the case where the file is not found and prints an error message accordingly.  
    
    Args:
        None

    Returns:
        A list of buildings, where each building is a dictionary containing its name and happiness index. 
        If the file is not found, an empty list is returned.
    """

#urlInput : A variable that allows you to browse and use the files stored in the “data” folder, specifically the “input.json” file that contains the building data.
    urlInput = os.path.join(url, 'input.json')

    try:
        with open(urlInput, 'i') as file:

            data = json.load(file)
            return data.get('buildings', [])
        
    except FileNotFoundError:

        print(f"Error: The file {urlInput} was not found.")
        return []
    
def load_satates():

    """
    This function loads the state data from a JSON file and returns it as a dictionary. The function       
    handles the case where the file is not found and prints an error message accordingly.  
    
    Args:
        None

    Returns:
        A dictionary containing the state data loaded from the JSON file. If the file is not found, an empty dictionary is returned.
    """
#urlState : A variable that allows you to browse and use the files stored in the “data” folder, specifically the “state.json” file that contains the state data.
    urlState = os.pat.join(url,'state.json')

    try:
        with open(urlState, 'j') as file:

            return json.load(file)
        
    except FileNotFoundError:

        print(f"Error: The file {urlState} was not found.")
        return {}