import sys

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow


class StudySubjectTableModel(QtCore.QAbstractTableModel):

    def __init__(self, studySubjects = [], parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.__studySubjects = studySubjects

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return QtCore.QString("SS label")
                elif section == 1:
                    return QtCore.QString("Secondary label")
                elif section == 2:
                    return QtCore.QString("Enrollment date")
                elif section == 3:
                    return QtCore.QString("Subject identifier")
                elif section == 4:
                    return QtCore.QString("Subject gender")
            else:
                return QtCore.QString("%1").arg(section + 1)


    def rowCount(self, parent):
        if self.__studySubjects:
            return len(self.__studySubjects)
        else:
            return 0

    def columnCount(self, parent):
        if self.__studySubjects:
            return self.__studySubjects[0].atrSize() + self.__studySubjects[0].subject.atrSize()
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
            label = self.__studySubjects[row].label()
            return  "Open Clinica study subject with label: " + str(label)

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__studySubjects[row]

            if column == 0:
                return value.label()
            elif column == 1:
                return value.secondaryLabel()
            elif column == 2:
                return value.enrollmentDate
            elif column == 3:
                return value.subject.uniqueIdentifier
            elif column == 4:
                return value.subject.gender


    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable