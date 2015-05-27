import sys, os
import unittest

sys.path.insert(0, os.path.abspath("./../"))

from services.TransformationService import TransformationService

class TestTransformationService(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """


    def test_transformation_service_can_be_initialised(self):
        """
        """
        svc = Transformation()
        self.assertTrue(svc is not None)


def suite():
    """
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTransformationService))

    return suite

if __name__ == '__main__':
    unittest.main()