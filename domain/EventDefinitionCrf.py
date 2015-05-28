class EventDefinitionCrf():
    """Study Form Definition

    According to Operation Data Model
    This holds the eCRF forms for StudyEventDefinition
    """

    def __init__(self, required="", doubleDataEntry="", passwordRequired="", hideCrf="", sourceDataVerification="", crf=None, defaultCrfVersion=None):
        """Default Constructor
        """
        # ODM -> Study -> MetaDataVersion -> FormDef -> OID
        self._oid = ""
        # ODM -> Study -> MetaDataVersion -> FormDef -> Name
        self._name = ""
        # ODM -> Study -> MetaDataVersion -> FormDef -> Repeating
        self._repeating = ""

        # OpenClinica form details
        self._required = required
        self._doubleDataEntry = doubleDataEntry
        self._passwordRequired = passwordRequired
        self._hideCrf = hideCrf
        self._sourceDataVerification = sourceDataVerification
        self._crf = crf
        self._defaultCrfVersion = defaultCrfVersion

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
        self._oid = value

    @property
    def name(self):
        """Name Getter
        """
        return self._name

    @name.setter
    def name(self, value):
        """Name Setter
        """
        self._name = value

    @property
    def repeating(self):
        """Repeating Getter
        """
        return self._repeating

    @repeating.setter
    def repeating(self, value):
        """Repeating Setter
        """
        self._repeating = value

    @property
    def required(self):
        """Required Getter
        """
        return self._required

    @property
    def doubleDataEntry(self):
        """DoubleDataEntry Getter
        """
        return self._doubleDataEntry

    @property
    def passwordRequired(self):
        """PasswordRequired Getter
        """
        return self._passwordRequired

    @property
    def hideCrf(self):
        """HideCrf Getter
        """
        return self._hideCrf

    @property
    def sourceDataVerification(self):
        """SourceDataVerification Getter
        """
        return self._sourceDataVerification

    @property
    def crf(self):
        """Crf Getter
        """
        return self._crf

    @property
    def defaultCrfVersion(self):
        """DefaultCrfVersion Getter
        """
        return self._defaultCrfVersion

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
        return "<Event Def CRF oid: %s, name: %s at %s>" % (self.oid, self.name, adr)
