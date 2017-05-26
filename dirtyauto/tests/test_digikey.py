import unittest
from dirtyauto.crawler.digikey import DigikeyPartInfo


class TestPartNumber(unittest.TestCase):
    # idtpn = DigikeyPartInfo('5PB1102')
    idtpn = DigikeyPartInfo('5P49V5901')

    def test_found_parts(self):
        if self.idtpn.found_parts():
            print(self.idtpn.found_parts())
            pass
        else:
            self.fail('No part table was found')

    def test_part_price(self):
        pass


if __name__ == '__main__':
    unittest.main()
