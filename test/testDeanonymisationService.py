import sys, os, tempfile
import unittest

sys.path.insert(0,os.path.abspath("./../"))

from services.DeanonymisationService import DeanonymisationService

class TestDeanonymisationService(unittest.TestCase):
    """
    """
    def setUp(self):
        """ Set up data used in the tests.
        setUp is called before each test function execution.
        """
        self.folder = "../../data/AarhusPhotonJoergenProstate-anonym"
        self.tmpFolder = "../../data/temp-test"#tempfile.mkdtemp()

    def test_deanonymisation_service_can_be_initialised(self):
        """
        """
        svc = DeanonymisationService(self.folder)

        self.assertTrue(svc is not None)

    def test_deanonymisation_service_can_deanonymise(self):
        """
        """
        svc = DeanonymisationService(self.folder)
        svc.makeDeanonymous()


def suite():
    """
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDeanonymisationService))

    return suite

if __name__ == '__main__':
    unittest.main()