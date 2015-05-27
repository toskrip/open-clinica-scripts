import sys

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow


class StudyEventDefinitionTableModel(QtCore.QAbstractTableModel):

    def __init__(self, studyEventDefinitions = [], parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.__studyEventDefinitions= studyEventDefinitions

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return QtCore.QString("OID")
                elif section == 1:
                    return QtCore.QString("Name")
            else:
                return QtCore.QString("%1").arg(section + 1)


    def rowCount(self, parent):
        if self.__studyEventDefinitions:
            return len(self.__studyEventDefinitions)
        else:
            return 0

    def columnCount(self, parent):
        if self.__studyEventDefinitions:
            return self.__studyEventDefinitions[0].atrSize()
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
            oid = self.__studyEventDefinitions[row].oid()
            return  "Open Clinica study event definition with oid: " + str(oid)

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__studyEventDefinitions[row]

            if column == 0:
                return value.oid()
            elif column == 1:
                return value.name()


    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable