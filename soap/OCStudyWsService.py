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

# Domain
from domain.Study import Study
from domain.StudySite import StudySite

# SOAP
import pysimplesoap.client
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement

# Preffer C accelerated version of ElementTree for XML parsing
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

STUDYNAMESPACE = "http://openclinica.org/ws/study/v1"
STUDYACTION = "http://openclinica.org/ws/study/v1/"

# Namespace maps for reading of XML
nsmaps = { 
    'odm': 'http://www.cdisc.org/ns/odm/v1.3', 
    'cdisc' : 'http://www.cdisc.org/ns/odm/v1.3', 
    "study": "http://openclinica.org/ws/study/v1" 
}

# ("xsl", "http://www.w3.org/1999/XSL/Transform")
# ("beans", "http://openclinica.org/ws/beans")
# ("study", "http://openclinica.org/ws/study/v1")
# ("OpenClinica", "http://www.openclinica.org/ns/odm_ext_v130/v3.1")

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########


class OCStudyWsService():
    """SOAP web services to OpenClinica
    Study metadata, studies and study sites
    """

    def __init__(self, studyLocation, proxyStr, proxyUsr, proxyPass, isTrace):
        """Default Constructor
        """
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        proxies = None

        if proxyStr:
            proxies = pysimplesoap.client.parse_proxy(proxyStr)
            self._logger.info("OC Study SOAP services with proxies: " + str(proxies))

        self._logger.info("OC Study SOAP services with auth: " + str(proxyUsr))

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

        self._logger.info("OC Study SOAP services sucesfully initialised.")
        
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

    def getMetadata(self, study):
        """Get XML ODM metadata for specified study
        """
        if sys.version < "3":
            query = u"""<?xml version="1.0" encoding="UTF-8"?>
                <getMetadataRequest>
                <v1:studyMetadata xmlns:v1="http://openclinica.org/ws/study/v1">
                <bean:identifier xmlns:bean="http://openclinica.org/ws/beans">%s</bean:identifier>
                </v1:studyMetadata>
                </getMetadataRequest>""" % study.identifier.decode("utf-8")
            params = SimpleXMLElement(query.encode("utf-8"))
        else:
            query = """<?xml version="1.0" encoding="UTF-8"?>
                        <getMetadataRequest>
                        <v1:studyMetadata xmlns:v1="http://openclinica.org/ws/study/v1">
                        <bean:identifier xmlns:bean="http://openclinica.org/ws/beans">%s</bean:identifier>
                        </v1:studyMetadata>
                        </getMetadataRequest>""" % study.identifier
            params = SimpleXMLElement(query)

        response = self.client.call('getMetadataRequest', params)

        metadata = str(response.odm)

        # Result of WS call
        result = str(response.result)
        return result, metadata

    def listAll(self):
        """Get hierarchical list of studies together with their study sites
        """
        studies = []

        query = u"""<?xml version="1.0" encoding="UTF-8"?><listAllRequest />"""

        params = SimpleXMLElement(query.encode("utf-8"))
        response = self.client.call('listAllRequest', params)

        documentTree = ET.ElementTree(ET.fromstring(response.as_xml()))

        # Locate Study data in XML file via XPath
        for study in documentTree.iterfind('.//study:study', namespaces=nsmaps):
            identifier = ""
            oid = ""
            name = ""
            sites = []
            for element in study:
                print(element.tag)
                if (str(element.tag)).strip() == "{http://openclinica.org/ws/study/v1}identifier":
                    identifier = element.text
                elif (str(element.tag)).strip() == "{http://openclinica.org/ws/study/v1}oid":
                    oid = element.text
                elif (str(element.tag)).strip() == "{http://openclinica.org/ws/study/v1}name":
                    name = element.text

                if (str(element.tag)).strip() == "{http://openclinica.org/ws/study/v1}sites":
                    for site in element:
                        siteid = ""
                        siteoid = ""
                        sitename = ""
                        for siteelement in site:
                            if (str(siteelement.tag)).strip() == "{http://openclinica.org/ws/study/v1}identifier":
                                siteid = siteelement.text
                            elif (str(siteelement.tag)).strip() == "{http://openclinica.org/ws/study/v1}oid":
                                siteoid = siteelement.text
                            elif (str(siteelement.tag)).strip() == "{http://openclinica.org/ws/study/v1}name":
                                sitename = siteelement.text

                        obtainedSite = StudySite(siteid, siteoid, sitename)
                        sites.append(obtainedSite)

            obtainedStudy = Study(identifier, oid, name)
            obtainedStudy.sites = sites
            studies.append(obtainedStudy)

        # Result of WS call
        result = str(response.result)
        return result, studies
        