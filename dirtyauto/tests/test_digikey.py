import unittest
from dirtyauto.crawler.digikey import DigikeyPartInfo, MultiPartDigikey


class TestPartNum(unittest.TestCase):
    idtpn = DigikeyPartInfo("5P49V6901")

    def _page_type(self, _partNum):
        self.idtpn = DigikeyPartInfo(_partNum)
        result = self.idtpn.page_type()
        return result

    def test_page_parts(self):
        self.assertEqual(self._page_type('5PB1102'), 'productTable')
        self.assertEqual(self._page_type('radowm123sds'), None)
        self.assertEqual(self._page_type('8SLVP1204ANLGI8'), 'productPage')

    def test_page_links(self):
        self.assertEqual(self._page_type('5P49V5901'), 'searchPage')

    def test_parse_pricing_table(self):
        self.idtpn = DigikeyPartInfo('5P49v6901')
        self.idtpn.parse_pricing_table()
        unit1_price = self.idtpn.info['1']
        self.assertEqual(unit1_price, '11.35000')

    def test_parse_mpn(self):
        self.idtpn = DigikeyPartInfo('5P49V6901')
        self.idtpn.parse_mpn()
        self.assertEqual('5P49V6901A000NLGI', self.idtpn.info['mpn'])

    def test_parse_qty(self):
        self.idtpn.parse_qty()
        self.assertEqual('2,081', self.idtpn.info['qty'])

    def test_get_product_table_lnk(self):
        self.idtpn = DigikeyPartInfo('5PB1102')
        lnk = self.idtpn.get_productlnk_from_productTable()[0]
        self.assertEqual(
            lnk, "https://www.digikey.com/product-detail/en/idt-integrated-device-technology-inc/5PB1102CMGI8/800-2888-2-ND/5253372")


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
