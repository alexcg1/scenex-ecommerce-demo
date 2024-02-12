import os

import streamlit as st
import yaml
from rich.console import Console

from helper import (LANGUAGES, Components, Style, bytes_to_data_uri,
                    image_to_data_uri, process_image)

console = Console()
st.set_page_config(page_title="SceneXplain eCommerce Demo", layout="wide")

Style.page_menu_css()
sidebar = Components.sidebar()


settings = {}

# st.sidebar.title("About SceneXplain")
# st.sidebar.markdown(
# "SceneXplain is your go-to solution for advanced image captioning and video summarization. Powered by Jina AI's cutting-edge multimodal algorithms, SceneXplain effortlessly converts visuals into captivating textual narratives, pushing beyond conventional captioning boundaries. With an intuitive interface and robust API integration, it's tailored for both seasoned users and developers alike. Opt for SceneXplain for unmatched visual comprehension, meticulously designed with innovation, precision, and expertise."
# )

# with st.sidebar.expander(label="QR codes"):
# st.markdown("### SceneXplain")
# st.image("./data/qr_codes/scenex_url.png")
# st.markdown("### eCommerce demo")
# st.image("./data/qr_codes/scenex_demo.png")

# debug = st.sidebar.toggle("Debug mode")

with open("data/products.yml") as file:
    data = yaml.safe_load(file)
    products = data["products"]

with open("data/prompts.yml") as file:
    data = yaml.safe_load(file)
    prompts = data["prompts"]
    jsons = data["json"]

tasks = [
    "Alt text",
    "Caption",
    "Product description",
    "Structured JSON",
    "Custom question",
]
# Create two columns and rename them as requested
source_col, task_col, lang_col = st.columns(3)

# Place a selectbox in each column using the new names
with source_col:
    input_source = st.selectbox(
        label="Input source", options=["Presets", "URL", "Upload", "Webcam"]
    )
with task_col:
    task = st.selectbox(label="Task", options=tasks)

with lang_col:
    language = st.selectbox(label="Language", options=LANGUAGES.keys())
    lang_code = LANGUAGES[language]

if task == "Custom question":
    question_text = st.text_input(label="Question")
# task = st.selectbox(label="Task", options=tasks)

# language = st.selectbox(label="Language", options=LANGUAGES.keys())
# lang_code = LANGUAGES[language]

if input_source == "Presets":
    selected_image_index = None

    # Create two rows: one for images and one for checkboxes
    with st.container():
        cols_img = st.columns(len(products))
        cols_cb = st.columns(len(products))

        for i, product in enumerate(products):
            # Display image in the top row
            with cols_img[i]:
                st.image(
                    product["images"][0]["url"], width=300
                )  # Adjust width as needed

            # Display checkbox in the second row
            with cols_cb[i]:
                # Unique key for each checkbox to work properly
                if st.checkbox(f"{product['name']}", key=f"cb_{i}"):
                    selected_image_index = i

    # Display the selected image index
    if selected_image_index is not None:
        product = products[selected_image_index]
        url = products[selected_image_index]["images"][0]["url"]
        operation = product["name"]
        insert_text = product["name"]

elif input_source == "URL":
    selected_image_index = None
    url = st.text_input(label="URL")
    operation = url.split("/")[-1]
    insert_text = ""

elif input_source == "Upload":
    selected_image_index = None
    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file is not None:
        save_path = "uploads"
        file_path = os.path.join(save_path, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        operation = uploaded_file.name
        url = image_to_data_uri(file_path)
        insert_text = ""

elif input_source == "Webcam":
    picture = st.camera_input("Take a picture")

    if picture is not None:
        bytes_data = picture.getvalue()
        url = bytes_to_data_uri(bytes_data, mime_type="image/png")
        operation = "Webcam photo"

run_button = st.button("Run task")
if run_button:
    # set default values
    task_id, question, json_schema = "", "", ""
    features = []

    if task == "Caption":
        task_id = "caption"
    elif task == "Alt text":
        task_id = "alt_text"
    elif task == "Product description":
        features = ["question_answer"]
        question = prompts["product_desc"] % product["name"]
    elif task == "Structured JSON":
        features = ["json"]
        json_schema = jsons["apparel"] % insert_text
    elif task == "Custom question":
        features = ["question_answer"]
        question = question_text

    with st.spinner(text=f"Creating **{task}** for **:blue[{operation}]**"):
        output = process_image(
            image_url=url,
            languages=[lang_code],
            features=features,
            task_id=task_id,
            question=question,
            json_schema=json_schema,
        )

    if "output" in locals():
        text = output["result"][0]["i18n"][lang_code]
        st.markdown(f"#### {task}")
        if task == "Structured JSON":
            st.json(text)
        else:
            st.write(text)

        if sidebar["debug"]:
            st.markdown("#### Raw response")
            st.json(output)
