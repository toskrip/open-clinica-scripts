 ######  ########  ######## 
##    ## ##     ## ##       
##       ##     ## ##       
##       ########  ######   
##       ##   ##   ##       
##    ## ##    ##  ##       
 ######  ##     ## ##       

class Crf():
    """Case Report Form
    This is CRF form associated to concrete study event
    """

    def __init__(self):
        """Default constructor
        """
        self._oid = ""
        self._name = ""
        self._version = ""
        self._status = ""
        self._isDefaultVersion = False

        self._itemGroups = []

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
    def version(self):
        """Version Getter
        """
        return self._version

    @version.setter
    def version(self, value):
        """Version Setter
        """
        self._version = value

    @property
    def status(self):
        """Status Getter
        """
        return self._status

    @status.setter
    def status(self, value):
        """Status Setter
        """
        self._status = value

    @property
    def isDefaultVersion(self):
        """Is default CRF version Getter
        """
        return self._isDefaultVersion

    @isDefaultVersion.setter
    def isDefaultVersion(self, value):
        """Is default CRF version Setter
        """
        self._isDefaultVersion = value

    @property
    def itemGroups(self):
        """Item groups Getter
        """
        return self._itemGroups

    @itemGroups.setter
    def itemGroups(self, value):
        """Item groups Setter
        """
        self._itemGroups = value
        
##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def atrSize(self):
        """Number of showable arguments
        """
        return 2
