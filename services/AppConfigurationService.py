#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# System
import sys, platform, os

# Config
from ConfigParser import *

# Singleton
from utils.SingletonType import SingletonType

# Logging
import logging
import logging.config

 ######  ######## ########  ##     ## ####  ######  ######## 
##    ## ##       ##     ## ##     ##  ##  ##    ## ##       
##       ##       ##     ## ##     ##  ##  ##       ##       
 ######  ######   ########  ##     ##  ##  ##       ######   
      ## ##       ##   ##    ##   ##   ##  ##       ##       
##    ## ##       ##    ##    ## ##    ##  ##    ## ##       
 ######  ######## ##     ##    ###    ####  ######  ######## 

class AppConfigurationService(object):
    """Application configuration service

    Usage: AppConfigurationService().get("SectionOne")['name']
    """

    __metaclass__ = SingletonType

    def __init__(self, configFileName):
        """Default Constructor
        """
        # Setup logger - use config file
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        self._logger.info("Reading config file: " + configFileName)
        self.configFileName = configFileName
        self.c = ConfigParser()
        self.configFile = open(configFileName, "r+")
        self.c.readfp(self.configFile)
        self.configFile.close()

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def hasSection(self, section):
        """Check whether the section exists within configuration
        """
        result = False

        try:
            options = self.c.options(section)
            result = True
        except:
            result = False

        return result

    def hasOption(self, section, option):
        """Check whether the section option exists within configuration
        """
        options = self.c.options(section)
        for o in options:
            if o == option:
                return True

        return False

    def get(self, section):
        """Get section options as dictionary
        """
        resultDict = {}

        options = self.c.options(section)
        for option in options:
            try:
                resultDict[option] = self.c.get(section, option)
                if resultDict[option] == -1:
                    self._logger.info("skip: %s" % option)
            except:
                self._logger.error("exception on %s!" % option)
                resultDict[option] = None

        return resultDict

    def getboolean(self, section, option):
        """Get boolean option from section
        """
        return self.c.getboolean(section, option)

    def set(self, section, option, value):
        """Set section option
        """
        self.c.set(section, option, value)

    def add(self, section):
        """Add section to config
        """
        self.c.add_section(section)

    def remove(self, section):
        """Remove section from config
        """
        self.c.remove_section(section)

    def saveConfiguration(self):
        """Write down changes in configuration
        """
        try:
            self._logger.info("Saving configuration to config file.")
            if platform.system() == "Windows":
                self.configFile = open(self.configFileName, "w+")
                self.c.write(self.configFile)
                self.configFile.close()
            else:
                os.remove(self.configFileName)
                self.configFile = open(self.configFileName, "w+")
                self.c.write(self.configFile)
                self.configFile.close()
        except Exception as err:
            self._logger.error("Failed to save configuration: " + err.strerror)
        