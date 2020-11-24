class StudySite():
    """Study Site domain object
    """

 ######   #######  ##    ##  ######  ######## ########  ##     ##  ######  ######## 
##    ## ##     ## ###   ## ##    ##    ##    ##     ## ##     ## ##    ##    ##    
##       ##     ## ####  ## ##          ##    ##     ## ##     ## ##          ##    
##       ##     ## ## ## ##  ######     ##    ########  ##     ## ##          ##    
##       ##     ## ##  ####       ##    ##    ##   ##   ##     ## ##          ##    
##    ## ##     ## ##   ### ##    ##    ##    ##    ##  ##     ## ##    ##    ##    
 ######   #######  ##    ##  ######     ##    ##     ##  #######   ######     ##  

    def __init__(self, identifier="", oid="", name=""):
        """Default Constructor
        """
        self._identifier = identifier
        self._oid = oid
        self._name = name

########  ########   #######  ########  ######## ########  ######## #### ########  ######
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ##
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ##
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ##
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ######

    @property
    def identifier(self):
        """Identifier Getter
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifierValue):
        """Identifier Setter
        """
        if self._identifier != identifierValue:
            self._identifier = identifierValue

    @property
    def oid(self):
        """OID Getter
        """
        return self._oid

    @oid.setter
    def oid(self, oidValue):
        """OID Setter
        """
        if self._oid != oidValue:
            self._oid = oidValue

    @property
    def name(self):
        """Name Getter
        """
        return self._name

    @name.setter
    def name(self, nameValue):
        """Name Setter
        """
        if self._name != nameValue:
            self._name = nameValue
