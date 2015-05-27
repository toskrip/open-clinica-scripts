import sys, os, tempfile
import unittest

sys.path.insert(0,os.path.abspath("./../"))

from services.AnonymisationService import AnonymisationService

class TestAnonymisationService(unittest.TestCase):
    """
    """
    def setUp(self):
        """Set up data used in the tests.
        setUp is called before each test function execution.
        """
        self.folder = "../../data/AarhusPhotonJoergenProstate"
        self.tmpFolder = "../../data/AarhusPhotonJoergenProstate-anonym"#tempfile.mkdtemp()
        self.mappingRoiDic = {}

    def test_anonymisation_service_can_be_initialised(self):
        """
        """
        svc = AnonymisationService(self.folder, self.tmpFolder, self.mappingRoiDic)

        self.assertTrue(svc is not None)

    def test_anonymisation_service_can_anonymise(self):
        """
        """
        svc = AnonymisationService(self.folder, self.tmpFolder, self.mappingRoiDic)

        # Provide optional setting for anonymisation (use PID)
        svc.GeneratePatientID = False
        svc.PatientID = "XXX"

        patientID, anonymisedSeriesID = svc.makeAnonymous()


def suite():
    """
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAnonymisationService))

    return suite

if __name__ == '__main__':
    unittest.main()