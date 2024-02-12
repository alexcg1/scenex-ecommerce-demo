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
