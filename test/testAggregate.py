import unittest

import testCsvFileDataService
import testDateConverter
import testFloatConverter
import testOdmFileDataService
#import testTransformationService

suite1 = testCsvFileDataService.suite()
suite2 = testOdmFileDataService.suite()
suite3 = testDateConverter.suite()
suite4 = testFloatConverter.suite()
#suite5 = testTransformationService.suit()

suite = unittest.TestSuite()
suite.addTest(suite1)
suite.addTest(suite2)
suite.addTest(suite3)
suite.addTest(suite4)
#suite.addTest(suite5)

unittest.TextTestRunner(verbosity=2).run(suite)
