#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# System
import sys

# Logging
import logging
import logging.config

# Datetime
from datetime import datetime

# SOAP
import pysimplesoap.client
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement

# Preffer C accelerated version of ElementTree for XML parsing
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# Domain
from domain.StudySubject import StudySubject
from domain.Subject import Subject
from domain.StudyEventDefinition import StudyEventDefinition
from domain.Event import Event

STUDYSUBJECTNAMESPACE = "http://openclinica.org/ws/studySubject/v1"
STUDYSUBJECTACTION = "http://openclinica.org/ws/studySubject/v1"

# Namespace maps for reading of XML
nsmaps = {
    'odm': 'http://www.cdisc.org/ns/odm/v1.3',
    'cdisc': 'http://www.cdisc.org/ns/odm/v1.3',
    'OpenClinica': 'http://www.openclinica.org/ns/odm_ext_v130/v3.1',
    'ns2': 'http://openclinica.org/ws/beans',
    'ns3': 'http://openclinica.org/ws/crf/v1',
    "ns4": "http://openclinica.org/ws/studySubject/v1"
}

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########


class OCStudySubjectWsService():
    """StudySubject SOAP web services to OpenClinica
    """

    def __init__(self, studyLocation, proxyStr, proxyUsr, proxyPass, isTrace):
        """Default Constructor
        """
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        proxies = None

        if proxyStr:
            proxies = pysimplesoap.client.parse_proxy(proxyStr)
            self._logger.info("OC StudySubject SOAP services with proxies: " + str(proxies))

        self._logger.info("OC StudySubject SOAP services with auth: " + str(proxyUsr))

        if proxies:
            self.client = SoapClient(location=studyLocation,
                namespace=STUDYSUBJECTNAMESPACE,
                action=STUDYSUBJECTACTION,
                soap_ns='soapenv',
                ns="v1",
                trace=isTrace,
                proxy=proxies,
                username=proxyUsr,
                password=proxyPass)
        else:
            self.client = SoapClient(location=studyLocation,
                namespace=STUDYSUBJECTNAMESPACE,
                action=STUDYSUBJECTACTION,
                soap_ns='soapenv',
                ns="v1",
                trace=isTrace,
                username=proxyUsr,
                password=proxyPass)   

        self._logger.info("OC StudySubject SOAP services successfully initialised.")

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def wsse(self, userName, passwordHash):
        """Setup security for web service
        """
        self.client['wsse:Security'] = {
            'wsse:UsernameToken': {
                'wsse:Username': userName,
                'wsse:Password': passwordHash,
            }
        }

    def listAllByStudy(self, study, metadata=None):
        """List all study  subject assigned in specified study
        """
        if sys.version < "3":
            query = u"""<?xml version="1.0" encoding="UTF-8"?>
                <listAllByStudyRequest>
                <bean:studyRef xmlns:bean="http://openclinica.org/ws/beans">
                <bean:identifier>%s</bean:identifier>
                </bean:studyRef>
                </listAllByStudyRequest>""" % study.identifier.decode("utf-8")
            params = SimpleXMLElement(query.encode("utf-8"))
        else:
            query = """<?xml version="1.0" encoding="UTF-8"?>
                        <listAllByStudyRequest>
                        <bean:studyRef xmlns:bean="http://openclinica.org/ws/beans">
                        <bean:identifier>%s</bean:identifier>
                        </bean:studyRef>
                        </listAllByStudyRequest>""" % study.identifier
            params = SimpleXMLElement(query)

        response = self.client.call('listAllByStudyRequest', params)

        documentTree = ET.ElementTree(ET.fromstring(response.as_xml()))

        studySubjects = []

        # Locate Study subject data in XML file via XPath
        for studySubject in documentTree.iterfind('.//ns2:studySubject', namespaces=nsmaps):
            label = ""
            secondaryLabel = ""
            enrollmentDate = ""
            uniqueIdentifier = ""
            gender = ""
            
            # Optional
            dateOfBirth = ""
            yearOfBirth = ""

            events = []
            for element in studySubject:
                if (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}label":
                    label = element.text
                elif (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}secondaryLabel":
                    secondaryLabel = element.text
                elif (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}enrollmentDate":
                    enrollmentDate = element.text

                if (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}subject":
                    for subjectElement in element:
                        if (str(subjectElement.tag)).strip() == "{http://openclinica.org/ws/beans}uniqueIdentifier":
                            uniqueIdentifier = subjectElement.text
                        elif (str(subjectElement.tag)).strip() == "{http://openclinica.org/ws/beans}gender":
                            gender = subjectElement.text
                        elif (str(subjectElement.tag)).strip() == "{http://openclinica.org/ws/beans}dateOfBirth":
                            dateOfBirth = subjectElement.text
                        elif (str(subjectElement.tag)).strip() == "{http://openclinica.org/ws/beans}yearOfBirth":
                            yearOfBirth = subjectElement.text

                if (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}events":
                    for event in element:
                        eventDefinitionOID = ""
                        location = ""
                        startDate = ""
                        startTime = ""
                        endDate = ""
                        endTime = ""

                        dateString = ""
                        timeString = ""
                        for eventElement in event:
                            if (str(eventElement.tag)).strip() == "{http://openclinica.org/ws/beans}eventDefinitionOID":
                                eventDefinitionOID = eventElement.text
                            elif (str(eventElement.tag)).strip() == "{http://openclinica.org/ws/beans}location":
                                location = eventElement.text
                            elif (str(eventElement.tag)).strip() == "{http://openclinica.org/ws/beans}startDate":
                                dateString = eventElement.text
                            elif (str(eventElement.tag)).strip() == "{http://openclinica.org/ws/beans}startTime":
                                timeString = eventElement.text

                        # Deal with both date an datetime
                        if timeString == "":
                            format = "%Y-%m-%d"
                            startDate = datetime.strptime(dateString, format)
                        else:
                            # Careful it uses 12/24 hour format
                            format12 = "%Y-%m-%d %I:%M:%S"
                            format24 = "%Y-%m-%d %H:%M:%S"

                            try:
                                startDate = datetime.strptime(dateString + " " + timeString, format12)
                            except ValueError:
                                startDate = datetime.strptime(dateString + " " + timeString, format24)

                        obtainedEvent = Event(eventDefinitionOID, startDate)
                        events.append(obtainedEvent)

            obtainedSubject = Subject(uniqueIdentifier, gender)
            obtainedSubject.dateOfBirth = dateOfBirth
            obtainedSubject.yearOfBirth = yearOfBirth
            obtainedStudySubject = StudySubject(label, secondaryLabel, enrollmentDate, obtainedSubject, events)

            studySubjects.append(obtainedStudySubject)

        # Enhance with information from metadata
        metadataEvents = self.loadEventsFromMetadata(metadata)

        for ss in studySubjects:
            for e in ss.events:
                for me in metadataEvents:
                    if e.eventDefinitionOID == me.oid:
                        e.name = me.name
                        e.description = me.description
                        e.isRepeating = me.repeating
                        e.eventType = me.type
                        e.category = me.category

        result = str(response.result)
        self._logger.debug(result)

        return studySubjects

    def listAllByStudySite(self, study, studySite, metadata=None):
        """List all study subject assigned in specific study and site
        """
        if sys.version < "3":
            query = u"""<?xml version="1.0" encoding="UTF-8"?>
                <listAllByStudyRequest>
                <bean:studyRef xmlns:bean="http://openclinica.org/ws/beans">
                <bean:identifier>%s</bean:identifier>
                </bean:studyRef>
                </listAllByStudyRequest>""" % studySite.identifier.decode("utf-8")
            params = SimpleXMLElement(query.encode("utf-8"))
        else:
            query = """<?xml version="1.0" encoding="UTF-8"?>
                        <listAllByStudyRequest>
                        <bean:studyRef xmlns:bean="http://openclinica.org/ws/beans">
                        <bean:identifier>%s</bean:identifier>
                        </bean:studyRef>
                        </listAllByStudyRequest>""" % studySite.identifier
            params = SimpleXMLElement(query)

        response = self.client.call('listAllByStudyRequest', params)

        documentTree = ET.ElementTree(ET.fromstring(response.as_xml()))

        studySubjects = []

        # Locate Study subject data in XML file via XPath
        for studySubject in documentTree.iterfind('.//ns2:studySubject', namespaces=nsmaps):
            label = ""
            secondaryLabel = ""
            enrollmentDate = ""
            uniqueIdentifier = ""
            gender = ""
            
            # Optional
            dateOfBirth = ""
            yearOfBirth = ""

            events = []
            for element in studySubject:
                if (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}label":
                    label = element.text
                elif (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}secondaryLabel":
                    secondaryLabel = element.text
                elif (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}enrollmentDate":
                    enrollmentDate = element.text

                if (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}subject":
                    for subjectElement in element:
                        if (str(subjectElement.tag)).strip() == "{http://openclinica.org/ws/beans}uniqueIdentifier":
                            uniqueIdentifier = subjectElement.text
                        elif (str(subjectElement.tag)).strip() == "{http://openclinica.org/ws/beans}gender":
                            gender = subjectElement.text
                        elif (str(subjectElement.tag)).strip() == "{http://openclinica.org/ws/beans}dateOfBirth":
                            dateOfBirth = subjectElement.text
                        elif (str(subjectElement.tag)).strip() == "{http://openclinica.org/ws/beans}yearOfBirth":
                            yearOfBirth = subjectElement.text

                if (str(element.tag)).strip() == "{http://openclinica.org/ws/beans}events":
                    for event in element:
                        eventDefinitionOID = ""
                        location = ""
                        startDate = ""
                        startTime = ""
                        endDate = ""
                        endTime = ""

                        dateString = ""
                        timeString = ""
                        for eventElement in event:
                            if (str(eventElement.tag)).strip() == "{http://openclinica.org/ws/beans}eventDefinitionOID":
                                eventDefinitionOID = eventElement.text
                            elif (str(eventElement.tag)).strip() == "{http://openclinica.org/ws/beans}location":
                                location = eventElement.text
                            elif (str(eventElement.tag)).strip() == "{http://openclinica.org/ws/beans}startDate":
                                dateString = eventElement.text     
                            elif (str(eventElement.tag)).strip() == "{http://openclinica.org/ws/beans}startTime":
                                timeString = eventElement.text

                        # Deal with both date an datetime
                        if timeString == "":
                            format = "%Y-%m-%d"
                            startDate = datetime.strptime(dateString, format)
                        else:
                            # Careful it uses 12/24 hour format
                            format12 = "%Y-%m-%d %I:%M:%S"
                            format24 = "%Y-%m-%d %H:%M:%S"

                            try:
                                startDate = datetime.strptime(dateString + " " + timeString, format12)
                            except ValueError:
                                startDate = datetime.strptime(dateString + " " + timeString, format24)

                        obtainedEvent = Event(eventDefinitionOID, startDate)
                        events.append(obtainedEvent)

            obtainedSubject = Subject(uniqueIdentifier, gender)
            obtainedSubject.dateOfBirth = dateOfBirth
            obtainedSubject.yearOfBirth = yearOfBirth
            obtainedStudySubject = StudySubject(label, secondaryLabel, enrollmentDate, obtainedSubject, events)

            studySubjects.append(obtainedStudySubject)

        # Enhance with information from metadata
        metadataEvents = self.loadEventsFromMetadata(metadata)
        
        for ss in studySubjects:
            for e in ss.events:
                for me in metadataEvents:
                    if e.eventDefinitionOID == me.oid:
                        e.name = me.name
                        e.description = me.description
                        e.isRepeating = me.repeating
                        e.eventType = me.type
                        e.category = me.category

        result = str(response.result)
        self._logger.debug(result)

        return studySubjects


    def create(self, studySubject, study, metadata=None):
        """Create new StudySubject in OpenClinica
        """
        result = ""

        #TODO: depending on metadata (secondaryLabel, uniqueIdentifier, dateOfBirth, yearOfBirth, siteIdentifier (multicentric?))

        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
            <createRequest>
            <v1:studySubject xmlns:v1="http://openclinica.org/ws/studySubject/v1">
            <bean:label xmlns:bean="http://openclinica.org/ws/beans">""" + studySubject.label + """</bean:label>
	    <bean:secondaryLabel xmlns:bean="http://openclinica.org/ws/beans">""" + studySubject.secondaryLabel + """</bean:secondaryLabel>
            <bean:enrollmentDate xmlns:bean="http://openclinica.org/ws/beans">
            """ + studySubject.enrollmentDate.isoformat() + """
            </bean:enrollmentDate>
            <bean:subject xmlns:bean="http://openclinica.org/ws/beans">
            <bean:uniqueIdentifier>""" + studySubject.subject.uniqueIdentifier + """</bean:uniqueIdentifier>
            <bean:gender>""" + studySubject.subject.gender + """</bean:gender>
            </bean:subject>
            <bean:studyRef xmlns:bean="http://openclinica.org/ws/beans">
            <bean:identifier>""" + study.identifier + """</bean:identifier>
            </bean:studyRef>
            </v1:studySubject>
            </createRequest>""")

        response = self.client.call('createRequest', params)

        result = str(response.result)
        return result

    def isStudySubject(self, studySubject, study):
        """Check if subject exists in study searching criteria is  StudySubject ID
        """
        result = ""

        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
            <isStudySubjectRequest>
            <v1:studySubject xmlns:v1="http://openclinica.org/ws/studySubject/v1">
            <bean:label xmlns:bean="http://openclinica.org/ws/beans">
            """ + studySubject.label + """
            </bean:label>
            <bean:studyRef xmlns:bean="http://openclinica.org/ws/beans">
            <bean:identifier>""" + study.identifier + """</bean:identifier>
            </bean:studyRef>
            </v1:studySubject>
            </isStudySubjectRequest>""")

        response = self.client.call('isStudySubjectRequest', params)

        result = str(response.result)

        return result

    def loadEventsFromMetadata(self, metadata):
        """Extract a list of Study Event domain objects according to ODM from metadata XML
        """
        studyEvents = []

        # Check if file path is setup
        if (metadata):
            documentTree = ET.ElementTree((ET.fromstring(str(metadata))))

            # First obtain list of references (OIDs) to study events defined in ODM -> Study -> MetaDataVersion -> Protocol
            studyEventRefs = []

            for studyEventRef in documentTree.iterfind('.//odm:StudyEventRef', namespaces=nsmaps):
                studyEventRefs.append(studyEventRef.attrib['StudyEventOID'])
                
                # In case I need this information later
                eventIsMandatory =  studyEventRef.attrib['Mandatory'] == "Yes"
                eventOrderInProtocol = int(studyEventRef.attrib['OrderNumber'])

            # Now for each study event reference find study event definition
            for eventRef in studyEventRefs:
                for element in documentTree.iterfind('.//odm:StudyEventDef[@OID="' + eventRef + '"]', namespaces=nsmaps):
                    studyEvent = StudyEventDefinition()

                    studyEvent.oid = element.attrib['OID']
                    studyEvent.name = element.attrib['Name']
                    studyEvent.repeating = element.attrib['Repeating'] == "Yes"
                    studyEvent.type = element.attrib['Type']
                    studyEvent.mandatory = eventIsMandatory
                    studyEvent.orderNumber = eventOrderInProtocol

                    for eventElement in element:
                        if (str(eventElement.tag)).strip() == "{http://www.openclinica.org/ns/odm_ext_v130/v3.1}EventDefinitionDetails":
                           for detailsElement in eventElement:
                                if (str(detailsElement.tag)).strip() == "{http://www.openclinica.org/ns/odm_ext_v130/v3.1}Description":
                                    studyEvent.description = detailsElement.text
                                elif (str(detailsElement.tag)).strip() == "{http://www.openclinica.org/ns/odm_ext_v130/v3.1}Category":
                                    studyEvent.category = detailsElement.text

                    studyEvents.append(studyEvent)

        # Return resulting study event defintion elements
        return studyEvents
