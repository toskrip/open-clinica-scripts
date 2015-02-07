#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import sys

# PyQt
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow

class Node(object):
    """Domain object node representation in tree model
    """

    def __init__(self, name, parent=None, isChecked=False):
        """Default constructor
        """
        self._name = name
        self._isChecked = isChecked
        self._children= []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

########  ########   #######  ########  ######## ########  ######## #### ########  ######
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ##
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ##
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ##
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ######

    @property
    def name(self):
        """Name Getter
        """
        return self._name

    @name.setter
    def name(self, name):
        """Name Setter
        """
        self._name = name

    @property
    def isChecked(self):
        """Node isChecked Getter
        """
        return self._isChecked

    @isChecked.setter
    def isChecked(self, isChecked):
        """Node isChecked Setter
        """
        self._isChecked = isChecked

        #print("Running is checked on Node")

        # Distribute the option to all children
        if self._children is not None:
            for child in self._children:
                child._isChecked = isChecked

    @property
    def children(self):
        """Children Getter
        """
        return self._children

    @children.setter
    def children(self, children):
        """Children Setter
        """
        self._children = children

    @property
    def parent(self):
        """Parent Getter
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Parent Setter
        """
        self._parent = parent

##     ## ######## ######## ##     ##  #######  ########   ######
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ##
#### #### ##          ##    ##     ## ##     ## ##     ## ##
## ### ## ######      ##    ######### ##     ## ##     ##  ######
##     ## ##          ##    ##     ## ##     ## ##     ##       ##
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ##
##     ## ########    ##    ##     ##  #######  ########   ######

    def child(self, row):
        """Get one child according to row
        """
        return self._children[row]

    def addChild(self, child):
        """Add child node
        """
        if (child.parent is None):
            child.parent = self
        self._children.append(child)

    def childCount(self):
        """Number of children
        """
        return len(self._children)

    def childrenIsChecked(self):
        """Indicate whether the node has checked some of the children
        """
        if self._children is not None:
            for child in self._children:
                if child.isChecked:
                    return True
        return False

    def row(self):
        """Get index of this not relative to its parent
        """
        if self.parent is not None:
            return self._parent._children.index(self)

    def typeInfo(self):
        """Node type is overwriten in child classes
        """
        return "NODE"

    def log(self, tabLevel=-1):
        """Some testing long info
        """
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "in"

        output += "/--------" + self._name + "\n"

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1

        return output

    def __repr__(self):
        """Print object string representation
        """
        return self.log()