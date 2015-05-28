######## ##     ## ######## ##    ## ######## 
##       ##     ## ##       ###   ##    ##    
##       ##     ## ##       ####  ##    ##    
######   ##     ## ######   ## ## ##    ##    
##        ##   ##  ##       ##  ####    ##    
##         ## ##   ##       ##   ###    ##    
########    ###    ######## ##    ##    ##  

class Event():
    """Study Event
    This is study event scheduled for specific study subject
    """

    def __init__(self, eventDefinitionOID="", startDate=None, startTime=None):
        """Default constructor
        """
        self._eventDefinitionOID = eventDefinitionOID
        self._name = ""
        self._description = ""
        self._status = ""
        self._category = ""
        self._startDate = startDate
        self._startTime = startTime
        self._isRepeating = False
        self._studyEventRepeatKey = ""
        self._eventType = ""
        self._subjectAgeAtEvent = ""

        self._forms = []

########  ########   #######  ########  ######## ########  ######## #### ########  ######  
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ## 
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##       
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######  
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ## 
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ## 
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ###### 

    @property
    def eventDefinitionOID(self):
        """Event definition OID Getter
        """
        return self._eventDefinitionOID

    @eventDefinitionOID.setter
    def eventDefinitionOID(self, value):
        """Event defintion OID Setter
        """
        if self._eventDefinitionOID != value:
            self._eventDefinitionOID = value

    @property 
    def name(self):
        """Event name Getter
        """
        return self._name

    @name.setter
    def name(self, value):
        """Event name Setter
        """
        if self._name != value:
            self._name = value

    @property
    def description(self):
        """Description Getter
        """
        return self._description

    @description.setter
    def description(self, value):
        """Sescription Setter
        """
        if self._description != value:
            self._description = value

    @property
    def status(self):
        """Status Getter
        """
        return self._status

    @status.setter
    def status(self, value):
        """Status Setter
        """
        if self._status != value:
            self._status = value

    @property
    def category(self):
        """Category Getter
        """
        return self._category

    @category.setter
    def category(self, value):
        """Category Setter
        """
        if self._category != value:
            self._category = value

    @property
    def startDate(self):
        """Study event start date Getter
        """
        return self._startDate

    @startDate.setter
    def startDate(self, value):
        """Study event start date Setter
        """
        self._startDate = value

    @property
    def startTime(self):
        """Study event start time Getter
        """
        return self._startTime

    @startTime.setter
    def startTime(self, value):
        """Study event start time Setter
        """
        self._startTime = value

    @property
    def isRepeating(self):
        """Is repeating Getter
        """
        return self._isRepeating

    @isRepeating.setter
    def isRepating(self, value):
        """Is repeating Setter
        """
        if self._isRepeating != value:
            self._isRepeating = value

    @property
    def studyEventRepeatKey(self):
        """StudyEventRepeatKey Getter
        """
        return self._studyEventRepeatKey

    @studyEventRepeatKey.setter
    def studyEventRepeatKey(self, value):
        """StudyEvent RepeatKey Setter
        """
        if self._studyEventRepeatKey != value:
            self._studyEventRepeatKey = value

    @property
    def eventType(self):
        """Event type Getter
        """
        return self._eventType

    @eventType.setter
    def eventType(self, value):
        """Event type Setter
        """
        if self._eventType != value:
            self._eventType = value

    @property
    def subjectAgeAtEvent(self):
        """Subject age at event Getter
        """
        return self._subjectAgeAtEvent

    @subjectAgeAtEvent.setter
    def subjectAgeAtEvent(self, value):
        """Subject age at event Setter
        """
        if self._subjectAgeAtEvent != value:
            self._subjectAgeAtEvent = value

    @property
    def forms(self):
        """eCRFs Getter
        """
        return self._forms

    @forms.setter
    def forms(self, eCrfs):
        """eCRFs Setter
        """
        self._forms = eCrfs

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def addCrf(self, form):
        """Add eCRF form to the event
        """
        self._forms.append(form)

    def hasScheduledCrf(self, formOid):
        """Verify whether the event has specific CRF scheduled
        """
        result = False

        for crf in self._forms:
            if crf.oid == formOid:
                result = True
                break

        return result

    def getCrf(self, formOid):
        """
        """
        result = None
        for crf in self._forms:
            if crf.oid == formOid:
                result = crf
                break

        return result

    def __repr__(self):
        """Object representation
        """
        adr = hex(id(self)).upper()
        return "<Scheduled event edoid: %s, date: %s at %s>" % (self.eventDefinitionOID, self.startDate, adr)