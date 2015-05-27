from StringIO import StringIO
import csv
import logging
import logging.config
import sys
import textwrap


class CsvFileDataService():
    """File data service dedicated to work with CSV files
    """
    def __init__(self, logger=None):
        """Constructor
        """
        # Logger
        self.logger = logger or logging.getLogger(__name__)
        #logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

        # Init members
        self.filename = ''
        self.delimiter = '\t'

        # Header columns are holding the names of data elements
        self.headers = []


    def isFileLoaded(self):
        """Determine whether the filename is provided to the service
        """
        return self.filename != ""


    def setFilename(self, filename):
        """Setup data filename for the service
        """
        if self.filename != filename:
            self.filename = filename


    def getFilename(self):
        """Get the name of the data file
        """
        return str(self.filename)


    def loadHeaders(self):
        """Load data columns from csv file

        First row of csv file is holding the headers
        """
        if (self.isFileLoaded) :
            f = open(self.filename, 'rt')
            try:
                rownum = 0
                reader = csv.reader(f, delimiter=self.delimiter)
                for row in reader:
                    if rownum == 0:
                        self.headers = row
                        break

            finally:
                f.close()


    def size(self):
        """Number of records in csv without header line
        """
        totalrows = 0
        if (self.isFileLoaded) :
            f = open(self.filename, 'rt')
            try:
                reader = csv.reader(f, delimiter=self.delimiter)
                rows = list(reader)
                totalrows = len(rows)
            finally:
                f.close()

        return totalrows


    def getRow(self, rowNr):
        """
        """
        resultRow = None
        if (self.isFileLoaded) :
            f = open(self.filename, 'rt')
            try:
                rownum = 0
                reader = csv.reader(f, delimiter=self.delimiter)
                for row in reader:
                    if rownum == rowNr:
                        resultRow = row
                        break
                    rownum = rownum + 1
            finally:
                f.close()

        return resultRow


    def printData(self):
        """Print the content of file to the console
        """
        if (self.isFileLoaded) :
            f = open(self.filename, 'rt')
            try:
                reader = csv.reader(f)
                for row in reader:
                    print row
            finally:
                f.close()
