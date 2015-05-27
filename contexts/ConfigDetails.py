#### ##     ## ########   #######  ########  ########  ######Lo
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Singleton
from utils.SingletonType import SingletonType

class ConfigDetails(object):
    """Application configuration details
    """

    __metaclass__ = SingletonType

    def __init__(self):
        """Default Constructor
        """
        # Configuration file
        self.configFileName = "oc-client.cfg"

        # Static burned in values
        self.name = "OpenClinica - Desktop Client"
        self.identifier = "OC-DESKTOP-CLIENT"
        self.version = "1.0.0.0"
        self.copyright = "2013-2015 Tomas Skripcak"
        self.logFilePath = ""

        # GUI settings - default
        self.width = 800
        self.height = 600

        # Values read from config file
        self.ocHost = ""
        self.ocPort = ""
        self.ocWsHost = ""
        self.ocWsPort = ""

        # Proxy
        self.proxyEnabled = ""
        self.proxyHost = ""
        self.proxyPort = ""
        self.noProxy = ""

        # Proxy auth
        self.proxyAuthEnabled = ""
        self.proxyAuthLogin = ""
        self.proxyAuthPassword = ""
       