from bs4 import BeautifulSoup
import requests


class PartNumber(object):
    soup = BeautifulSoup("", 'html.parser')

    def __init__(self, partn):
        self.partn = partn

    def get_html(self):
        page = requests.get(
            "https://www.digikey.com/products/en?keywords=" + self.partn)
        self.soup = BeautifulSoup(page.text, 'html.parser').encode('utf-8')
