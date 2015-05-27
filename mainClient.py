#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import sys, os, platform

# Logging
import logging
import logging.config

# PyQt
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow

# Contexts
from contexts.ConfigDetails import ConfigDetails
from contexts.OCUserDetails import OCUserDetails

# UI
from gui.LoginDialog import LoginDialog
from gui.mainClientUI import MainWindowUI

# Services
from services.DiagnosticService import DiagnosticService
from services.AppConfigurationService import AppConfigurationService

##      ## #### ##    ## ########   #######  ##      ##
##  ##  ##  ##  ###   ## ##     ## ##     ## ##  ##  ##
##  ##  ##  ##  ####  ## ##     ## ##     ## ##  ##  ##
##  ##  ##  ##  ## ## ## ##     ## ##     ## ##  ##  ##
##  ##  ##  ##  ##  #### ##     ## ##     ## ##  ##  ##
##  ##  ##  ##  ##   ### ##     ## ##     ## ##  ##  ##
 ###  ###  #### ##    ## ########   #######   ###  ###

EXIT_CODE_RESTART = -123456789 # any value

class MainWindow(QMainWindow, MainWindowUI):
    """Main window view shell
    Main view shell where the other modules views are registered
    """
    def __init__(self,  parent=None):
        """Constructor of main application widnow
        """
        QMainWindow.__init__(self, parent)

        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        exit_code = EXIT_CODE_RESTART

        #-----------------------------------------------------------------------
        #--------------------- Create Module UI --------------------------------
        self.setupUi(self)
        self.statusBar.showMessage("Ready")

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def connectToOpenClinica(self):
        """Connection to OpenClinica SOAP web services
        """
        if (OCUserDetails().connected != True):
            QtGui.QMessageBox.warning(self, "Error", "Cannot connect to OpenClinica SOAP services!")
        else:
            return True

##     ##    ###    #### ##    ##
###   ###   ## ##    ##  ###   ##
#### ####  ##   ##   ##  ####  ##
## ### ## ##     ##  ##  ## ## ##
##     ## #########  ##  ##  ####
##     ## ##     ##  ##  ##   ###
##     ## ##     ## #### ##    ##

def startup():
    """Start the client/upgrade
    """
    logger = logging.getLogger(__name__)
    logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

    # Apply app configuration according the config file
    configure()

    # Log the version of client (useful for remote debuging)
    logger.info(ConfigDetails().name + " version: " + ConfigDetails().version)

    # Basic services
    svcDiagnostic = DiagnosticService()
    svcDiagnostic.ProxyDiagnostic()

    # App log
    app = QtGui.QApplication(sys.argv)
    ConfigDetails().logFilePath = (str(QtCore.QDir.currentPath())) + os.sep + "client.log"

    # Continue with standard login dialog
    loginDialog = LoginDialog()
    if loginDialog.exec_() == QtGui.QDialog.Accepted:

        # Main application window
        ui = MainWindow()
        ui.show()
                
        currentExitCode = app.exec_()
        return currentExitCode

def main():
    """Main function
    """
    currentExitCode = EXIT_CODE_RESTART

    while currentExitCode == EXIT_CODE_RESTART:
        currentExitCode = 0
        currentExitCode = startup()

 ######   #######  ##    ## ######## ####  ######   
##    ## ##     ## ###   ## ##        ##  ##    ##  
##       ##     ## ####  ## ##        ##  ##        
##       ##     ## ## ## ## ######    ##  ##   #### 
##       ##     ## ##  #### ##        ##  ##    ##  
##    ## ##     ## ##   ### ##        ##  ##    ##  
 ######   #######  ##    ## ##       ####  ######   

def configure():
    """Read configuration settings from config file
    """
    appConfig = AppConfigurationService(ConfigDetails().configFileName)
    
    section = "OpenClinica"
    if appConfig.hasSection(section):
        option = "host"
        if appConfig.hasOption(section, option):
            ConfigDetails().ocHost = appConfig.get(section)[option]
        option = "port"
        if appConfig.hasOption(section, option):
            ConfigDetails().ocPort = appConfig.get(section)[option]

    section = "OpenClinica-ws"
    if appConfig.hasSection(section):
        option = "host"
        if appConfig.hasOption(section, option):
            ConfigDetails().ocWsHost = appConfig.get(section)[option]
        option = "port"
        if appConfig.hasOption(section, option):
            ConfigDetails().ocWsPort = appConfig.get(section)[option]

    section = "Proxy"
    if appConfig.hasSection(section):
        option = "enabled"
        if appConfig.hasOption(section, option):
            ConfigDetails().proxyEnabled = appConfig.getboolean(section, option)
        option = "host"
        if appConfig.hasOption(section, option):
            ConfigDetails().proxyHost = appConfig.get(section)[option]
        option = "port"
        if appConfig.hasOption(section, option):
            ConfigDetails().proxyPort = appConfig.get(section)[option]
        option = "noproxy"
        if appConfig.hasOption(section, option):
            ConfigDetails().noProxy = appConfig.get(section)[option]

    section = "Proxy-auth"
    if appConfig.hasSection(section):
        option = "enabled"
        if appConfig.hasOption(section, option):
            ConfigDetails().proxyAuthEnabled = appConfig.getboolean(section, option)
        option = "login"
        if appConfig.hasOption(section, option):
            ConfigDetails().proxyAuthLogin = appConfig.get(section)[option]
        option = "password"
        if appConfig.hasOption(section, option):
            ConfigDetails().proxyAuthPassword = appConfig.get(section)[option]

    section = "GUI"
    if appConfig.hasSection(section):
        option = "main.width"
        if appConfig.hasOption(section, option):
            ConfigDetails().width = int(appConfig.get(section)[option])
        option = "main.height"
        if appConfig.hasOption(section, option):
            ConfigDetails().height = int(appConfig.get(section)[option])

if __name__ == '__main__':
    main()
    