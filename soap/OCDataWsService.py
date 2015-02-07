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

STUDYNAMESPACE = "http://openclinica.org/ws/data/v1"
STUDYACTION = "http://openclinica.org/ws/data/v1/"

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########

class OCDataWsService():
    """SOAP import data web services to OpenClinica
    """

    def __init__(self, studyLocation, proxyStr, proxyUsr, proxyPass, isTrace):
        """Default Constructor
        """
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        proxies = None

        if proxyStr:
            proxies = pysimplesoap.client.parse_proxy(proxyStr)
            self._logger.info("OC Data SOAP services with proxies: " + str(proxies))

        self._logger.info("OC Data SOAP services with auth: " + str(proxyUsr))

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
        """Setup WSSE security
        """
        self.client['wsse:Security'] = {
            'wsse:UsernameToken': {
                'wsse:Username': userName,
                'wsse:Password': passwordHash,
            }
        }

    def importData(self, odm):
        """Import ODM formated study data
        """
        xmlstring = """<?xml version="1.0" encoding="UTF-8"?><importRequest>""" + odm + """</importRequest>"""

        params = SimpleXMLElement(xmlstring)

        response = self.client.call("importRequest", params)

        return str(response.result)
