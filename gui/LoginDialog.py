#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import sys

# Hashing
import hashlib

# PyQt
from PyQt4 import QtGui, QtCore, uic

# Contexts
from contexts.UserDetails import UserDetails
from contexts.OCUserDetails import OCUserDetails
from contexts.ConfigDetails import ConfigDetails

# Services
from soap.OCConnectInfo import OCConnectInfo
from soap.OCWebServices import OCWebServices

# Resource images for buttons
from gui import images_rc

########  ####    ###    ##        #######   ######
##     ##  ##    ## ##   ##       ##     ## ##    ##
##     ##  ##   ##   ##  ##       ##     ## ##
##     ##  ##  ##     ## ##       ##     ## ##   ####
##     ##  ##  ######### ##       ##     ## ##    ##
##     ##  ##  ##     ## ##       ##     ## ##    ##
########  #### ##     ## ########  #######   ######

class LoginDialog(QtGui.QDialog):
    """Login Dialog Class
    """

    def __init__(self):
        """Default constructor
        """
        # Setup GUI
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("OpenClinica - Login")
        appIconPath =':/images/rpb-icon.jpg'
        appIcon = QtGui.QIcon()
        appIcon.addPixmap(QtGui.QPixmap(appIconPath));
        self.setWindowIcon(appIcon)

        toolBarButtonSize = 15

        # Dialog layout root
        rootLayout = QtGui.QVBoxLayout(self)

        # Login grid
        loginLayout = QtGui.QGridLayout()
        loginLayout.setSpacing(10)
        rootLayout.addLayout(loginLayout)

        # Connection
        lblConnection = QtGui.QLabel("Connection:")
        self.txtConnection = QtGui.QLineEdit()
        self.txtConnection.setText(ConfigDetails().ocHost + "/")
        self.txtConnection.setMinimumWidth(300)
        self.txtConnection.setDisabled(True)

        # User label
        lblUsername = QtGui.QLabel("Username:")
        self.txtUsername = QtGui.QLineEdit()

        # Password label
        lblPassword = QtGui.QLabel("Password:")
        self.txtPassword = QtGui.QLineEdit()
        self.txtPassword.setEchoMode(QtGui.QLineEdit.Password)

        # Login button
        loginIconPath =':/images/login.png'
        loginIcon = QtGui.QIcon()
        loginIcon.addPixmap(QtGui.QPixmap(loginIconPath))

        self.btnLogin = QtGui.QPushButton("Login")
        self.btnLogin.setIcon(loginIcon)
        self.btnLogin.setToolTip("Login")
        self.btnLogin.setIconSize(QtCore.QSize(toolBarButtonSize, toolBarButtonSize))
        self.btnLogin.clicked.connect(self.handleLogin)

        # Add to connection layout
        loginLayout.addWidget(lblConnection, 0, 0)
        loginLayout.addWidget(self.txtConnection, 0, 2)
        loginLayout.addWidget(lblUsername, 1, 0)
        loginLayout.addWidget(self.txtUsername, 1, 1, 1, 2)

        loginLayout.addWidget(lblPassword, 2, 0)
        loginLayout.addWidget(self.txtPassword, 2, 1, 1, 2)

        loginLayout.addWidget(self.btnLogin, 3, 1, 1, 2)

        self.txtUsername.setFocus()

        #------------------------------------------------------------------
        #------------------ ViewModel -------------------------------------
        self.userName = ""
        self.password = ""

##     ##    ###    ##    ## ########  ##       ######## ########   ######  
##     ##   ## ##   ###   ## ##     ## ##       ##       ##     ## ##    ## 
##     ##  ##   ##  ####  ## ##     ## ##       ##       ##     ## ##       
######### ##     ## ## ## ## ##     ## ##       ######   ########   ######  
##     ## ######### ##  #### ##     ## ##       ##       ##   ##         ## 
##     ## ##     ## ##   ### ##     ## ##       ##       ##    ##  ##    ## 
##     ## ##     ## ##    ## ########  ######## ######## ##     ##  ###### 
    
    def handleLogin(self):
        """Send authenticate user message to site server
        """
        username = str(self.txtUsername.text())
        password = str(self.txtPassword.text())
        passwordHash = hashlib.sha1(password).hexdigest()

        # Create connection artefact to users main OpenClinica SOAP 
        ocConnectInfo = OCConnectInfo(ConfigDetails().ocWsHost, username)
        ocConnectInfo.setPasswordHash(passwordHash)

        if ConfigDetails().proxyEnabled:
            ocWebServices = OCWebServices(
                ocConnectInfo, 
                ConfigDetails().proxyHost, 
                ConfigDetails().proxyPort,
                ConfigDetails().noProxy, 
                ConfigDetails().proxyAuthLogin, 
                ConfigDetails().proxyAuthPassword
            )
        else:
            ocWebServices = OCWebServices(ocConnectInfo)

        successfull = False
        try:
            successfull, studies = ocWebServices.listAllStudies()
        except:
            QtGui.QMessageBox.warning(self, "Error", "Cannot communicate with the server, no network connection or the server is not running.")

        if (successfull):
            OCUserDetails().username = username
            OCUserDetails().passwordHash = passwordHash
            OCUserDetails().connected = True

            UserDetails().username = username
            UserDetails().clearpass = password
            UserDetails().password = passwordHash

            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Wrong username or password.')
