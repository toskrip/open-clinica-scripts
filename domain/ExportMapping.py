class ExportMapping:
    """Export mapping domain object
    """

    #----------------------------------------------------------------------
    #--------------------------- Constructors -----------------------------

    def __init__(self, metadata, data=""):
        """Constructor
        """
        # Initialize metadata field
        self.metadata = metadata

        # Metadata field properties
        self.metadataOid = ""
        self.dataType = ""
        self.length = -1
        self.mandatory = False

        # If metadata specify code list for this metadata field it is stored here
        self.codeList = None
        # User shoud specify if tha provided data field are already encoded
        self.__useCodeListToEncodeData = False

        # Initialize data field as empty because mapping was not defined yet
        self.data = data

        # Conveter
        self.__converter = None

    #----------------------------------------------------------------------
    #--------------------------- Properties -------------------------------

    def converter(self):
        """Converter Getter
        """
        return self.__converter


    def setConverter(self, converterValue):
        """Converter Setter
        """
        if self.__converter is not converterValue:
            self.__converter = converterValue


    def useCodeListToEncodeData(self):
        """UseCodeListToEncodeData Getter
        """
        return self.__useCodeListToEncodeData


    def setUseCodeListToEncodeData(self, useCodeListToEncodeDataValue):
        """UseCodeListToEncodeData Setter
        """
        if self.__useCodeListToEncodeData != useCodeListToEncodeDataValue:
            self.__useCodeListToEncodeData = useCodeListToEncodeDataValue


    def isComplete(self):
        """According to dataType check if mapper has all information needed

        E.g. also if complete converter is defined etc.
        """
        #TODO: implement later
        return True

    #----------------------------------------------------------------------
    #--------------------------- Methods ----------------------------------

    def map(self, data):
        """Map data to metadata and produce string data which conform metadata
        """
        result = data

        if self.__converter is not None:
            result = self.convert(data)
        elif self.codeList is not None:
            if self.validate(data):
                result = self.encode(data)

        return result


    def convert(self, data):
        """If converter was defined convert the data
        """
        # When no converter return the original data
        convertedData = data

        if self.__converter is not None:
            convertedData = self.__converter.convert(data)

        return convertedData


    def validate(self, data):
        """validate if data could be encoded with defined code list (if defined)
        """
        # When no code items return true because there is nothing to validate
        isValid = True

        #self.codeList.dataType - take also this into account later
        if self.codeList is not None:
            for item in self.codeList.listItems:
                if item.decodedValue == data:
                    isValid = True
                    break
                else:
                    isValid = False

        return isValid


    def encode(self, data):
        """Encode data according to defined codeList
        """
        # When no code items return the original data
        encodedData = data

        if self.__useCodeListToEncodeData:
            for item in self.codeList.listItems:
                if item.decodedValue == data:
                    encodedData = item.codedValue
                    break

        return encodedData
