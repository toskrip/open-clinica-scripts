class CrfDicomField():

 ######   #######  ##    ##  ######  ######## ########  ##     ##  ######  ########  #######  ########   ######
##    ## ##     ## ###   ## ##    ##    ##    ##     ## ##     ## ##    ##    ##    ##     ## ##     ## ##    ##
##       ##     ## ####  ## ##          ##    ##     ## ##     ## ##          ##    ##     ## ##     ## ##
##       ##     ## ## ## ##  ######     ##    ########  ##     ## ##          ##    ##     ## ########   ######
##       ##     ## ##  ####       ##    ##    ##   ##   ##     ## ##          ##    ##     ## ##   ##         ##
##    ## ##     ## ##   ### ##    ##    ##    ##    ##  ##     ## ##    ##    ##    ##     ## ##    ##  ##    ##
 ######   #######  ##    ##  ######     ##    ##     ##  #######   ######     ##     #######  ##     ##  ######

    def __init__(self, oid, value, annotationType, eventOid, formOid, groupOid):
        """Default constructor
        """
        # Init members
        self.__oid = oid
        self.__label = ""
        self.__description = ""
        self.__value = value
        self.__annotationType = annotationType

        self.__eventOid = eventOid
        self.__formOid = formOid
        self.__groupOid = groupOid

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
        return self.__oid

    @property
    def label(self):
        """
        """
        return self.__label

    @label.setter
    def label(self, value):
        """
        """
        if self.__label != value:
            self.__label = value

    @oid.setter
    def oid(self, oidValue):
        """OID Setter
        """
        if self.__oid != oidValue:
            self.__oid = oidValue

    @property
    def value(self):
        """Value Getter
        """
        return self.__value


    @value.setter
    def value(self, value):
        """Value Setter
        """
        if self.__value != value:
            self.__value = value

    @property
    def annotationType(self):
        """Annotation type Getter
        """
        return self.__annotationType


    @annotationType.setter
    def annotationType(self, value):
        """Annotation type Setter
        """
        if self.__annotationType != annotationType:
            self.__annotationType = annotationType

    @property
    def eventOid(self):
        """EventOid Getter
        """
        return self.__eventOid

    @eventOid.setter
    def eventOid(self, eventOid):
        """EventOid Setter
        """
        if self.__eventOid != eventOid:
            self.__eventOid = eventOid

    @property
    def formOid(self):
        """FormOid Getter
        """
        return self.__formOid


    @formOid.setter
    def formOid(self, formOid):
        """FormOid Setter
        """
        if self.__formOid != formOid:
            self.__formOid = formOid

    @property
    def groupOid(self):
        """GroupOid Getter
        """
        return self.__groupOid


    @groupOid.setter
    def groupOid(self, groupOid):
        """Group Setter
        """
        if self.__groupOid != groupOid:
            self.__groupOid = groupOid

