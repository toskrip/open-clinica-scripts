class ItemGroup():
    """ItemGroup
    """

    def __init__(self, oid="", name=""):
        """Default constructor
        """
        self._oid = oid
        self._name = name
        self._repeating = ""
        self._sasDatasetName = ""

        self._items = []

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

    @property
    def items(self):
        """
        """
        return self._items
        
##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def addItem(self, item):
        """Add eCRF item to the group
        """
        self._items.append(item)

    def getItemG(self, itemOid):
        """
        """
        result = None
        for item in self._items:
            if item.oid == itemOid:
                result = group
                break

        return result

    def __repr__(self):
        """Object representation
        """
        adr = hex(id(self)).upper()
        return "<Item group oid: %s, name: %s at %s>" % (self.oid, self.name, adr)
