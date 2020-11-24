#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

class StudySubject():
    """Representation of a subject which is enrolled into a Study
    """

    def __init__(self, label="", secondaryLabel="", enrollmentDate="", subject=None, events=[]):
        """Default Constructor
        """
        # OC OID like SS_afasdf
        self._oid = ""

        # StudySubjectID - depend on study paramenter configuration (can be generated automatically)
        self._label = label

        # Optional - if some kind of secondary ID has to be stored
        self._secondaryLabel = secondaryLabel

        # ISO date string of enrollment of subject to the study
        self._enrollmentDate = enrollmentDate

        # Study agnostic entity subject (has person ID)
        self._subject = subject

        # Scheduled events list
        self._events = events

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
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def secondaryLabel(self):
        return self._secondaryLabel

    @secondaryLabel.setter
    def secondaryLabel(self, value):
        self._secondaryLabel = value

    @property
    def enrollmentDate(self):
        """Enrollment date Getter
        ISO formated string
        """
        return self._enrollmentDate

    @enrollmentDate.setter
    def enrollmentDate(self, enrollmentDateValue):
        """Enrollment date Setter
        """
        # TODO: check validity of enrollmentDateValue
        self._enrollmentDate = enrollmentDateValue

    @property
    def subject(self):
        """Subject Getter
        """
        return self._subject

    @subject.setter
    def subject(self, subjectRef):
        """Subject Setter
        """
        self._subject = subjectRef

    @property
    def events(self):
        """Subject events Getter
        """
        return self._events

    @events.setter
    def events(self, eventList):
        """Subject events Setter
        """
        self._events = eventList

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def scheduledEventOccurrenceExists(self, query):
        """Check whether there is scheduled event occurrence with the provided repeat key
        """
        for e in self._events:
            if e.isRepeating:
                if (e.eventDefinitionOID == query.eventDefinitionOID and e.studyEventRepeatKey == query.studyEventRepeatKey):
                    return True

        return False

    def __repr__(self):
        """Object representation
        """
        adr = hex(id(self)).upper()
        return "<StudySubject oid: %s, ssid: %s at %s>" % (self.oid, self.label, adr)

