class Subject():
    """Representation of subject
    This
    """

    #-------------------------------------------------------------------
    #-------------------- Constuctor -----------------------------------

    def __init__(self, uniqueIdentifier="", gender=""):
        """Constructor
        """

        # OC OID
        self._oid = ""
        # OC StudySubjectID
        self._studySubjectId = ""
        # OC Person ID (PID)
        self.__uniqueIdentifier = uniqueIdentifier

        # Should depend on study configuration but right now it is mandatory (OC - bug)
        # can be 'm' of 'f'
        self.__gender = gender

        # Optional depending on study configuration
        # ISO date string
        self.__dateOfBirth = ""
        self.__yearOfBirth = ""

        # Subject can be person
        self.__person = None

    #-------------------------------------------------------------------
    #-------------------- Properties -----------------------------------

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
        return self.__uniqueIdentifier

    @uniqueIdentifier.setter
    def uniqueIdentifier(self, uniqueIdentifierValue):
        """PID Setter
        """
        if self.__uniqueIdentifier != uniqueIdentifier:
            self.__uniqueIdentifier = uniqueIdentifier

    @property
    def gender(self):
        """Gender Getter
        """
        return self.__gender

    @gender.setter
    def gender(self, genderValue):
        """Gender Setter (m or f)
        """
        if self.__gender != genderValue:
            if genderValue == "m" or genderValue == "f":
                self.__gender = genderValue

    @property
    def person(self):
        """Person Getter
        """
        return self.__person

    @person.setter
    def person(self, personRef):
        """Person Setter
        """
        self.__person = personRef

    def dateOfBirth(self):
        return self.__dateOfBirth

    def yearOfBirth(self):
        return self.__yearOfBirth

    #-------------------------------------------------------------------
    #----------------------- Methods -----------------------------------

    def atrSize(self):
        return 2

    def __repr__(self):
        """Object representation
        """
        adr = hex(id(self)).upper()
        return "<StudySubject oid: %s, ssid: %s at %s>" % (self.oid, self.studySubjectId, adr)