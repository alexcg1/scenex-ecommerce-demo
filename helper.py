import base64
import json
import logging
import os

import requests
from rich.console import Console
from rich.logging import RichHandler

SCENEX_KEY = os.environ.get("SCENEX_KEY", None)
# from creds import SCENEX_KEY

console = Console()

# set up logging
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")

LANGUAGES = {
    "English": "en",
    "German": "de",
    "French": "fr",
    "Italian": "it",
    "Spanish": "es",
    "Portuguese": "pt",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "Esperanto": "eo",
    "Estonian": "et",
    "Finnish": "fi",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish (Kurmanji)": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog (Filipino)": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}


def image_to_data_uri(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_image}"


def bytes_to_data_uri(bytes_data, mime_type="image/png"):
    encoded_image = base64.b64encode(bytes_data).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_image}"


def process_image(
    image_url: str,
    features: list = [],
    task_id: str = "",
    question: str = "",
    json_schema: str = "",
    languages: list = ["en"],
    output_length: int = 0,
    cid: str = "",
):
    headers = {
        "x-api-key": f"token {SCENEX_KEY}",
        "content-type": "application/json",
    }
    data = {
        "data": [
            {
                "image": image_url,
                "features": features,
                "task_id": task_id,
                "question": question,
                "json_schema": json_schema,
                "languages": languages,
                "output_length": output_length,
                "cid": cid,
            },
        ]
    }

    log.info(f"Sending {image_url}")
    response = requests.post(
        "https://api.scenex.jina.ai/v1/describe", headers=headers, json=data
    )
    return response.json()
