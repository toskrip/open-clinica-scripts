#----------------------------------------------------------------------
#------------------------------ Modules -------------------------------
# Date
import datetime

from converters.Converter import Converter


#----------------------------------------------------------------------
class FloatConverter(Converter):
    """FloatConverter class convert string float with specified decimal
    delimiter to string float with dot decimal delimiter
    """

    #----------------------------------------------------------------------
    #--------------------------- Constructors -----------------------------

    def __init__(self):
        """Constructor
        """
        self.__floatingNumberDelimiter = ""

    #----------------------------------------------------------------------
    #--------------------------- Properites -------------------------------

    def floatingNumberDelimiter(self):
        """FloatingNumberDelimiter Getter
        """
        return self.__floatingNumberDelimiter


    def setFloatingNumberDelimiter(self, floatingNumberDelimiterValue):
        """FloatingNumberDelimiter Setter
        """
        if self.__floatingNumberDelimiter != floatingNumberDelimiterValue:
            self.__floatingNumberDelimiter = floatingNumberDelimiterValue


    def containCommaThousandDelimiter(self, data):
        """Determine if withing the strig float there is comma thousand delimiter
        """
        hasDot = data.find(".") != -1
        hasComma = data.find(",") != -1

        return hasDot and hasComma


    #----------------------------------------------------------------------
    #--------------------------- Methods ----------------------------------

    def convert(self, rawDate):
        """Convert to string float with dot floating number delimiter
        """
        # First clear the white spaces from the raw float string
        clearFloat = rawDate.replace(" ","")

        # Remove comma thousand deliminter if there is shuch in float string
        if self.containCommaThousandDelimiter(clearFloat):
            clearFloat = clearFloat.replace(",", "")

        # Make sure that
        returnFloatString = clearFloat.replace(self.__floatingNumberDelimiter, ".")

        return returnFloatString


    def __str__(self):
        """ToString

        Print the class itself
        """
        #TODO: print converter settings
        return "Float Converter: "