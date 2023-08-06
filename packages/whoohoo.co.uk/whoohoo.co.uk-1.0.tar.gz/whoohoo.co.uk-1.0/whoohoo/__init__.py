"""
A Module that allows you to use www.whoohoo.co.uk to translate texts into different dialects.
Works using BeautifulSoup4 and requests.

LICENSED UNDER THE WTFPL (DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE), SEE LICENSE.txt
NO COPYRIGHT WHATSOEVER
"""

import requests
from bs4 import BeautifulSoup as bs
from enum import Enum


class WhooHooTranslatorType(Enum):

    alig = "alig"
    cockney = "cockney"
    upnorf = "upnorf"
    irish = "irish"
    brummie = "brummie"
    geordie = "geordie"
    posh = "posh"
    scottie = "scottie"
    scouse = "scouse"


class WhooHooTranslator:

    def __init__(self, translator_type):
        self.translateType = translator_type.value

    def translate(self, text: str) -> str:
        html = requests.post(
            url="http://www.whoohoo.co.uk/main.asp",
            data={
                'string': text,
                'x': '26',
                'y': '6',
                'pageid': self.translateType,
                'topic': 'translator'
            }
        ).content.decode()
        soup = bs(html, 'html.parser')
        return soup.find_all('form', recursive=True)[1].find('b').string

    def translate_to_file(self, text: str, file_path: str) -> None:
        translated_text = self.translate(text)
        open(file_path, 'wb').write(translated_text.encode())