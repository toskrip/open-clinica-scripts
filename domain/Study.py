#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

class Study():
    """Study domain object

    According to CDISC Operational Data Model
    """

    def __init__(self, identifier="", oid="", name="", description=""):
        """Default Constructor
        """
        self._identifier = identifier

        # ODM->Study->OID
        self._oid = oid

        self._name = name

        # ODM->Study->GlobalVariables->StudyDescription
        self._description = description

        # Study sites
        self._sites = []

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

    @property
    def oid(self):
        """OID Getter
        """
        return self._oid

    @oid.setter
    def oid(self, oidValue):
        """OID Setter
        """
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
        self._name = nameValue

    @property
    def description(self):
        """Description Getter
        """
        return self._description

    @description.setter
    def description(self, descriptionValue):
        """Description Setter
        """
        self._description = descriptionValue

    @property
    def sites(self):
        """Sites Getter
        """
        return self._sites

    @sites.setter
    def sites(self, sites):
        """Sites Setter
        """
        self._sites = sites

    @property
    def isMulticentre(self):
        """Determine whether the study is multicentre
        """
        return len(self.sites) > 0

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
        return "<Study identifier: %s, oid:%s at %s>" % (self.identifier, self.oid, adr)