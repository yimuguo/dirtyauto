import unittest
from dirtyauto.crawler.digikey import DigikeyPartInfo


class TestPartNumber(unittest.TestCase):
    idtpn = DigikeyPartInfo()
    idtpn.part_list = '5PB1102'
    # idtpn = DigikeyPartInfo('5P49V5901')

    def test_part_list(self):
        print(self.idtpn._part_list)
        self.assertEqual(self.idtpn._part_list, ['5PB1102'])

    def test_found_parts(self):
        test_avalst = self.idtpn.found_parts()
        self.assertEqual(test_avalst, [1])

    def test_part_price(self):
        pass


if __name__ == '__main__':
    unittest.main()
