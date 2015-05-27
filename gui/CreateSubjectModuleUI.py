#----------------------------------------------------------------------
#------------------------------ Modules -------------------------------
# PyQt
import sys

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT


# Standard
# UTF 8
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

#----------------------------------------------------------------------

class CreateSubjectModuleUI(object):
    """Create Subject Module UI
    """

    #-------------------------------------------------------------------
    #-------------------- UI -------------------------------------------

    def setupUi(self, Module):
        """
        """
        #----------------------------------------------------------------------
        #--------------------------- Module -----------------------------------
        self.centralwidget = QtGui.QWidget(Module)
        self.centralwidget.setObjectName(_fromUtf8("createSubjectModule"))
        self.rootLayout = QtGui.QVBoxLayout(self.parent)
        #----------------------------------------------------------------------
        #---------------------------- Icons -----------------------------------
        newIconRes = ':/images/new.png'
        reloadIconRes = ':/images/reload.png'
        saveIconRes = ':/images/save.png'
        detailsIconRes = ':/images/details.png'
        deleteIconRes = ':/images/delete.png'

        self.newIcon = QtGui.QIcon()
        self.newIcon.addPixmap(QtGui.QPixmap(newIconRes))

        self.detailsIcon = QtGui.QIcon()
        self.detailsIcon.addPixmap(QtGui.QPixmap(detailsIconRes))

        self.reloadIcon = QtGui.QIcon()
        self.reloadIcon.addPixmap(QtGui.QPixmap(reloadIconRes));

        self.saveIcon = QtGui.QIcon()
        self.saveIcon.addPixmap(QtGui.QPixmap(saveIconRes))

        self.deleteIcon = QtGui.QIcon()
        self.deleteIcon.addPixmap(QtGui.QPixmap(deleteIconRes))
        #----------------------------------------------------------------------
        #----------------------- Module buttons toolbar -----------------------
        self.rootLayout.addLayout(self.__setupToolbarButtonsUI())

        #----------------------------------------------------------------------
        #-------------------------- Module ------------------------------------
        self.tabCreateSubjectModule = QtGui.QTabWidget()
        self.connect(self.tabCreateSubjectModule, SIGNAL('currentChanged(int)'), self.moduleTabChanged)

        # Create tabs
        tabStudies = QtGui.QWidget()
        tabSubjects = QtGui.QWidget()
        tabEvents = QtGui.QWidget()

        # Add tabs to widget
        self.tabCreateSubjectModule.addTab(tabStudies, "Study Sites")
        self.tabCreateSubjectModule.addTab(tabSubjects, "Subjects")
        self.tabCreateSubjectModule.addTab(tabEvents, "Events")

        self.tabCreateSubjectModule.setTabEnabled(1, False)
        self.tabCreateSubjectModule.setTabEnabled(2, False)

        # Define layout for tabs
        layoutStudies = QtGui.QVBoxLayout(tabStudies)
        layoutSubjects = QtGui.QVBoxLayout(tabSubjects)
        layoutEvents = QtGui.QVBoxLayout(tabEvents)

        self.rootLayout.addWidget(self.tabCreateSubjectModule)
        #----------------------------------------------------------------------
        #---------------------------  Data tab --------------------------------
        # Table View
        self.tvStudies = QtGui.QTableView()
        layoutStudies.addWidget(self.tvStudies)

        # Behaviour for the table views - select single row
        self.tvStudies.setAlternatingRowColors(True)
        self.tvStudies.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvStudies.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        self.tvSubjects = QtGui.QTableView()
        layoutSubjects.addWidget(self.tvSubjects)

        # Behaviour for the table views - select single row
        self.tvSubjects.setAlternatingRowColors(True)
        self.tvSubjects.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvSubjects.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        self.tvEvents = QtGui.QTableView()
        layoutEvents.addWidget(self.tvEvents)

        # Behaviour for the table views - select single row
        self.tvEvents.setAlternatingRowColors(True)
        self.tvEvents.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvEvents.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        #----------------------------------------------------------------------

        self.rootLayout.addLayout(self.__setupWizzardButtonsUI())

        #---------------------------------------------------------------------
        # Put defined central widget into ManWindow central widget
        self.retranslateUi(Module)
        QtCore.QMetaObject.connectSlotsByName(Module)


    def __setupToolbarButtonsUI(self):
        # Buttons toolbar
        toolbarButtonsSpace = 2
        toolbarButtonSize = 25

        toolbarGrid = QtGui.QHBoxLayout()

        self.btnReload = QtGui.QPushButton()
        self.btnReload.setIcon(self.reloadIcon)
        self.btnReload.setToolTip("reload")
        self.btnReload.setIconSize(QtCore.QSize(toolbarButtonSize, toolbarButtonSize))

        self.btnNew = QtGui.QPushButton()
        self.btnNew.setIcon(self.newIcon)
        self.btnNew.setToolTip("new")
        self.btnNew.setIconSize(QtCore.QSize(toolbarButtonSize, toolbarButtonSize))

        self.btnDetails = QtGui.QPushButton()
        self.btnDetails.setIcon(self.detailsIcon)
        self.btnDetails.setToolTip("edit details")
        self.btnDetails.setIconSize(QtCore.QSize(toolbarButtonSize, toolbarButtonSize))

        self.btnSave = QtGui.QPushButton()
        self.btnSave.setIcon(self.saveIcon)
        self.btnSave.setToolTip("save")
        self.btnSave.setIconSize(QtCore.QSize(toolbarButtonSize, toolbarButtonSize))

        self.btnDelete = QtGui.QPushButton()
        self.btnDelete.setIcon(self.deleteIcon)
        self.btnDelete.setToolTip("delete")
        self.btnDelete.setIconSize(QtCore.QSize(toolbarButtonSize, toolbarButtonSize))

        space = QtGui.QSpacerItem(1000, 0)

        toolbarGrid.addWidget(self.btnReload,)
        toolbarGrid.addWidget(self.btnNew,)
        toolbarGrid.addWidget(self.btnDetails)
        toolbarGrid.addWidget(self.btnSave)
        toolbarGrid.addWidget(self.btnDelete)

        # The rest of toolbar button row
        toolbarGrid.addItem(space)

        return toolbarGrid


    def __setupWizzardButtonsUI(self):
        """
        """
        buttonGrid = QtGui.QGridLayout()

        self.btnNext = QtGui.QPushButton()
        self.btnNext.setText("Next step")
        self.btnNext.setToolTip("next step")
        self.btnNext.clicked.connect(self.btnNextClicked)

        self.btnPrevious = QtGui.QPushButton()
        self.btnPrevious.setText("Previous step")
        self.btnPrevious.setToolTip("previous step")
        self.btnPrevious.setEnabled(False)
        self.btnPrevious.clicked.connect(self.btnPreviousClicked)

        self.btnFinish = QtGui.QPushButton()
        self.btnFinish.setText("Finish")
        self.btnFinish.setToolTip("finish")
        self.btnFinish.setVisible(False)

        buttonGrid.addWidget(self.btnPrevious, 0, 0)
        buttonGrid.addWidget(self.btnNext, 0, 1)
        buttonGrid.addWidget(self.btnFinish, 0, 1)

        return buttonGrid

    #-------------------------------------------------------------------
    #-------------------- Module Event Handlers ------------------------

    def moduleTabChanged(self, selectedIndex):
        """According to selected index of tab setup the toolbar buttons
        """
        self.setupToolBarButtons(selectedIndex)
        self.setupWizzardButtons(selectedIndex)
        self.loadModuleData(selectedIndex)


    def btnNextClicked(self):
        """
        """
        currentIndex = self.tabCreateSubjectModule.currentIndex()

        for i in range (0, self.tabCreateSubjectModule.count()):
            self.tabCreateSubjectModule.setTabEnabled(i, False)

        self.tabCreateSubjectModule.setTabEnabled(currentIndex + 1, True)
        self.tabCreateSubjectModule.setCurrentIndex(currentIndex + 1)


    def btnPreviousClicked(self):
        currentIndex = self.tabCreateSubjectModule.currentIndex()

        for i in range (0, self.tabCreateSubjectModule.count()):
            self.tabCreateSubjectModule.setTabEnabled(i, False)

        self.tabCreateSubjectModule.setTabEnabled(currentIndex - 1, True)
        self.tabCreateSubjectModule.setCurrentIndex(currentIndex - 1)

    #-------------------------------------------------------------------
    #------------------------ Button Commands --------------------------

    def setupToolBarButtons(self, selectedTabIndex):
        """
        """
        # Study sites
        if selectedTabIndex == 0:
            self.btnReload.setVisible(True)
            self.btnNew.setVisible(False)
            self.btnDetails.setVisible(False)
            self.btnSave.setVisible(False)
            self.btnDelete.setVisible(False)
        # Study subjects
        elif selectedTabIndex == 1:
            self.btnReload.setVisible(True)
            self.btnNew.setVisible(True)
            self.btnDetails.setVisible(False)
            self.btnSave.setVisible(False)
            self.btnDelete.setVisible(False)
        elif selectedTabIndex == 2:
            self.btnReload.setVisible(True)
            self.btnNew.setVisible(True)
            self.btnDetails.setVisible(False)
            self.btnSave.setVisible(False)
            self.btnDelete.setVisible(False)
        else:
            self.btnReload.setVisible(False)
            self.btnNew.setVisible(False)
            self.btnDetails.setVisible(False)
            self.btnSave.setVisible(False)
            self.btnDelete.setVisible(False)


    def setupWizzardButtons(self, selectedTabIndex):
        """When first tab, disable previous
        When last tab, make next text finish
        """
        # First tab
        if selectedTabIndex == 0:
            self.btnFinish.setVisible(False)
            self.btnPrevious.setEnabled(False)
            self.btnNext.setVisible(True)
        # Last tab
        elif selectedTabIndex == self.tabCreateSubjectModule.count() - 1:
            self.btnNext.setVisible(False)
            self.btnPrevious.setEnabled(True)
        else:
            self.btnFinish.setVisible(False)
            self.btnPrevious.setEnabled(True)
            self.btnNext.setVisible(True)

    #-------------------------------------------------------------------
    #-------------------- Internationalisation -------------------------

    def retranslateUi(self, Module):
        """
        """
        # Toolbar buttons
        self.btnNew.setText(QtGui.QApplication.translate("CreateSubjectModule", "new", None, QtGui.QApplication.UnicodeUTF8))
        self.btnReload.setText(QtGui.QApplication.translate("CreateSubjectModule", "reload", None, QtGui.QApplication.UnicodeUTF8))
