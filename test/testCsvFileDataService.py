import sys, os
import unittest

sys.path.insert(0,os.path.abspath("./../"))

from services.CsvFileDataService import CsvFileDataService

class TestCsvFileDataService(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """

    def test_csv_file_service_can_be_initialised(self):
        """
        """
        svc = CsvFileDataService()
        self.assertTrue(svc is not None)

def suite():
    """
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCsvFileDataService))

    return suite


if __name__ == '__main__':
    unittest.main()