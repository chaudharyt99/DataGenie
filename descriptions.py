import classes

function_data_module = [
    {
        "name": "load_data",
        "description": "Load the specified file into a pandas DataFrame.",
        "parameters": classes.LoadDataFrame.model_json_schema(),
    },
    {
        "name": "change_columns",
        "description": "Change the column names in a pandas DataFrame.",
        "parameters": classes.ChangeColumnNames.model_json_schema(),
    },
]

function_plot_module = [
    {
        "name": "plot_scatter",
        "description": "Create a scatter plot between two columns of a pandas DataFrame. Optionally, add color and size as well.",
        "parameters": classes.ScatterPlot.model_json_schema(),
    },
    {
        "name": "plot_line",
        "description": "Create a line plot between two columns of a pandas DataFrame. Optionally, add color and size as well.",
        "parameters": classes.LinePlot.model_json_schema(),
    },
    {
        "name": "plot_bubble",
        "description": "Create a bubble plot between two columns of a pandas DataFrame. Optionally, add color and size as well.",
        "parameters": classes.ScatterPlot.model_json_schema(),
    },
    {
        "name": "plot_area",
        "description": "Create an area plot between two columns of a pandas DataFrame. Optionally, add color and size as well.",
        "parameters": classes.LinePlot.model_json_schema(),
    },
]
