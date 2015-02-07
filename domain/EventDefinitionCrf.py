class EventDefinitionCrf():
    """Study Form Definition

    According to Operation Data Model
    This holds the eCRF forms for StudyEventDefinition
    """
    #--------------------------------------------------------------------------
    #----------------------------- Constructors -------------------------------

    def __init__(self, required="", doubleDataEntry="", passwordRequired="", hideCrf="", sourceDataVerificaiton="", crf=None, defaultCrfVersion=None):
        """Constructor
        """
        # ODM -> Study -> MetaDataVersion -> FormDef -> OID
        self.__oid = ""
        # ODM -> Study -> MetaDataVersion -> FormDef -> Name
        self.__name = ""
        # ODM -> Study -> MetaDataVersion -> FormDef -> Repeating
        self.__repeating = ""

        # OpenClinica form details
        self.__required = required
        self.__doubleDataEntry = doubleDataEntry
        self.__passwordRequired = passwordRequired
        self.__hideCrf = hideCrf
        self.__sourceDataVerificaiton = sourceDataVerificaiton
        self.__crf = crf
        self.__defaultCrfVersion = defaultCrfVersion

    #--------------------------------------------------------------------------
    #----------------------------- Properties ---------------------------------
    def oid(self):
        """OID Getter
        """
        return self.__oid


    def setOid(self, oidValue):
        """OID Setter
        """
        if self.__oid != oidValue:
            self.__oid = oidValue


    def name(self):
        """Name Getter
        """
        return self.__name


    def setName(self, nameValue):
        """Name Setter
        """
        if self.__name != nameValue:
            self.__name = nameValue


    def repeating(self):
        """Repeating Getter
        """
        return self.__repeating


    def setRepeating(self, repeatingValue):
        """Repeating Setter
        """
        if self.__repeating != repeatingValue:
            self.__repeating = repeatingValue


    def required(self):
        """Required Getter
        """
        return self.__required


    def doubleDataEntry(self):
        return self.__doubleDataEntry


    def passwordRequired(self):
        return self.__passwordRequired


    def hideCrf(self):
        return self.__hideCrf


    def sourceDataVerificaiton(self):
        return self.__sourceDataVerificaiton


    def crf(self):
        return self.__crf


    def defaultCrfVersion(self):
        return self.__defaultCrfVersion


    #-----------------------------------------------------------------------

    def atrSize(self):
        "Visible attributes in import table view"
        return 3

