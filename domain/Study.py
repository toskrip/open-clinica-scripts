class Study():
    """Study domain object

    According to Operational Data Model
    """
    #--------------------------------------------------------------------------
    #----------------------------- Constructors -------------------------------

    def __init__(self, identifier="", oid="", name="", description=""):
        """Constructor

        """
        self.__identifier = identifier

        # ODM->Study->OID
        self.__oid = oid

        self.__name = name

        # ODM->Study->GlobalVariables->StudyDescription
        self.__description = description

        # Study sites
        self.__sites = []

    #--------------------------------------------------------------------------
    #----------------------------- Properties ---------------------------------

    def identifier(self):
        """Identifier Getter
        """
        return self.__identifier


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


    def description(self):
        """Description Getter
        """
        return self.__description


    def setDescription(self, descriptionValue):
        """Description Setter
        """
        if self.__description != descriptionValue:
            self.__description = descriptionValue


    @property
    def sites(self):
        """Sites Getter
        """
        return self.__sites

    @sites.setter
    def sites(self, sites):
        """Sites Setter
        """
        self.__sites = sites

    @property
    def isMulticentre(self):
        """Determine whether the study is multicentre
        """
        return len(self.sites) > 0


    #----------------------------------------------------

    def atrSize(self):
        """Visible attributes in import tableView
        """
        return 3

    def __repr__(self):
        """Object representation
        """
        adr = hex(id(self)).upper()
        return "<Study %s at %s>" % (self.__identifier, adr)