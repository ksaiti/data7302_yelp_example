import json
import pandas as pd

def flatten_json(data, parent_key="", seperator=""):

    # Recursively flatten a nested JSON dictionary.

    # Parameters (inputs to the function)
    #data (dict): the JSON object to flatten
    #parent_key(str): the prefix for nested keys
    #seperator(str): the symbol used to join parent and child keys

    # Return: flattened dictionary

    items ={} # store flattened key-value pairs

    #Loop through each key-value in the JSON object
    for key, value in data.items():
        #build the new key name
        #example: attributes + "_" + BikeParking --> attributes_BikeParking
        new_key = parent_key + seperator + key if parent_key else key

        # if the value is another dictionary, flatten recursively
        if isinstance(value, dict):
            items.update(
                flatten_json(value, new_key, seperator)
            )
        #if the value is a list, convert it to string
        elif isinstance(value, list):
            items[new_key] = str(value)
        
        #otherwise, if it is a normal value, sfetsch the value and store it 
        else:
            items[new_key] = value
    return items

def auto_flatten_file(input_file, output_file):
    #Read a JSON file, flatten each JSON record, save the result in a csv

    rows = []

    with open(input_file, "r", encoding="utf-8") as f:

        #process the file line by line
        for line in f:

            #convert the JSON text into a python dictionary
            data = json.loads(line)

            #flatten the dictionary automatically
            flat_record = flatten_json(data)

            #add to the list of rows
            rows.append(flat_record)
    
    df = pd.DataFrame(rows)

    print(df.columns)

    #save to a csv
    df.to_csv(output_file, index=False)