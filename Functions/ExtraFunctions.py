
from  kiteconnect import KiteConnect
import datetime , requests


def send_to_telegram(message):

    apiToken = '6058041177:AAHhrqXPDRa1vghxQu_dTyTXTar1JRgNjCo'
    chatID = '1083941928'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)
        
def is_function_used_today(FunctionName):
    today = datetime.date.today()
    
    with open("Logs/" + FunctionName + ".txt", "a+") as file:
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            
            if str(today) in line:
                
                return True
        
        # file.write(str(today) + "\n")
        return False

def CompareTime(TimeInput):

    current_time = datetime.datetime.now().time()
    given_time_str = TimeInput # Replace this with the desired time
    given_time = datetime.datetime.strptime(given_time_str, "%H:%M:%S").time()
    # print(current_time , given_time)
    
    if given_time <= current_time:
        return True 
    else :  return False
    
    
def ZerodhaApiLogin(Credentials):
    file = open("Access_Tokens/"+Credentials["user_id"] + '.txt', 'r')

    Credentials['access_token'] = file.read()
    api = KiteConnect(api_key=Credentials["api_key"])
    api.set_access_token(Credentials["access_token"])
    api.profile()
    return {"Cred" :Credentials , "API":api}

import time

from prettytable import PrettyTable

def flatten_dict(data, parent_key='', sep='_'):
    """
    Function to flatten a nested dictionary.
    """
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def display_data_in_table(data):
    # Create a table object
    table = PrettyTable()

    # Flatten the nested dictionary (if any) into a flat dictionary
    flattened_data = flatten_dict(data)

    # Extract keys (column names) and values from the flattened dictionary
    column_names = list(flattened_data.keys())
    values = list(flattened_data.values())

    # Define table headers
    table.field_names = column_names

    # Add rows to the table
    table.add_row(values)

    # Set table alignment (optional)
    for header in table.field_names:
        table.align[header] = "l"  # Left align columns

    # Print the table
    print(table)
    
from tabulate import tabulate

def display_arrays_and_objects(data):
    """
    Display arrays' content vertically and objects' content in separate tables.

    Args:
    - data (dict): Dictionary containing arrays and objects.
    """

    arrays = {}
    objects = {}

    # Group arrays and objects
    for key, value in data.items():
        if isinstance(value, list):
            arrays[key] = value
        elif isinstance(value, dict):
            objects[key] = value

    # Display arrays' content vertically
    headers = []
    table = []
    
    for key in arrays:
        # print(key)
        headers.append(key)
        newTab = ""
        for i in arrays[key]:
            # print(i)
            newTab =newTab + str(i) + "\n"
            # print(newTab)
        table.append(newTab)
    table = [table]
    # table = [ [[" efw"] , ["wfwe"]]]
    # print(table)
    
    print(tabulate(table, headers = headers ,tablefmt="fancy_grid" ))
  
    # print("Objects:")
    for key, value in objects.items():
        print(f"Object {key}:")
        for sub_key, sub_value in value.items():
            print(f"{sub_key}:" , sub_value)
            
            print()

# Example object containing arrays and objects
