import re
import os
import time
import json
import descriptions

from io import StringIO
from openai import OpenAI
from dotenv import load_dotenv

import pandas as pd
import altair as alt


JSONIFY_DF_DICT = {}
SYSTEM_PROMPT = (
    "You are a helpful assistant that grabs the important keywords and arguments."
)

# Initialising the OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_response(llm, user_prompt):
    gpt_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    while True:
        time.sleep(10)
        response = client.chat.completions.create(
            model=llm,
            messages=gpt_messages,
            functions=descriptions.function_data_module
            + descriptions.function_plot_module,
            function_call="auto",
        )

        response_message = response.choices[0].message
        gpt_messages.append(response_message)

        if response.choices[0].finish_reason == "stop":
            return response_message.content

        elif response_message.function_call.name == "load_data":
            file_paths = json.loads(response_message.function_call.arguments).get(
                "file_paths"
            )

            for _, path in enumerate(file_paths):
                name = re.compile(r"(\w+).csv$").search(path).group(1)
                JSONIFY_DF_DICT[name] = load_data(path)

            gpt_messages.append(
                {
                    "role": "function",
                    "name": "load_data",
                    "content": json.dumps(JSONIFY_DF_DICT),
                }
            )

            return f"Loaded the data {file_paths} into the memory."

        # elif response_message.function_call.name == 'change_columns':
        #     from_cols = json.loads(response_message.function_call.arguments).get('from_col_names')
        #     to_cols = json.loads(response_message.function_call.arguments).get('to_col_names')

        #     messages.append({"role": "function", "name": "change_columns", "content": json.dumps(jsonify_df_dict)})

        elif response_message.function_call.name == "plot_scatter":
            data = json.loads(response_message.function_call.arguments).get("data")
            x = json.loads(response_message.function_call.arguments).get("x")
            y = json.loads(response_message.function_call.arguments).get("y")
            color = json.loads(response_message.function_call.arguments).get("color")
            
            if '.csv' in data:
                name = re.compile(r"(\w+).csv$").search(data).group(1)

            else:
                name = data
            plot = plot_scatter(pd.read_json(StringIO(JSONIFY_DF_DICT[name])), x, y, color)

            gpt_messages.append(
                {
                    "role": "function",
                    "name": "scatter_plot",
                    "content": plot,
                }
            )

            return plot


def load_data(file_path):
    """Load the data in the memory"""

    if not os.path.exists(file_path):
        return None

    return pd.read_csv(file_path).to_json()


def plot_scatter(data, x, y, color=None):
    if color:
        plot = (
            alt.Chart(data)
            .mark_point()
            .encode(
                x=alt.X(x).scale(zero=False),
                y=alt.Y(y).scale(zero=False),
                color=alt.Color(color),
            )
        )

    else:
        plot = (
            alt.Chart(data)
            .mark_point()
            .encode(
                x=alt.X(x).scale(zero=False),
                y=alt.Y(y).scale(zero=False),
            )
        )

    return plot


def plot_scatter_with_trendline(data, x, y, size, color=None):
    if color:
        points = (
            alt.Chart(data)
            .mark_point()
            .encode(
                x=alt.X(x).scale(zero=False),
                y=alt.Y(y).scale(zero=False),
                color=alt.Color(color),
            )
        )

        line = points.mark_line(size=size).transform_regression(x, y, groupby=[color])

    else:
        points = (
            alt.Chart(data)
            .mark_point()
            .encode(
                x=alt.X(x).scale(zero=False),
                y=alt.Y(y).scale(zero=False),
            )
        )

        line = points.mark_line(size=size).transform_regression(
            x,
            y,
        )

    plot = points + line
    return plot
