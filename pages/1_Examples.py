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


# st.title("SceneXplain eCommerce Demo")

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

# (
# example_tab,
# live_tab,
# bts_tab,
# ) = st.tabs(["Example outputs", "Live", "Behind the scenes"])

with open("data/products.yml") as file:
    data = yaml.safe_load(file)
    products = data["products"]

with open("data/prompts.yml") as file:
    data = yaml.safe_load(file)
    prompts = data["prompts"]
    jsons = data["json"]

# with example_tab:
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
