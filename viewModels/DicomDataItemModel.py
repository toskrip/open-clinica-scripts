#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import sys

# GUI
import gui.colours

# PyQt
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow
  
class DicomDataItemModel(QtCore.QAbstractItemModel):
    """View model for DICOM hierarchy
    """

    def __init__(self, root, parent=None):
        """Default constructor
        """
        super(DicomDataItemModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        """Amount of children the item has
        """
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        """Number of section the header has
        """
        return 2

    def headerData(self, section, orientation, role):
        """Header data
        """
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "DICOM element"
            else:
                return "Type"

    def flags(self, index):
        """What is possible to do with data items
        """
        return  QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Display data
        """
        if not index.isValid():
            return None

        node = index.internalPointer()

        # Setup different colours for checked DICOM elements
        if role == QtCore.Qt.BackgroundRole:
            if node.isChecked:
                return QtGui.QBrush(QtGui.QColor(gui.colours.GREEN))
            elif node.childrenIsChecked():
                return QtGui.QBrush(QtGui.QColor(gui.colours.ORANGE))
            else:
                return QtGui.QBrush(QtGui.QColor(gui.colours.RED))

        # Node name
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return str(node.name)
            else:
                return node.typeInfo()

        # Icon according to node type
        # if role == QtCore.Qt.DecorationRole:
        #     if index.column() == 0:

        # Check option
        if role == QtCore.Qt.CheckStateRole:
            if index.column() == 0:
                if node.isChecked:
                    return QtCore.QVariant(QtCore.Qt.Checked)
                else:
                    return QtCore.QVariant(QtCore.Qt.Unchecked)

    def setData(self, index, value, role):
        """Set data, right now only the check box
        """
        if index.isValid():
            if role == QtCore.Qt.CheckStateRole:
                node = index.internalPointer()
                
                # True or False value according to checkbox
                newValue = value.toPyObject()
                node.isChecked = newValue
                
                # TODO: I have a strong feeling that one of these events is messing with selection performance
                # Apply the changes to whole hierarchy view
                self.emit(QtCore.SIGNAL("LayoutAboutToBeChanged()"))
                self.emit(QtCore.SIGNAL("LayoutChanged()"))
                self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(index), self.columnCount(index)))
                self.emit(QtCore.SIGNAL("DataChanged(QModelIndex,QModelIndex)"), self.createIndex(0, 0), self.createIndex(self.rowCount(index), self.columnCount(index)))

                return True

        return False

    def parent(self, index):
        """Return the parent of the node
        """
        node = self.getNode(index)
        parentNode = node.parent

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        else:
            if parentNode is not None:
                return self.createIndex(parentNode.row(), 0, parentNode)
            else:
                return QtCore.QModelIndex()

    def index(self, row, column, parent):
        """Return a child of a given row, column and parent
        """
        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):
        """Node according to index
        """
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode
