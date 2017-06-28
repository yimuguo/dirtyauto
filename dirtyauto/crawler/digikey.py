from bs4 import BeautifulSoup
import requests
from dirtyauto import log


class DigikeyPartInfo(object):

    """For parsing part info on digikey
    qty: [1, 10, 25, 50, 100, 250, 500, 1000, 1250, 3000] units
    """
    info = {'mpn': "", 'pkging': "", 'avail': "", 'qty': 0}

    def __init__(self, partn):
        """
        :param part_list: list of the part numbers
        """
        self.log = log(self.__class__.__name__)
        self.partn = partn
        self.soup = self.get_soup(self.partn)

    @staticmethod
    def get_soup(partn):
        """
        :param partn part number input
        """
        page = requests.get(
            "https://www.digikey.com/products/en?keywords=" + partn)
        return BeautifulSoup(page.content, 'html.parser')

    def get_productlnk_from_productTable(self):
        """
        :return: return list with product links from product search table
        """
        links = []
        row_soup = self.soup.find_all('td', {"class": "tr-mfgPartNumber"})
        for item in row_soup:
            int_lnk = item.find('a').get('href')
            links.append("https://www.digikey.com" + int_lnk)
            self.log.info(str(self.partn) + "| Scrap " + int_lnk)
        # print(links)
        return links

    def parse_prod_attr(self):
        table = self.soup.find('table', id='prod-att-table')
        # print(table)
        rows = table.find_all('tr')
        for tr in rows:
            print(tr)

    def parse_pricing_table(self):
        table = self.soup.find('table', id='product-dollars')
        rows = table.find_all('tr')
        for row in range(1, len(rows)):
            # print(rows[row])
            cols = rows[row].find_all('td')
            price_break = str(cols[0].text)
            price_break = price_break.strip()
            # print(price_break)
            unit_price = str(cols[1].text)
            unit_price = unit_price.strip()
            # print(unit_price)
            self.info[price_break] = unit_price
        # print(self.info)

    def parse_mpn(self):
        """
        parse manufacturer part number to dict:info
        """
        mpn = self.soup.find('h1', {"itemprop": "model"}).text
        mpn = ''.join(mpn.split())
        self.info['mpn'] = mpn

    def parse_qty(self):
        """
        parse available quantity to dict:info
        """
        qty = self.soup.find('span', id='dkQty').text
        self.info['qty'] = qty

    def parse_manufacturer(self):
        """
        parse current manufacturer to dict:info
        """
        manu = self.soup.find('span', {"itemprop": "name"}).text
        self.info['manufacturer'] = manu

    def _find_product_link(self, searchtxt):
        if self.soup.find('a', href=True, text=searchtxt):
            tree_lnk = self.soup.find(
                'a', href=True, text=searchtxt)
            product_table_lnk = "https://www.digikey.com" + \
                tree_lnk.get('href')
            self.log.info(str(self.partn) +
                          '| Redirect soup to product search page link under ' + searchtxt)
            _page = requests.get(product_table_lnk)
            self.soup = BeautifulSoup(_page.content, 'html.parser')
            return True
        else:
            return False

    def page_type(self):
        """
        :return: return string with type
        """
        if self.soup.find('table', id="productTable"):
            return "productTable"
        elif self.soup.find('table', id='product-dollars'):
            return "productPage"
        elif 'No Results Found | DigiKey Electronics' in self.soup.title.string:
            self.log.error(
                "There's no part found with this part number on DIGIKEY:" + self.partn)
            return None
        elif self._find_product_link('Clock/Timing - Clock Generators, PLLs, Frequency Synthesizers'):
            return "searchPage"
        elif self._find_product_link('Clock/Timing - Clock Buffers, Drivers'):
            return "searchPage"
        elif self._find_product_link('Programmable Oscillators'):
            return "searchPage"
        else:
            self.log.error("Found Nothing here with P/N: " + self.partn)


class MultiPartDigikey(DigikeyPartInfo):
    """
    Processing multiple parts
    """

    def __init__(self):
        self.log = log(self.__class__.__name__)
        self._part_list = None

    @property
    def part_list(self):
        return self._part_list

    @part_list.setter
    def part_list(self, part_input):
        if not isinstance(part_input, list):
            if isinstance(part_input, str):
                self.log.warning(
                    "Input is not a list, converting string to list")
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

    def found_parts(self):
        part_lst = []
        for x in self._part_list:
            _soup = self.get_soup(x)
            if _soup.find("table", id="productTable"):
                part_lst.append(1)
            else:
                part_lst.append(0)
        return part_lst
