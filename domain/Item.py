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
        self.__oid = ""
        self.__name = ""
        self.__description = ""
        self.__dataType = ""
        self.__label = ""
        self.__value = ""

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
        return self.__oid

    @oid.setter
    def oid(self, value):
        """ItemDef OID Setter
        """
        self.__oid = value

    @property
    def name(self):
        """
        """
        return self.__name

    @name.setter
    def name(self, value):
        """
        """
        self.__name = value

    @property
    def description(self):
        """
        """
        return self.__description

    @description.setter
    def description(self, value):
        """
        """
        self.__description = value

    @property
    def label(self):
        """
        """
        return self.__label

    @label.setter
    def label(self, value):
        """
        """
        self.__label = value

    @property
    def dataType(self):
        """
        """
        return self.__dataType

    @dataType.setter
    def dataType(self, value):
        """
        """
        self.__dataType = value

    @property
    def value(self):
        """ItemDef OID Getter
        """
        return self.__value

    @value.setter
    def value(self, itemValue):
        """ItemDef OID Setter
        """
        self.__value = itemValue
