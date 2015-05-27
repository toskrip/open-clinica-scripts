import sys

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow


class ExportMappingTableModel(QtCore.QAbstractTableModel):

    def __init__(self, dataItems = [], parent = None):
        """
        """
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.dataItems = dataItems

    def headerData(self, section, orientation, role):
        """
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return QtCore.QString("Metadata name")
                elif section == 1:
                    return QtCore.QString("Format")
                elif section == 2:
                    return QtCore.QString("Data name")
                elif section == 3:
                    return QtCore.QString("Mandatory")
            else:
                return QtCore.QString("%1").arg(section + 1)


    def rowCount(self, parent):
        """
        """
        if self.dataItems:
            return len(self.dataItems)
        else:
            return 0

    def columnCount(self, parent):
        """
        """
        return 5


    def setData(self, index, value):
        column = index.column()

        if column == 1:
            self.dataItems[index.row()].data = str(value.toString())

        return True


    def data(self, index, role):
        """
        """
        #if role == QtCore.Qt.DecorationRole:
        #    row = index.row()
        #    value = self.__studies[row]
        #    pixmap = QtGui.QPixmap(26, 26)
        #    pixmap.fill(value)
        #    icon = QtGui.QIcon(pixmap)
        #    return icon

        # if role == QtCore.Qt.ToolTipRole:
        #     row = index.row()
        #     oid = self.__studyEventDefinitionCrfs[row].crf().oid()
        #     return  "Open Clinica study event definition CRF with oid: " + str(oid)

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()

            if column == 0:
                value = self.dataItems[row].metadata
                return value
            elif column == 1:
                value = self.dataItems[row].dataType
                return value
            elif column == 2:
                value = self.dataItems[row].data
                return value
            elif column == 3:
                return self.dataItems[row].mandatory


    def flags(self, index):
        """
        """
        column = index.column()
        # # Metadata item name and data type
        # if column == 0 or column == 1:
        #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        # # Data item name is editable
        # elif column == 2:
        #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        # # The rest
        # else:
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable