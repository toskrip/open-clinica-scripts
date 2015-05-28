class StudyEventDefinition():
    """Study Event Definition

    According to Operation Data Model

    This is the study event definition which defines the form of study event
    It means it is like a class which is realised via the scheduled study subject Event
    """

    def __init__(self, oid="", name="", eventDefinitionCrfs=[], repeating="", eventType=""):
        """Default Constructor
        """
        # ODM -> Study -> MetaDataVersion -> StudyEventDef -> OID
        self._oid = oid
        # ODM -> Study -> MetaDataVersion -> StudyEventDef -> Name
        self._name = name
        # ODM -> Study -> MetaDataVersion -> StudyEventDef -> Repeating
        self._repeating = repeating
        # ODM -> Study -> MetaDataVersion -> StudyEventDef -> Type
        self._type = eventType

        self._description = ""
        self._category = ""

        self._mandatory = False
        self._orderNumber = 0

        # ODM -> Study -> MetaDataVersion -> FormDef
        self._eventDefinitionCrfs = eventDefinitionCrfs

########  ########   #######  ########  ######## ########  ######## #### ########  ######  
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ## 
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##       
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######  
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ## 
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ## 
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ###### 

    @property
    def oid(self):
        """OID Getter
        """
        return self._oid

    @oid.setter
    def oid(self, value):
        """OID Setter
        """
        self._oid = oidValue

    @property
    def name(self):
        """Name Getter
        """
        return self.__name

    @name.setter
    def name(self, value):
        """Name Setter
        """
        self._name = nameValue

    @property
    def description(self):
        """Description Getter
        """
        return self._description

    @description.setter
    def description(self, value):
        """Description Setter
        """
        self._description = value

    @property
    def category(self):
        """Category Getter
        """
        return self._category

    @category.setter
    def category(self, value):
        """Category Setter
        """
        self._category = value

    @property
    def repeating(self):
        """Repeating Getter
        """
        return self._repeating

    @repeating.setter
    def repeating(self, value):
        """Repeating Setter
        """
        self._repeating = repeatingValue

    @property
    def type(self):
        """Type Getter
        """
        return self._type

    @type.setter
    def type(self, value):
        """Type Setter
        """
        self._type = typeValue

    @property
    def mandatory(self):
        """Event is mandatory Getter
        """
        return self._mandatory

    @mandatory.setter
    def mandatory(self, value):
        """Event is mandatory Setter
        """
        self._mandatory = value

    @property
    def orderNumber(self):
        """Event order number in protocol Getter
        """
        return self._orderNumber

    @orderNumber.setter
    def orderNumber(self, value):
        """Event order number in protocol Setter
        """
        self._orderNumber = value

    @property
    def eventDefinitionCrfs(self):
        """EventDefinitionCrfs Getter
        """
        return self._eventDefinitionCrfs

    @eventDefinitionCrfs.setter
    def eventDefintionCrfs(self, crfs):
        """EventDefintiionCrfs Setter
        """
        self._eventDefinitionCrfs = crfs

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def __repr__(self):
        """Object representation
        """
        adr = hex(id(self)).upper()
        return "<StudyEventDefinition oid: %s, name: %s at %s>" % (self.oid, self.name, adr)
