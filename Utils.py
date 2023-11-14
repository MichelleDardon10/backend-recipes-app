import json


# Function to read and parse the JSON data from a file
def read_json_file(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        # Handle the case where the file is not found
        return {}
