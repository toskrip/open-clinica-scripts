#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# System
import sys

# PyQt
from PyQt4 import QtGui, QtCore, uic

# Resource images
from gui import images_rc

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ItemImportDialogUI(object):
    """
    """

    def setupUi(self, parent):
        """Prepare graphical user interface elements
        """
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Import item data")
        appIconPath =':/images/rpb-icon.jpg'
        appIcon = QtGui.QIcon()
        appIcon.addPixmap(QtGui.QPixmap(appIconPath));
        self.setWindowIcon(appIcon)
        self.resize(400, 400)

        # Dialog layout root
        rootLayout = QtGui.QVBoxLayout(self)

        # Instructions
        msg = "Provide a valid value for selected item:"
        lblInstructions = QtGui.QLabel(msg)

        rootLayout.addWidget(lblInstructions)
        rootLayout.addWidget(self.setupItem())
        rootLayout.addWidget(self.setupButtons())

    def setupItem(self):
        """Setup DICOM patient UI
        """
        # Patient Grid
        itemLayout = QtGui.QFormLayout()

        # Group
        itemGroup = QtGui.QGroupBox("CRF item: ")
        itemGroup.setLayout(itemLayout)

        self.txtItemName = QtGui.QLineEdit()
        self.txtItemName.setReadOnly(True)

        self.txtItemDescription = QtGui.QLineEdit()
        self.txtItemDescription.setReadOnly(True)

        self.textItemDataType = QtGui.QLineEdit()
        self.textItemDataType.setReadOnly(True)

        self.txtItemValueST = QtGui.QLineEdit()

        self.txtItemValueINT = QtGui.QLineEdit()
        self.txtItemValueINT.setValidator(QtGui.QIntValidator(self.txtItemValueINT))

        self.txtItemValueREAL = QtGui.QLineEdit()
        self.txtItemValueREAL.setValidator(QtGui.QDoubleValidator(self.txtItemValueREAL))

        self.txtItemValueDATE = QtGui.QLineEdit()

        # ComboBox
        # MultiSelect

        itemLayout.addRow("Item name:", self.txtItemName)
        itemLayout.addRow("Item description:", self.txtItemDescription)
        itemLayout.addRow("Item data type:", self.textItemDataType)

        itemLayout.addRow("String value:", self.txtItemValueST)
        itemLayout.addRow("Integer value:", self.txtItemValueINT)
        itemLayout.addRow("Real value:", self.txtItemValueREAL)
        itemLayout.addRow("Date value:", self.txtItemValueDATE)

        return itemGroup

    def setupButtons(self):
        """Setup dialog OK button
        """
        self.btnOk = QtGui.QPushButton("Ok")
        return self.btnOk
