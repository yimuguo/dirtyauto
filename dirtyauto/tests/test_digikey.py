import unittest
from dirtyauto.crawler.digikey import DigikeyPartInfo, MultiPartDigikey


class TestPartNum(unittest.TestCase):
    idtpn = DigikeyPartInfo("5PB1102")

    def _page_type(self, _partNum):
        self.idtpn.partn = _partNum
        self.idtpn.soup = self.idtpn.get_soup(_partNum)
        result = self.idtpn.page_type()
        return result

    def test_page_parts(self):
        self.assertEqual(self._page_type('5PB1102'), 'productTable')
        self.assertEqual(self._page_type('radowm123sds'), None)
        self.assertEqual(self._page_type('8SLVP1204ANLGI8'), 'productPage')

    def test_page_links(self):
        self.assertEqual(self._page_type('5P49V5901'), 'searchPage')

    def test_part_price(self):
        pass


class TestMultiPartNum(unittest.TestCase):
    """
    Test for MultiPartDigikey Class
    """
    idtpns = MultiPartDigikey()
    idtpns.part_list = '5PB1102'
    # idtpn = DigikeyPartInfo('5P49V5901')

    def test_part_list(self):
        print(self.idtpns._part_list)
        self.assertEqual(self.idtpns._part_list, ['5PB1102'])

    def test_found_parts(self):
        test_avalst = self.idtpns.found_parts()
        self.assertEqual(test_avalst, [1])


if __name__ == '__main__':
    unittest.main()
