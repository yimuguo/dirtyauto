from bs4 import BeautifulSoup
import requests


class DigikeyPartInfo(BeautifulSoup):

    """docstring for DigikeyPartInfo"""

    def __init__(self, partn):
        """
        :param partn: The stadard part number
        """
        self._partn = partn
        page = requests.get(
            "https://www.digikey.com/products/en?keywords=" + self._partn)
        self.soup = BeautifulSoup(page.text, 'html.parser').encode('utf-8')

    # def __init__(self, partn):
    #     self._partn = partn
    #     super(self.__class__, self).__init__(self._partn)

    # def get_html(self):
    #     self.soup = BeautifulSoup(page.text, 'html.parser').encode('utf-8')

    def found_parts(self):
        return self.soup.find(id='productTable')
