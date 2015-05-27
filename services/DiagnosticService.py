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

# HTTP
import urllib2
import requests

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########

class DiagnosticService():
    """This service is providing connection diangnostic features
    """

    def __init__(self):
        """Default constructor
        """
        # Setup logger - use logging config file
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
        

    def ProxyDiagnostic(self):
        """Diagnose
        """
        self._logger.info("Checking proxy setting within environment.")
        
        self._logger.info("Proxies detected within urllib2:")
        proxies = urllib2.getproxies()
        self._logger.info(proxies)

        self._logger.info("Proxies detected within requests:")
        proxies = requests.utils.get_environ_proxies("")
        self._logger.info(proxies)
