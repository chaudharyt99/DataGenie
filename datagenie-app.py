import time
import functions

import pandas as pd
import streamlit as st


# Function to clear chat history
def clear_chat_history():
    st.session_state.app_messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


# Building the app here
st.set_page_config(page_title="DataGenie 🧞‍♂️💬")

with st.sidebar:
    st.title("DataGenie 🧞‍♂️")
    st.write(
        """Your GenAI wizard, fueled by OpenAI's GPT-3.5! Transform natural language into
        data tasks effortlessly - plots, ML pipelines, and more in a chat."""
    )

    st.subheader("Upload data (or write a query)")
    uploaded_files = st.file_uploader("Choose a .csv file", accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        progress_text = f"Uploading {uploaded_file.name}. Please wait."
        my_bar = st.progress(0, text=progress_text)
        dataframe = pd.read_csv(uploaded_file)
        time.sleep(1)
        my_bar.progress(100, text=progress_text)
        time.sleep(1)
        my_bar.empty()

        st.success(f"{uploaded_file.name} uploaded successfully!", icon="✅")

    st.subheader("Models and parameters")
    selected_model = st.sidebar.selectbox(
        "Choose an OpenAI model", ["GPT-3.5", "GPT-4"], key="selected_model"
    )
    if selected_model == "GPT-3.5":
        llm = "gpt-3.5-turbo"
    elif selected_model == "GPT-4":
        llm = "gpt-4"

    st.markdown(
        "📖 Learn how to build this app in this [GitHub repo](https://github.com/chaudharyt99/DataGenie)"
    )

# Store LLM generated responses
if "app_messages" not in st.session_state.keys():
    st.session_state.app_messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]

# Display the chat messages
for app_message in st.session_state.app_messages:
    with st.chat_message(app_message["role"]):
        if isinstance(app_message["content"], str):
            st.write(app_message["content"])

        else:
            st.altair_chart(st.session_state.chart, theme=None, use_container_width=True)

st.sidebar.button("Clear Chat History", on_click=clear_chat_history)


# User-provided prompt
if prompt := st.chat_input(disabled=False):
    st.session_state.app_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.app_messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = functions.generate_response(llm, prompt)

            if isinstance(response, str):
                placeholder = st.empty()
                full_response = ""
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
                message = {"role": "assistant", "content": response}

            else:
                st.session_state.chart = response
                st.altair_chart(st.session_state.chart, theme=None, use_container_width=True)
                message = {"role": "assistant", "content": st.session_state.chart}

    st.session_state.app_messages.append(message)
