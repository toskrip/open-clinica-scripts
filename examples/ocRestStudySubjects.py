import sys, os

sys.path.insert(0,os.path.abspath("./../"))

# Contexts
from contexts.ConfigDetails import ConfigDetails
from contexts.UserDetails import UserDetails
from contexts.OCUserDetails import OCUserDetails

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
# Debug lvls ... trace=logging.INFO, trace=logging.DEBUG in OCWebServices constructor 
ocWebServices = OCWebServices(ocConnectInfo)

successfull = False
try:
    successfull, studies = ocWebServices.listAllStudies()
except:
    print "Cannot communicate with the server, no network connection or the server is not running."

if successfull:
    for study in studies:
        selectedStudy = study
        break

ConfigDetails().ocHost = "http://skripcak.net:8080/OpenClinica"
ConfigDetails().ocPort = "80"

UserDetails().username = OCUserDetails().username
UserDetails().clearpass = password

svcHttp = HttpConnectionService(
	ConfigDetails().ocHost, 
	ConfigDetails().ocPort, 
	UserDetails()
)

# From rest output we can reade SubjectKey (OID) which is not accessible via SOAP
restSubjects = svcHttp.getStudyCasebookSubjects(
        [ConfigDetails().ocHost, selectedStudy.oid]
    )

for restSubject in restSubjects:
	print restSubject