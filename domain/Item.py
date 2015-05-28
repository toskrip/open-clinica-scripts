#### ######## ######## ##     ## 
 ##     ##    ##       ###   ### 
 ##     ##    ##       #### #### 
 ##     ##    ######   ## ### ## 
 ##     ##    ##       ##     ## 
 ##     ##    ##       ##     ## 
####    ##    ######## ##     ## 

class Item():
    """Study CRF item definition domain object

    According to Operational Data Model
    """

    def __init__(self):
        """Default Constructor
        """
        self._oid = ""
        self._name = ""
        self._description = ""
        self._dataType = ""
        self._label = ""
        self._value = ""
        self._itemGroupOid = ""

########  ########   #######  ########  ######## ########  ######## #### ########  ######  
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ## 
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##       
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######  
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ## 
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ## 
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ###### 

    @property
    def oid(self):
        """ItemDef OID Getter
        """
        return self._oid

    @oid.setter
    def oid(self, value):
        """ItemDef OID Setter
        """
        self._oid = value

    @property
    def name(self):
        """
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        """
        self._name = value

    @property
    def description(self):
        """
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        """
        self._description = value

    @property
    def label(self):
        """
        """
        return self._label

    @label.setter
    def label(self, value):
        """
        """
        self._label = value

    @property
    def dataType(self):
        """
        """
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        """
        """
        self._dataType = value

    @property
    def value(self):
        """ItemDef OID Getter
        """
        return self._value

    @value.setter
    def value(self, itemValue):
        """ItemDef OID Setter
        """
        self._value = itemValue

    @property
    def itemGroupOid(self):
        """ItemGroupOID Getter
        """
        return self._itemGroupOid

    @itemGroupOid.setter
    def itemGroupOid(self, value):
        """ItemGroupOID setter
        """
        self._itemGroupOid = value

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
        return "<CRF item oid: %s, name: %s at %s>" % (self.oid, self.name, adr)