class StudySite():
    """Study Site domain object
    """
    #--------------------------------------------------------------------------
    #----------------------------- Constructors -------------------------------

    def __init__(self, identifier="", oid="", name=""):
        """Constructor

        """
        self.__identifier = identifier
        self.__oid = oid
        self.__name = name

    #--------------------------------------------------------------------------
    #----------------------------- Properties ---------------------------------

    @property
    def identifier(self):
        """Identifier Getter
        """
        return self.__identifier


    @identifier.setter
    def identifier(self, identifierValue):
        """Identifier Setter
        """
        if self.__identifier != identifierValue:
            self.__identifier = identifierValue


    @property
    def oid(self):
        """OID Getter
        """
        return self.__oid


    @oid.setter
    def oid(self, oidValue):
        """OID Setter
        """
        if self.__oid != oidValue:
            self.__oid = oidValue


    @property
    def name(self):
        """Name Getter
        """
        return self.__name


    @name.setter
    def name(self, nameValue):
        """Name Setter
        """
        if self.__name != nameValue:
            self.__name = nameValue


    #----------------------------------------------------