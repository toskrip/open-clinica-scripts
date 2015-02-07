#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Logging
import logging
import logging.config

# SOAP
import pysimplesoap.client
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from pysimplesoap.transport import get_http_wrapper, set_http_wrapper

# Domain
from domain.StudyEventDefinition import StudyEventDefinition
from domain.EventDefinitionCrf import EventDefinitionCrf
from domain.Crf import Crf
from domain.CrfVersion import CrfVersion
from domain.EventDefinitionCrf import EventDefinitionCrf
from domain.StudyEventDefinition import StudyEventDefinition

#----------------------------------------------------------------------
#------------------------------ Constants -----------------------------
STUDYNAMESPACE = "http://openclinica.org/ws/studyEventDefinition/v1"
STUDYACTION = "http://openclinica.org/ws/studyEventDefinition/v1"

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########

class OCStudyEventDefinitionWsService():
    """SOAP web services to OpenClinica
    """

    def __init__(self, studyLocation, proxyStr, proxyUsr, proxyPass, isTrace):
        """Default Constructor
        """
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        proxies = None

        if proxyStr:
            proxies = pysimplesoap.client.parse_proxy(proxyStr)
            self._logger.info("OC EventDef SOAP services with proxies: " + str(proxies))

        self._logger.info("OC EventDef SOAP services with auth: " + str(proxyUsr))

        if proxies:
            self.client = SoapClient(location=studyLocation,
                namespace=STUDYNAMESPACE,
                action=STUDYACTION,
                soap_ns='soapenv',
                ns="v1",
                trace=isTrace,
                proxy=proxies,
                username=proxyUsr,
                password=proxyPass)
        else:
            self.client = SoapClient(location=studyLocation,
                namespace=STUDYNAMESPACE,
                action=STUDYACTION,
                soap_ns='soapenv',
                ns="v1",
                trace=isTrace,
                username=proxyUsr,
                password=proxyPass) 

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def wsse(self, userName, passwordHash):
        """
        """
        self.client['wsse:Security'] = {
            'wsse:UsernameToken': {
                'wsse:Username': userName,
                'wsse:Password': passwordHash,
            }
        }


    def listAllByStudy(self, study):
        """
        """
        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
            <listAllRequest>
            <v1:studyEventDefinitionListAll xmlns:v1="http://openclinica.org/ws/studyEventDefinition/v1">
            <bean:studyRef xmlns:bean="http://openclinica.org/ws/beans">
            <bean:identifier>""" + study.identifier() + """</bean:identifier>
            </bean:studyRef>
            </v1:studyEventDefinitionListAll>
            </listAllRequest>""")

        response = self.client.call('listAllRequest', params)

        studyEventDefinitions = []
        for studyEventDefinition in response.studyEventDefinitions.children():

            oid = str(studyEventDefinition.oid)
            name = str(studyEventDefinition.name)

            eventDefinitionCrfs = []
            for eventDefinitionCrf in studyEventDefinition.eventDefinitionCrfs.children():

                required = str(eventDefinitionCrf.required)
                doubleDataEntry = str(eventDefinitionCrf.doubleDataEntry)
                passwordRequired = str(eventDefinitionCrf.passwordRequired)
                hideCrf = str(eventDefinitionCrf.hideCrf)
                sourceDataVerificaiton = str(eventDefinitionCrf.sourceDataVerificaiton)

                crfOid  = str(eventDefinitionCrf.crf.oid)
                crfName = str(eventDefinitionCrf.crf.name)
                obtainedCrf = Crf(crfOid, crfName)

                defaultCrfVersionOid = str(eventDefinitionCrf.defaultCrfVersion.oid)
                defaultCrfVersionName = str(eventDefinitionCrf.defaultCrfVersion.name)

                obtainedDefaultCrfVersion = CrfVersion(defaultCrfVersionOid, defaultCrfVersionName)

                obtainedEventDefinitionCrf = EventDefinitionCrf(required,
                    doubleDataEntry,
                    passwordRequired,
                    hideCrf,
                    sourceDataVerificaiton,
                    obtainedCrf,
                    obtainedDefaultCrfVersion)

                eventDefinitionCrfs.append(obtainedEventDefinitionCrf)

            obtainedStudyEventDefintion = StudyEventDefinition(oid, name, eventDefinitionCrfs)
            studyEventDefinitions.append(obtainedStudyEventDefintion)

        return studyEventDefinitions

