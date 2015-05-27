#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import sys, platform, os

# PyQt
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import Qt

# Contexts
from contexts.ConfigDetails import ConfigDetails

########  ####    ###    ##        #######   ######
##     ##  ##    ## ##   ##       ##     ## ##    ##
##     ##  ##   ##   ##  ##       ##     ## ##
##     ##  ##  ##     ## ##       ##     ## ##   ####
##     ##  ##  ######### ##       ##     ## ##    ##
##     ##  ##  ##     ## ##       ##     ## ##    ##
########  #### ##     ## ########  #######   ######

class AboutDialog(QtGui.QDialog):
    """About Dialog Class
    """

    def __init__(self, parent=None):
        """Default Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("About")

        size = 100
        lblIcon = QtGui.QLabel()
        appIconPath =":/images/rpb-icon.jpg"
        myPixmap = QtGui.QPixmap(appIconPath)
        myScaledPixmap = myPixmap.scaled(size, size, Qt.KeepAspectRatio)
        lblIcon.setPixmap(myScaledPixmap)

        copyright = u"\u00A9"

        # Dialog layout root
        rootLayout = QtGui.QVBoxLayout(self)

        # About Text
        lblAppName = QtGui.QLabel(ConfigDetails().name)
        lblAppVersion = QtGui.QLabel("version: " + ConfigDetails().version)
        lblPlatform = QtGui.QLabel("system: " + platform.system())
        lblLogFile = QtGui.QLabel("log: " + ConfigDetails().logFilePath)
        lblEmptyLine = QtGui.QLabel("")
        lblAppCopyright = QtGui.QLabel(copyright + ConfigDetails().copyright)

        # Layouting
        rootLayout.addWidget(lblIcon)
        rootLayout.addWidget(lblAppName)
        rootLayout.addWidget(lblAppVersion)
        rootLayout.addWidget(lblPlatform)
        rootLayout.addWidget(lblLogFile)
        rootLayout.addWidget(lblEmptyLine)
        rootLayout.addWidget(lblAppCopyright)
