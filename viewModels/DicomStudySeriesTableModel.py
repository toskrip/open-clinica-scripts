#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import sys

#GUI
import gui.colours

# PyQt
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow

class DicomStudySeriesTableModel(QtCore.QAbstractTableModel):
    """View model for DICOM study serie list
    """

    def __init__(self, dataItems = [], parent = None):
        """Default constructor
        """
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.dataItems = dataItems

    def headerData(self, section, orientation, role):
        """Setup table header
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return QtCore.QString("Modality")
                elif section == 1:
                    return QtCore.QString("Original description")
                elif section == 2:
                    return QtCore.QString("New description")
                elif section == 3:
                    return QtCore.QString("UID")   
            else:
                return QtCore.QString("%1").arg(section + 1)

    def rowCount(self, parent):
        """Setup how many rows will be displayed
        """
        if self.dataItems:
            return len(self.dataItems)
        else:
            return 0

    def columnCount(self, parent):
        """Setup how many columns will be displayed
        """
        return 4

    def setData(self, index, value, role):
        """What to do when changes are made
        """
        if index.isValid():
            column = index.column()

            # Series new description is editable
            if column == 2:
                self.dataItems[index.row()].newDescription = str(value.toString().toUtf8()).decode("utf-8")

            return True
        return False

    def data(self, index, role):
        """Setup row data wich will be displayed
        """
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        # Setup different colours for originl and pseudonymised data
        if role == QtCore.Qt.BackgroundRole:
            if column == 0:
                return QtGui.QBrush(QtGui.QColor(gui.colours.GREEN))
            elif column == 1:
                return QtGui.QBrush(QtGui.QColor(gui.colours.RED))
            elif column == 2:
                return QtGui.QBrush(QtGui.QColor(gui.colours.GREEN))
            elif column == 3:
                return QtGui.QBrush(QtGui.QColor(gui.colours.RED))

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if column == 0:
                value = self.dataItems[row].modality
            elif column == 1:
                value = self.dataItems[row].description
            elif column == 2:
                value = self.dataItems[row].newDescription
            elif column == 3:
                value = str(self.dataItems[row].suid)

            return value

    def flags(self, index):
        """Setup flugs which determine what is possible to do with columns
        """
        row = index.row()
        column = index.column()

        # Series new description is editable
        if column == 2:
            # Editable only when original description is not empty
            if self.dataItems[row].description != "":
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
            else:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable