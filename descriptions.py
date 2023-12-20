import classes

function_data_module = [
    {
        "name": "load_data",
        "description": "Load the specified file into a pandas DataFrame.",
        "parameters": classes.DataFrame.model_json_schema(),
    }
]