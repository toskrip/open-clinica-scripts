#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Datetime
from datetime import datetime


class Subject(object):
    """Representation of RPB study subject entity
    
    RPB study subject is RPB middleware entity that can
    aggregate patient data across RPB subsystems (EDC, PACS, PID)
    """

 ######   #######  ##    ##  ######  ######## ########  ##     ##  ######  ######## 
##    ## ##     ## ###   ## ##    ##    ##    ##     ## ##     ## ##    ##    ##    
##       ##     ## ####  ## ##          ##    ##     ## ##     ## ##          ##    
##       ##     ## ## ## ##  ######     ##    ########  ##     ## ##          ##    
##       ##     ## ##  ####       ##    ##    ##   ##   ##     ## ##          ##    
##    ## ##     ## ##   ### ##    ##    ##    ##    ##  ##     ## ##    ##    ##    
 ######   #######  ##    ##  ######     ##    ##     ##  #######   ######     ##  

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

        # Subject can be person with identity
        self._person = None

        # StudySubject status
        self._status = ""

        # Subject can have associated DICOM studies
        self._dicomData = []

        # Subject can have scheduled study events
        self._studyEventData = []

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
    def uniqueIdentifier(self, value):
        """PID Setter
        """
        if self._uniqueIdentifier != value:
            self._uniqueIdentifier = value

    @property
    def gender(self):
        """Gender Getter
        """
        return self._gender

    @gender.setter
    def gender(self, genderValue):
        """Gender Setter (m or f)
        """
        if self._gender != genderValue:
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
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def dateOfBirth(self):
        """Date of birth Getter
        """
        return self._dateOfBirth

    @dateOfBirth.setter
    def dateOfBirth(self, value):
        """Date of birth Setter
        """
        self._dateOfBirth = value

    @property
    def yearOfBirth(self):
        """Year of birth Getter
        """
        if self._yearOfBirth is not None and self._yearOfBirth != "":
            return self._yearOfBirth
        elif self._dateOfBirth is not None and self._dateOfBirth != "":
            edcDateFormat = "%Y-%m-%d"
            return datetime.strptime(self._dateOfBirth, edcDateFormat).year

        return self._yearOfBirth

    @yearOfBirth.setter
    def yearOfBirth(self, value):   
        """Year of birth Setter
        """
        self._yearOfBirth = value

    @property 
    def dicomData(self):
        """DICOM studies Getter
        """
        return self._dicomData

    @dicomData.setter
    def dicomData(self, dicomData):
        """DICOM data Setter
        """
        self._dicomData = dicomData

    @property
    def studyEventData(self):
        """Scheduled study events Getter
        """
        return self._studyEventData

    @studyEventData.setter
    def studyEventData(self, studyEventData):
        """Scheduled study events Setter
        """
        self._studyEventData = studyEventData

##     ## ######## ######## ##     ##  #######  ########   ######
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ##
#### #### ##          ##    ##     ## ##     ## ##     ## ##
## ### ## ######      ##    ######### ##     ## ##     ##  ######
##     ## ##          ##    ##     ## ##     ## ##     ##       ##
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ##
##     ## ########    ##    ##     ##  #######  ########   ######

    def atrSize(self):
        return 2