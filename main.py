import os
import json
import dotenv
import functions
import descriptions

from openai import OpenAI

if __name__ == "__main__":
    dotenv.load_dotenv()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    user_query = input("Enter your query: ")
    messages.append({"role": "user", "content": user_query})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=descriptions.function_data_module,
        function_call="auto",
    )

    output = completion.choices[0].message

    if output.function_call.name == "load_data":
        args = json.loads(output.function_call.arguments).get("file_paths")
        df_dict = {}

        for idx, path in enumerate(args):
            df_dict[idx] = functions.load_data(path)
            print(f"loaded {path}")
