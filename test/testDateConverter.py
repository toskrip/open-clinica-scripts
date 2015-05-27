import sys, os
import unittest

sys.path.insert(0,os.path.abspath("./../"))

from converters.DateConverter import DateConverter

class TestDateConverter(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """


    def test_date_converter_can_be_initialised(self):
        """
        """
        dateConverter = DateConverter()
        self.assertTrue(dateConverter is not None)


    def test_isfulldate_is_true_when_fulldate_provided(self):
        """
        """
        dateConverter = DateConverter()
        dateConverter.setHasDayComponet(True)
        dateConverter.setHasMonthComponet(True)
        dateConverter.setHasYearComponet(True)

        isFullDate = dateConverter.isFullDate()

        self.assertTrue(isFullDate)


    def test_isfulldate_is_false_when_partialdate_provided(self):
        """
        """
        dateConverter = DateConverter()
        dateConverter.setHasDayComponet(False)
        dateConverter.setHasMonthComponet(True)
        dateConverter.setHasYearComponet(True)

        isFullDate = dateConverter.isFullDate()

        self.assertTrue(not isFullDate)


    def test_ispartialdate_is_true_when_partialdate_provided(self):
        """
        """
        dateConverter = DateConverter()
        dateConverter.setHasDayComponet(False)
        dateConverter.setHasMonthComponet(True)
        dateConverter.setHasYearComponet(True)

        isPartialDate = dateConverter.isPartialDate()

        self.assertTrue(isPartialDate)


    def test_ispartialdate_is_false_when_fulldate_provided(self):
        """
        """
        dateConverter = DateConverter()
        dateConverter.setHasDayComponet(True)
        dateConverter.setHasMonthComponet(True)
        dateConverter.setHasYearComponet(True)

        isPartialDate = dateConverter.isPartialDate()

        self.assertTrue(not isPartialDate)


    def test_convert_works_with_fulldate_normal_ordering(self):
        """
        """
        dateConverter = DateConverter()
        dateConverter.setHasDayComponet(True)
        dateConverter.setHasMonthComponet(True)
        dateConverter.setHasYearComponet(True)

        dateConverter.setIsIsoOrdered(False)

        dateConverter.setDateSeparator(".")

        rawDates = ["1.3.2004", "12. 4. 1987", " 26. 4. 2006 ", "04.6.1969", "6.07.2010"]
        expectedDates = ["2004-03-01", "1987-04-12", "2006-04-26", "1969-06-04", "2010-07-06"]

        works = True
        i = 0
        for date in rawDates:
            result = dateConverter.convert(date)
            if expectedDates[i] != result:
                works = False
                break
            i = i + 1

        self.assertTrue(works)


def suite():
    """
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDateConverter))

    return suite


if __name__ == '__main__':
    unittest.main()