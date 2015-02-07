class StudySubject():
    """Representation of a subject which is enrolled into a Study
    """

    #-------------------------------------------------------------------
    #-------------------- Constuctor -----------------------------------

    def __init__(self, label="", secondaryLabel="", enrollmentDate="", subject=None, events=[]):
        """Concsturoctor
        """
        # OC OID like SS_afasdf
        self._oid = ""

        # StudySubjectID - depend on study paramenter configuration (can be generated automatically)
        self.__label = label

        # Optional - if some kind of secondary ID has to be stored
        self.__secondaryLabel = secondaryLabel

        # ISO date string of enrollment of subject to the study
        self.__enrollmentDate = enrollmentDate

        self.__subject = subject
        self.__events = events

    #-------------------------------------------------------------------
    #-------------------- Properties -----------------------------------

    @property
    def oid(self):
        return self._oid

    @oid.setter
    def oid(self, value):
        self._oid = value

    def label(self):
        return self.__label

    def secondaryLabel(self):
        return self.__secondaryLabel

    @property
    def enrollmentDate(self):
        """Enrollment date Getter
        ISO formated string
        """
        return self.__enrollmentDate

    @enrollmentDate.setter
    def enrollmentDate(self, enrollmentDateValue):
        """Enrollment date Setter
        """
        if self.__enrollmentDate != enrollmentDateValue:
            # TODO: check validity of enrollmentDateValue
            self.__enrollmentDate = enrollmentDateValue

    @property
    def subject(self):
        """Subject Getter
        """
        return self.__subject

    @subject.setter
    def subject(self, subjectRef):
        """Subject Setter
        """
        self.__subject = subjectRef

    @property
    def events(self):
        """Subject events Getter
        """
        return self.__events

    @events.setter
    def events(self, eventList):
        """Subject events Setter
        """
        self.__events = eventList

    #-------------------------------------------------------------------
    #----------------------- Methods -----------------------------------

    def atrSize(self):
        return 3

