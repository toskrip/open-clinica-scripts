#----------------------------------------------------------------------
#------------------------------ Modules -------------------------------
# Date
import datetime

from converters.Converter import Converter


#----------------------------------------------------------------------
class DateConverter(Converter):
    """DateConverter class convert string date to ISO date according to specified settings
    """

    #----------------------------------------------------------------------
    #--------------------------- Constructors -----------------------------

    def __init__(self):
        """Constructor
        """
        # Members
        self.__hasDayComponent = False
        self.__hasMonthComponent = False
        self.__hasYearComponent = False

        # ISO orderred means reverse order like YYY-MM-DD
        self.__isISOOrdered = False
        self.__dateSeparator = ""

    #----------------------------------------------------------------------
    #--------------------------- Properites -------------------------------

    def hasDayComponent(self):
        """HasDayComponet Getter
        """
        return self.__hasDayComponent


    def setHasDayComponet(self, hasDayValue):
        """HasDayComponent Setter
        """
        if self.__hasDayComponent != hasDayValue:
            self.__hasDayComponent = hasDayValue


    def hasMonthComponent(self):
        """HasMonthComponet Getter
        """
        return self.__hasMonthComponent


    def setHasMonthComponet(self, hasMonthValue):
        """HasMonthComponent Setter
        """
        if self.__hasMonthComponent != hasMonthValue:
            self.__hasMonthComponent = hasMonthValue


    def hasYearComponent(self):
        """HasYearComponet Getter
        """
        return self.__hasYearComponent


    def setHasYearComponet(self, hasYearValue):
        """HasYearComponent Setter
        """
        if self.__hasYearComponent != hasYearValue:
            self.__hasYearComponent = hasYearValue


    def isIsoOrdered(self):
        """IsIsoOrdered Getter
        """
        return self.__isISOOrdered


    def setIsIsoOrdered(self, isIsoOrderedValue):
        """IsIsoOrdered Setter
        """
        if self.__isISOOrdered != isIsoOrderedValue:
            self.__isISOOrdered = isIsoOrderedValue


    def dateSeparator(self):
        """DateSeparator Getter
        """
        return self.__dateSeparator


    def setDateSeparator(self, dateSeparatorValue):
        """DateSeparator Setter
        """
        if self.__dateSeparator != dateSeparatorValue:
            self.__dateSeparator = dateSeparatorValue


    def isFullDate(self):
        return self.__hasDayComponent and self.__hasMonthComponent and self.__hasYearComponent


    def isPartialDate(self):
        return not self.__hasDayComponent and self.__hasMonthComponent and self.__hasYearComponent


    #----------------------------------------------------------------------
    #--------------------------- Methods ----------------------------------

    def convert(self, rawDate):
        """Convert to ISO date
        """
        # First clear the white spaces from the raw date string
        clearDate = rawDate.replace(" ","")

        # Now create a python dateTime from string
        format = ""
        if self.isFullDate():
            if self.__isISOOrdered:
                format = "%Y" + self.__dateSeparator + "%m" + self.__dateSeparator + "%d"
            else:
                format = "%d" + self.__dateSeparator + "%m" + self.__dateSeparator + "%Y"
        elif self.isPartialDate():
            if self.__isISOOrdered:
                format = "%Y" + self.__dateSeparator + "%m"
            else:
                format = "%m" + self.__dateSeparator + "%Y"

        if format != "":
            dpython = datetime.datetime.strptime(clearDate, format)

        # Finally convert to ISO date string
        return datetime.datetime.strftime(dpython, "%Y-%m-%d")


    def __str__(self):
        """ToString

        Print the class itself
        """
        #TODO: print converter settings
        return "Date Converter: "