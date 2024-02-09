import os

import streamlit as st
import yaml
from rich.console import Console

from helper import LANGUAGES, image_to_data_uri, process_image

console = Console()

st.set_page_config(page_title="SceneXplain eCommerce Demo", layout="wide")

st.title("SceneXplain eCommerce Demo")

settings = {}

st.sidebar.title("About SceneXplain")
st.sidebar.markdown(
    "SceneXplain is your go-to solution for advanced image captioning and video summarization. Powered by Jina AI's cutting-edge multimodal algorithms, SceneXplain effortlessly converts visuals into captivating textual narratives, pushing beyond conventional captioning boundaries. With an intuitive interface and robust API integration, it's tailored for both seasoned users and developers alike. Opt for SceneXplain for unmatched visual comprehension, meticulously designed with innovation, precision, and expertise."
)

example_tab, live_tab = st.tabs(["Example outputs", "Live"])

with open("products.yaml") as file:
    data = yaml.safe_load(file)
    products = data["products"]

with open("prompts.yml") as file:
    data = yaml.safe_load(file)
    prompts = data["prompts"]
    jsons = data["json"]

with example_tab:
    for product in products:
        name = product["name"]
        st.markdown(f"#### {name}")

        # Create a row for each product
        cols = st.columns([1, 3])  # Adjust the ratio as needed
        with cols[0]:
            st.image(product["images"][0]["url"])
        with cols[1]:
            st.markdown("##### Generated description")
            st.markdown(
                ':gray[Prompt: "_Create an attractive and SEO friendly product description for use in an ecommerce website. It should make the product sound attractive and entice users to purchase it_"]'
            )
            st.markdown(product["desc"])
            st.markdown("##### Generated JSON")
            st.markdown(":gray[_Define your custom JSON Schema with specific fields_]")
            st.json(product["json"])

        st.markdown("##### Generated alt texts")

        alt_cols = st.columns(len(product["images"]))

        # Populate the first row with images
        for col, img in zip(alt_cols, product["images"]):
            with col:
                st.image(img["url"], width=100)

        # Create another set of dynamic columns for the alt texts
        alt_text_cols = st.columns(len(product["images"]))

        # Populate the second row with alt texts
        for col, img in zip(alt_text_cols, product["images"]):
            with col:
                st.markdown(img["alt"])

        st.divider()

with live_tab:
    tasks = ["Alt text", "Caption", "Product description", "Structured JSON"]
    # Create two columns and rename them as requested
    task_col, lang_col, source_col = st.columns(3)

    # Place a selectbox in each column using the new names
    with task_col:
        task = st.selectbox(label="Task", options=tasks)

    with lang_col:
        language = st.selectbox(label="Language", options=LANGUAGES.keys())
        lang_code = LANGUAGES[language]

    with source_col:
        input_source = st.selectbox(
            label="Input source", options=["Presets", "URL", "Upload"]
        )
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
                    if st.checkbox("Select", key=f"cb_{i}"):
                        selected_image_index = i

        # Display the selected image index
        if selected_image_index is not None:
            product = products[selected_image_index]
            url = products[selected_image_index]["images"][0]["url"]
            operation = product["name"]

    elif input_source == "URL":
        selected_image_index = None
        url = st.text_input(label="URL")
        operation = url.split("/")[-1]

    elif input_source == "Upload":
        selected_image_index = None
        uploaded_file = st.file_uploader("Upload a file")
        if uploaded_file is not None:
            # Define the path where you want to save the file
            save_path = "uploads"
            file_path = os.path.join(save_path, uploaded_file.name)

            # Write the contents of the uploaded file to the new file.
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            operation = uploaded_file.name
            url = image_to_data_uri(file_path)

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
            question = prompts["product_desc"] % product["name"]
            features = ["question_answer"]
        elif task == "Structured JSON":
            features = ["json"]
            json_schema = jsons["apparel"] % product["name"]

        with st.spinner(text=f"Creating **{task}** for **:blue[{operation}]**"):
            output = process_image(
                image_url=url,
                languages=[lang_code],
                features=features,
                task_id=task_id,
                question=question,
                json_schema=json_schema,
            )

            text = output["result"][0]["i18n"][lang_code]

        if "output" in locals():
            st.markdown(f"#### {task}")
            if task == "Structured JSON":
                st.json(text)
            else:
                st.write(text)
