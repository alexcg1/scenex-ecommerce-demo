import os

import streamlit as st
import yaml
from rich.console import Console

from helper import (LANGUAGES, Components, Style, bytes_to_data_uri,
                    image_to_data_uri, process_image)

console = Console()

st.set_page_config(page_title="SceneXplain eCommerce Demo", layout="wide")
Style.page_menu_css()
Components.sidebar()

st.title("SceneXplain eCommerce Demo")

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

st.markdown("### Behind the scenes")

st.markdown(
    "This web app uses [SceneXplain's API](https://scenex.jina.ai/api) to generate alt texts, products descriptions and JSON output."
)
st.markdown("##### JSON Schema")
st.markdown(
    "With a JSON Schema you can define your output data format, making it easier to integrate SceneXplain with your existing tech stack."
)
with open("data/product.json") as file:
    st.json(file.read())
