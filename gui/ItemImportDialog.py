#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# System
import sys, os, shutil

# Logging
import logging
import logging.config

# Datetime
from datetime import datetime

# PyQt
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QMainWindow

# GUI
from gui.ItemImportDialogUI import ItemImportDialogUI

# Utils
from utils import first

########  ####    ###    ##        #######   ######
##     ##  ##    ## ##   ##       ##     ## ##    ##
##     ##  ##   ##   ##  ##       ##     ## ##
##     ##  ##  ##     ## ##       ##     ## ##   ####
##     ##  ##  ######### ##       ##     ## ##    ##
##     ##  ##  ##     ## ##       ##     ## ##    ##
########  #### ##     ## ########  #######   ######

class ItemImportDialog(QtGui.QDialog, ItemImportDialogUI):
    
    def __init__(self,  parent = None):
        """ Setup Ui, and load default names from file
        """
        # Setup UI
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(parent)

        # Setup logger - use config file
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

        self._item = None

        # Handlers
        self.connect(self.txtItemValueINT, QtCore.SIGNAL("textChanged(QString)"), self.intValueChanged)
        self.btnOk.clicked.connect(self.btnOkClicked)

########  ########   #######  ########  ######## ########  ######## #### ########  ######
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ##
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ##
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ##
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ######

    @property
    def item(self):
        """CRF item Getter
        """
        return self._item

##     ## ######## ######## ##     ##  #######  ########   ######
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ##
#### #### ##          ##    ##     ## ##     ## ##     ## ##
## ### ## ######      ##    ######### ##     ## ##     ##  ######
##     ## ##          ##    ##     ## ##     ## ##     ##       ##
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ##
##     ## ########    ##    ##     ##  #######  ########   ######

    def setModel(self, item):
        """Prepare view models for this dialog
        """
        self._item = item

        # View model for CRF item
        self.txtItemName.setText(item.name)
        self.txtItemDescription.setText(item.description)
        self.textItemDataType.setText(item.dataType)

        if item.dataType == "text":
            self.txtItemValueST.setDisabled(False)
            self.txtItemValueINT.setDisabled(True)
            self.txtItemValueREAL.setDisabled(True)
            self.txtItemValueDATE.setDisabled(True)
        elif item.dataType == "integer":
            self.txtItemValueST.setDisabled(True)
            self.txtItemValueINT.setDisabled(False)
            self.txtItemValueREAL.setDisabled(True)
            self.txtItemValueDATE.setDisabled(True)            

        # Selection changed
        #self.cmbStudyType.currentIndexChanged['QString'].connect(self.cmbStudyTypeChanged)
        

##     ##    ###    ##    ## ########  ##       ######## ########   ######
##     ##   ## ##   ###   ## ##     ## ##       ##       ##     ## ##    ##
##     ##  ##   ##  ####  ## ##     ## ##       ##       ##     ## ##
######### ##     ## ## ## ## ##     ## ##       ######   ########   ######
##     ## ######### ##  #### ##     ## ##       ##       ##   ##         ##
##     ## ##     ## ##   ### ##     ## ##       ##       ##    ##  ##    ##
##     ## ##     ## ##    ## ########  ######## ######## ##     ##  ######

    def cmbStudyTypeChanged(self, value):
        """On selected study type changed
        """
        self._study.studyType = value

    def intValueChanged(self, value):
        """
        """
        self._item.value = str(value)

    def btnOkClicked(self):
        """
        """
        self.accept()
