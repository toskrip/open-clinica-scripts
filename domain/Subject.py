class Subject():
    """Representation of subject
    """

    def __init__(self, uniqueIdentifier="", gender=""):
        """Default Constructor
        """

        # OC OID
        self._oid = ""
        # OC StudySubjectID
        self._studySubjectId = ""
        # OC Person ID (PID)
        self._uniqueIdentifier = uniqueIdentifier

        # Should depend on study configuration but right now it is mandatory (OC - bug)
        # can be 'm' of 'f'
        self._gender = gender

        # Optional depending on study configuration
        # ISO date string
        self._dateOfBirth = ""
        self._yearOfBirth = ""

        # Subject can be person
        self._person = None

########  ########   #######  ########  ######## ########  ######## #### ########  ######
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ##
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ##
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ##
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ######

    @property
    def oid(self):
        return self._oid

    @oid.setter
    def oid(self, value):
        self._oid = value

    @property
    def studySubjectId(self):
        return self._studySubjectId

    @studySubjectId.setter
    def studySubjectId(self, value):
        self._studySubjectId = value

    @property
    def uniqueIdentifier(self):
        """PID Getter
        """
        return self._uniqueIdentifier

    @uniqueIdentifier.setter
    def uniqueIdentifier(self, uniqueIdentifierValue):
        """PID Setter
        """
        self._uniqueIdentifier = uniqueIdentifier

    @property
    def gender(self):
        """Gender Getter
        """
        return self._gender

    @gender.setter
    def gender(self, genderValue):
        """Gender Setter (m or f)
        """
        if genderValue == "m" or genderValue == "f":
            self._gender = genderValue

    @property
    def person(self):
        """Person Getter
        """
        return self._person

    @person.setter
    def person(self, personRef):
        """Person Setter
        """
        self._person = personRef

    @property
    def dateOfBirth(self):
        return self._dateOfBirth

    @property
    def yearOfBirth(self):
        return self._yearOfBirth

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
        return "<StudySubject oid: %s, ssid: %s at %s>" % (self.oid, self.studySubjectId, adr)