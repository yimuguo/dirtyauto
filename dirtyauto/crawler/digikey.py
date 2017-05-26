from bs4 import BeautifulSoup
import requests


class DigikeyPartInfo(object):

    """For parsing part info on digikey"""

    def __init__(self, part_list):
        """
        :param partn: The stadard part number
        """
        self._partList = part_list
        self.soup = BeautifulSoup("", 'html.parser')

    def get_table(self, _partn):
        page = requests.get(
            "https://www.digikey.com/products/en?keywords=" + _partn)
        self.soup = BeautifulSoup(page.content, 'html.parser').encode('utf-8')
        if self.soup.find("table", id="productTable"):
            # TODO: implement product table parser
            pass

    # def __init__(self, partn):
    #     self._partn = partn
    #     super(self.__class__, self).__init__(self._partn)

    # def get_html(self):
    #     self.soup = BeautifulSoup(page.text, 'html.parser').encode('utf-8')

    def found_parts(self):
        return self.soup.find("table", id="productTable")

    def parse_table(self):
        pass
