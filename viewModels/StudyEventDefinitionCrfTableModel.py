import sys

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow


class StudyEventDefinitionCrfTableModel(QtCore.QAbstractTableModel):

    def __init__(self, studyEventDefinitionCrfs = [], parent = None):

        QtCore.QAbstractItemModel.__init__(self, parent)
        self.__studyEventDefinitionCrfs = studyEventDefinitionCrfs

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return QtCore.QString("CRF OID")
                elif section == 1:
                    return QtCore.QString("CRF Name")
                elif section == 2:
                    return QtCore.QString("CRF version OID")
                elif section == 3:
                    return QtCore.QString("CRF version Name")
                elif section == 4:
                    return QtCore.QString("Required")
                elif section == 5:
                    return QtCore.QString("Double data entry")
                elif section == 6:
                    return QtCore.QString("Password required")
                elif section == 7:
                    return QtCore.QString("Hide CRF")
                elif section == 8:
                    return QtCore.QString("Source data verificaiton")
            else:
                return QtCore.QString("%1").arg(section + 1)


    def rowCount(self, parent):
        if self.__studyEventDefinitionCrfs:
            return len(self.__studyEventDefinitionCrfs)
        else:
            return 0

    def columnCount(self, parent):
        if self.__studyEventDefinitionCrfs:
            return self.__studyEventDefinitionCrfs[0].atrSize() + self.__studyEventDefinitionCrfs[0].crf().atrSize() + self.__studyEventDefinitionCrfs[0].defaultCrfVersion().atrSize()
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
            oid = self.__studyEventDefinitionCrfs[row].crf().oid()
            return  "Open Clinica study event definition CRF with oid: " + str(oid)

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__studyEventDefinitionCrfs[row]

            if column == 0:
                return value.crf().oid()
            elif column == 1:
                return value.crf().name()
            elif column == 2:
                return value.defaultCrfVersion().oid()
            elif column == 3:
                return value.defaultCrfVersion().oid()
            elif column == 4:
                return value.required()
            elif column == 5:
                return value.doubleDataEntry()
            elif column == 6:
                return value.passwordRequired()
            elif column == 7:
                return value.hideCrf()
            elif column == 8:
                return value.sourceDataVerificaiton()


    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable