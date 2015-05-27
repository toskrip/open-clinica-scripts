import sys, os
import unittest

sys.path.insert(0,os.path.abspath("./../"))

from converters.FloatConverter import FloatConverter

class TestFloatConverter(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """


    def test_float_converter_can_be_initialised(self):
        """
        """
        floatConverter = FloatConverter()
        self.assertTrue(floatConverter is not None)


    def test_contain_comma_thousand_delimiter_is_true_when_number_with_thousand_delimiter_provided(self):
        """
        """
        floatConverter = FloatConverter()
        data = "1, 234.23"

        self.assertTrue(floatConverter.containCommaThousandDelimiter(data))


    def test_contain_comma_thousand_delimiter_is_false_when_number_without_thousand_delimiter_provided(self):
        """
        """
        floatConverter = FloatConverter()
        data = "1 234,23"

        self.assertTrue(not floatConverter.containCommaThousandDelimiter(data))


    def test_convert_works_with_comma_floating_nr_delimiter(self):
        """
        """
        floatConverter = FloatConverter()
        floatConverter.setFloatingNumberDelimiter(",")

        rawFloats = ["156,234", "1698, 68", " 4526 , 459 ", "1 234,04566"]
        expectedFloats = ["156.234", "1698.68", "4526.459", "1234.04566"]

        works = True
        i = 0
        for floatnr in rawFloats:
            result = floatConverter.convert(floatnr)
            if expectedFloats[i] != result:
                works = False
                break
            i = i + 1

        self.assertTrue(works)


def suite():
    """
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFloatConverter))

    return suite


if __name__ == '__main__':
    unittest.main()