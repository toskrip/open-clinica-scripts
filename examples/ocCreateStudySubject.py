import sys, os
from datetime import date

sys.path.insert(0,os.path.abspath("./../"))

# Contexts
from contexts.OCUserDetails import OCUserDetails

# Services
from soap.OCConnectInfo import OCConnectInfo
from soap.OCWebServices import OCWebServices

# Domain
from domain.StudySubject import StudySubject
from domain.Subject import Subject

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

newStudySubject = StudySubject()
newStudySubject.subject = Subject()

# Based on study subject id generation
# if manual than specify
# even if automatic it has to be empty string
newStudySubject.label = ""

# Based on metadata (can be optional)
newStudySubject.subject.uniqueIdentifier = ""

# SecondaryId, BUG OC ignores secondary ID
#newStudySubject.secondaryId = ""

# Should depend on study configuration, BUG OC always requires gender
newStudySubject.subject.gender = "f"
#newStudySubject.subject.gender = "f"

# OC requires ISO formated date
newStudySubject.enrollmentDate = date.today()

ocWebServices.createStudySubject(newStudySubject, selectedStudy)