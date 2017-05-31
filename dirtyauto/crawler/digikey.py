from bs4 import BeautifulSoup
import requests
from dirtyauto import log


class DigikeyPartInfo(object):

    """For parsing part info on digikey"""

    def __init__(self):
        """
        :param part_list: list of the part numbers
        """
        self.log = log(self.__class__.__name__)
        self._part_list = None
        # self.part_list = part_list
        self.soup = BeautifulSoup("", 'html.parser')

    @property
    def part_list(self):
        return self._part_list

    @part_list.setter
    def part_list(self, part_input):
        if not isinstance(part_input, list):
            if isinstance(part_input, str):
                self.log.warning("Input is not a list, converting string to list")
                self._part_list = [part_input]
                return
            elif isinstance(part_input, int):
                self.log.warning("Input is not a list, converting int to list")
                self._part_list = [str(part_input)]
            else:
                self.log.error("Input is not a list, cannot process " +
                               str(type(part_input)))
        else:
            self._part_list = part_input

    @staticmethod
    def get_soup(partn):
        """
        :param partn part number input
        """
        page = requests.get(
            "https://www.digikey.com/products/en?keywords=" + partn)
        return BeautifulSoup(page.content, 'html.parser')

    def get_table(self, partn):
        self.soup = self.get_soup(partn)
        if self.soup.find("table", id="productTable"):
            # TODO: implement product table parser
            pass

    # def get_html(self):
    #     self.soup = BeautifulSoup(page.text, 'html.parser').encode('utf-8')

    def found_parts(self):
        part_lst = []
        for x in self._part_list:
            print(x)
            _soup = self.get_soup(x)
            if _soup.find("table", id="productTable"):
                part_lst.append(1)
            else:
                part_lst.append(0)
        return part_lst

    def page_type(self, _soup):
        """
        :param _soup: Beautifulsoup object
        :type arg1: class object
        :return: return string with type
        """
        if _soup.find('table', id="productTable"):
            return "productTable"
        elif _soup.find('table', id='product-dollars'):
            return ""

    def parse_table(self):
        pass
