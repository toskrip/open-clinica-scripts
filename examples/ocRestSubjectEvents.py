import sys, os

sys.path.insert(0,os.path.abspath("./../"))

# Contexts
from contexts.OCUserDetails import OCUserDetails
from contexts.ConfigDetails import ConfigDetails
from contexts.UserDetails import UserDetails

# Services
from rest.HttpConnectionService import HttpConnectionService
from soap.OCConnectInfo import OCConnectInfo
from soap.OCWebServices import OCWebServices

ocWsHost = "http://skripcak.net:8080/OpenClinica-ws"
password = "user1_workshop"

OCUserDetails().username = "user1"
OCUserDetails().connected = False

# Create connection artefact to users main OpenClinica SOAP 
ocConnectInfo = OCConnectInfo(
    ocWsHost, 
    OCUserDetails().username
)
ocConnectInfo.setPassword(password)

# Initialise SOAP services    
ocWebServices = OCWebServices(ocConnectInfo)

successfull = False
try:
    successfull, studies = ocWebServices.listAllStudies()
except:
    print "Cannot communicate with the server, no network connection or the server is not running."

if successfull:
    for study in studies:
        selectedStudy = study
        sucessfull, studyMetadata = ocWebServices.getStudyMetadata(selectedStudy)
        break

# Load subject for whole study or only site if it is multicentre study
if selectedStudy and selectedStudy.isMulticentre:
    studySubjects = ocWebServicees.listAllStudySubjectsByStudySite(
        [selectedStudy, selectedStudySite, studyMetadata]
    )
else:
    studySubjects = ocWebServices.listAllStudySubjectsByStudy(
        [selectedStudy, studyMetadata]
    )

ConfigDetails().ocHost = "http://skripcak.net:8080/OpenClinica"
ConfigDetails().ocPort = "80"

UserDetails().username = OCUserDetails().username
UserDetails().clearpass = password

svcHttp = HttpConnectionService(
    ConfigDetails().ocHost, 
    ConfigDetails().ocPort, 
    UserDetails()
)

restSubjects = svcHttp.getStudyCasebookSubjects(
    [ConfigDetails().ocHost, selectedStudy.oid]
)

# Enhance with subject OID
for studySubject in studySubjects:
    for sREST in restSubjects:
        if sREST.studySubjectId == studySubject.label:
            studySubject.oid = sREST.oid
            break

subjectOid = "SS_1"
for subject in studySubjects:
    if subject.oid == subjectOid:
        selectedStudySubject = subject
        break

restEvents = svcHttp.getStudyCasebookEvents( 
        [ConfigDetails().ocHost, selectedStudy.oid, selectedStudySubject.oid]
    )


# SOAP events
for event in selectedStudySubject.events:
    # Enhance with information from REST
    for e in restEvents:
        if e.eventDefinitionOID == event.eventDefinitionOID and e.startDate.isoformat() == event.startDate.isoformat():
            # Read status and repeat key (repeat key importat for import)
            event.status = e.status
            event.studyEventRepeatKey = e.studyEventRepeatKey
            
            # Detailed forms
            event.forms = e.forms
            
            print event
            for crf in event.forms:
                print crf
                for item in crf.items:
                    print item