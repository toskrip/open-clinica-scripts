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

# Date
from datetime import datetime

# SOAP
import pysimplesoap.client
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from pysimplesoap.transport import get_http_wrapper, set_http_wrapper

#----------------------------------------------------------------------
#------------------------------ Constants -----------------------------
STUDYNAMESPACE = "http://openclinica.org/ws/event/v1"
STUDYACTION = "http://openclinica.org/ws/event/v1"

class OCEventWsService():
    """SOAP web services for openclinica
    Sheduling study events for study subject
    """

    #----------------------------------------------------------------------
    #--------------------------- Constructors -----------------------------

    def __init__(self, studyLocation, proxyStr, proxyUsr, proxyPass, isTrace):
        """Constructor
        """
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        proxies = None

        if proxyStr:
            proxies = pysimplesoap.client.parse_proxy(proxyStr)
            self._logger.info("OC Event SOAP services with proxies: " + str(proxies))

        self._logger.info("OC Event SOAP services with auth: " + str(proxyUsr))

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

    def schedule(self, study, site, studySubject, event):
        """Shedule study event for specified study subject
        """
        result = ""

        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
            <scheduleRequest>
            <v1:event xmlns:v1="http://openclinica.org/ws/event/v1">
            <bean:studySubjectRef xmlns:bean="http://openclinica.org/ws/beans">
            <bean:label>""" + studySubject.label()  + """</bean:label>
            </bean:studySubjectRef>
            <bean:studyRef xmlns:bean="http://openclinica.org/ws/beans">
            <bean:identifier>""" + study.identifier() + """</bean:identifier>
            <bean:siteRef>
            <bean:identifier>""" + site.identifier + """</bean:identifier>
            </bean:siteRef>
            </bean:studyRef>
            <bean:eventDefinitionOID xmlns:bean="http://openclinica.org/ws/beans">""" +  event.oid() + """</bean:eventDefinitionOID>
            <bean:location xmlns:bean="http://openclinica.org/ws/beans">""" + site.name + """</bean:location>
            <bean:startDate xmlns:bean="http://openclinica.org/ws/beans">""" + datetime.strftime(datetime.now(), "%Y-%m-%d") + """</bean:startDate>
            </v1:event>
            </scheduleRequest>""")

        response = self.client.call('scheduleRequest', params)

        # Result of WS call
        result = str(response.result)
        return result

