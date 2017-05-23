import unittest
from dirtyauto.crawler.digikey import DigikeyPartInfo


class TestPartNumber(unittest.TestCase):
    idtpn = DigikeyPartInfo('5PB1102')

    def test_found_parts(self):
        if self.idtpn.found_parts():
            pass
        else:
            self.fail('No part table was found')


if __name__ == 'main':
    unittest.main()
