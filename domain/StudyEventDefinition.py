class StudyEventDefinition():
    """Study Event Definition

    According to Operation Data Model

    This is the study event definition which defines the form of study event
    It means it is like a class which is realised via the scheduled study subject Event
    """
    #--------------------------------------------------------------------------
    #----------------------------- Constructors -------------------------------

    def __init__(self, oid="", name="", eventDefinitionCrfs=[], repeating="", eventType=""):
        """Constructor
        """
        # ODM -> Study -> MetaDataVersion -> StudyEventDef -> OID
        self.__oid = oid
        # ODM -> Study -> MetaDataVersion -> StudyEventDef -> Name
        self.__name = name
        # ODM -> Study -> MetaDataVersion -> StudyEventDef -> Repeating
        self.__repeating = repeating
        # ODM -> Study -> MetaDataVersion -> StudyEventDef -> Type
        self.__type = eventType

        self.__description = ""
        self.__category = ""

        # ODM -> Study -> MetaDataVersion -> FormDef
        self.__eventDefinitionCrfs = eventDefinitionCrfs

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

    @property
    def description(self):
        """Description Getter
        """
        return self.__description

    @description.setter
    def description(self, value):
        """Description Setter
        """
        if self.__description != value:
            self.__description = value

    @property
    def category(self):
        """Category Getter
        """
        return self.__category

    @category.setter
    def category(self, value):
        """Category Setter
        """
        if self.__category != value:
            self.__category = value

    def repeating(self):
        """Repeating Getter
        """
        return self.__repeating


    def setRepeating(self, repeatingValue):
        """Repeating Setter
        """
        if self.__repeating != repeatingValue:
            self.__repeating = repeatingValue


    def type(self):
        """Type Getter
        """
        return self.__type


    def setType(self, typeValue):
        """Type Setter
        """
        if self.__type != typeValue:
            self.__type = typeValue


    def eventDefinitionCrfs(self):
        """EventDefinitionCrfs Getter
        """
        return self.__eventDefinitionCrfs


    #-----------------------------------------------------------------------

    def atrSize(self):
        "Visible attributes in import table view"
        return 2

