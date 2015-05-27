import sys

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow


class StudyTableModel(QtCore.QAbstractTableModel):

    def __init__(self, studies = [], parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.__studies = studies

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return QtCore.QString("Identifier")
                elif section == 1:
                    return QtCore.QString("OID")
                elif section == 2:
                    return QtCore.QString("Name")
            else:
                return QtCore.QString("%1").arg(section + 1)


    def rowCount(self, parent):
        if self.__studies:
            return len(self.__studies)
        else:
            return 0

    def columnCount(self, parent):
        if self.__studies:
            return self.__studies[0].atrSize()
        else:
            return 1

    def data(self, index, role):

        #if role == QtCore.Qt.DecorationRole:
        #    row = index.row()
        #    value = self.__studies[row]
        #    pixmap = QtGui.QPixmap(26, 26)
        #    pixmap.fill(value)
        #    icon = QtGui.QIcon(pixmap)
        #    return icon

        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            oid = self.__studies[row].oid()
            return  "Open Clinica study with Oid: " + str(oid)

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__studies[row]

            if column == 0:
                return value.identifier()
            elif column == 1:
                return value.oid()
            elif column == 2:
                return value.name()


    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable