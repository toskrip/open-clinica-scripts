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


class OcModuleUI(object):
    """Import Module UI definition
    """

    def setupUi(self, Module):
        """
        """
        #----------------------------------------------------------------------
        #--------------------------- Module -----------------------------------
        self.centralwidget = QtGui.QWidget(Module)
        self.centralwidget.setObjectName(_fromUtf8("ocModule"))
        self.rootLayout = QtGui.QVBoxLayout(self.parent)

        #----------------------------------------------------------------------
        #---------------------------- Icons -----------------------------------
        newIconRes = ":/images/new.png"
        reloadIconRes = ":/images/reload.png"
        saveIconRes = ":/images/save.png"
        detailsIconRes = ":/images/details.png"
        deleteIconRes = ":/images/delete.png"
        reloadIconRes = ":/images/reload.png"
        uploadIconPath = ":/images/localDicomUpload.png"

        self.reloadIcon = QtGui.QIcon()
        self.reloadIcon.addPixmap(QtGui.QPixmap(reloadIconRes))

        self.newIcon = QtGui.QIcon()
        self.newIcon.addPixmap(QtGui.QPixmap(newIconRes))

        self.saveIcon = QtGui.QIcon()
        self.saveIcon.addPixmap(QtGui.QPixmap(saveIconRes))

        self.deleteIcon = QtGui.QIcon()
        self.deleteIcon.addPixmap(QtGui.QPixmap(deleteIconRes))

        self.detailsIcon = QtGui.QIcon()
        self.detailsIcon.addPixmap(QtGui.QPixmap(detailsIconRes))

        self.uploadIcon = QtGui.QIcon()
        self.uploadIcon.addPixmap(QtGui.QPixmap(uploadIconPath))

        self.toolBarButtonSize = 20

        #----------------------------------------------------------------------
        #--------------------- Setup UI----------------------------------------

        self.setupOcConnectionBar()

        #--------------------------------------------------------------------
        # Main Tab Widget
        self.tabWidget = QtGui.QTabWidget()

        # Create tabs
        self.setupSites()
        self.setupSubjects()
        self.setupEvents()
        self.setupCrfs()
        self.setupItems()
        self.setupSummary()

        self.rootLayout.addWidget(self.tabWidget)
        
        #----------------------------------------------------------------------
        #---- Put defined central widget into ManWindow central widget --------
        self.retranslateUi(Module)
        QtCore.QMetaObject.connectSlotsByName(Module)

    def setupOcConnectionBar(self):
        # Connection info
        connectionLayout = QtGui.QGridLayout()
        connectionLayout.setSpacing(10)
        self.rootLayout.addLayout(connectionLayout)

        # OC connection SOAP web services
        ocSOAPConnection= QtGui.QLabel("OC connection:")
        self.lblOcConnection = QtGui.QLabel()

        # Add to connection layout
        connectionLayout.addWidget(ocSOAPConnection, 1, 0)
        connectionLayout.addWidget(self.lblOcConnection, 1, 1, 1, 8)

        # OC study
        study = QtGui.QLabel("Study: ")
        self.cmbStudy = QtGui.QComboBox()

        # Add to layout
        connectionLayout.addWidget(study, 2, 0)
        connectionLayout.addWidget(self.cmbStudy, 2, 1, 2, 8)

    def setupSites(self):
        """
        """
        tabStudySites = QtGui.QWidget()

        self.tabWidget.addTab(tabStudySites, "Study/Sites")

        self.txtStudyFilter = QtGui.QLineEdit()
        self.tvStudies = QtGui.QTableView()

        self.tvStudies.setAlternatingRowColors(True)
        self.tvStudies.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvStudies.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tvStudies.setSortingEnabled(True);

        layoutStudySites = QtGui.QVBoxLayout(tabStudySites)
        layoutStudySitesToolbar = QtGui.QGridLayout()

        txtFilter = QtGui.QLabel("Filter:")
        layoutStudySitesToolbar.addWidget(txtFilter, 1, 0)
        layoutStudySitesToolbar.addWidget(self.txtStudyFilter, 1, 1)

        layoutStudySites.addLayout(layoutStudySitesToolbar)
        layoutStudySites.addWidget(self.tvStudies)

    def setupSubjects(self):
        """
        """
        # Tab
        tabSubjects = QtGui.QWidget()
        self.tabWidget.addTab(tabSubjects, "Study subjects")

        # Toolbar with buttons
        self.btnReloadStudySubjects = QtGui.QPushButton()
        self.btnReloadStudySubjects.setIcon(self.reloadIcon)
        self.btnReloadStudySubjects.setToolTip("Reload study subjects")
        self.btnReloadStudySubjects.setIconSize(QtCore.QSize(self.toolBarButtonSize, self.toolBarButtonSize))

        self.btnNewStudySubject = QtGui.QPushButton()
        self.btnNewStudySubject.setIcon(self.newIcon)
        self.btnNewStudySubject.setToolTip("Create a new study subject")
        self.btnNewStudySubject.setIconSize(QtCore.QSize(self.toolBarButtonSize, self.toolBarButtonSize))
        
        subjectToolbar = QtGui.QHBoxLayout()
        subjectToolbar.addWidget(self.btnReloadStudySubjects)
        subjectToolbar.addWidget(self.btnNewStudySubject)
        subjectToolbar.addStretch(1)

        # Filter
        self.txtStudySubjectFilter = QtGui.QLineEdit()
        subjectFilterLayout = QtGui.QFormLayout()
        subjectFilterLayout.addRow("Filter:", self.txtStudySubjectFilter)

        # Data table
        self.tvStudySubjects = QtGui.QTableView()
        self.tvStudySubjects.setAlternatingRowColors(True)
        self.tvStudySubjects.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvStudySubjects.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tvStudySubjects.setSortingEnabled(True);
    
        # Layout
        layoutSubjects = QtGui.QVBoxLayout(tabSubjects)
        layoutSubjects.addLayout(subjectToolbar)
        layoutSubjects.addLayout(subjectFilterLayout)
        layoutSubjects.addWidget(self.tvStudySubjects)

    def setupEvents(self):
        """
        """
        tabEvents = QtGui.QWidget()
        self.tabWidget.addTab(tabEvents, "Study events")

        # Toolbar with buttons
        self.btnNewEvent = QtGui.QPushButton()
        self.btnNewEvent.setIcon(self.newIcon)
        self.btnNewEvent.setToolTip("Schedule a new study event")
        self.btnNewEvent.setIconSize(QtCore.QSize(self.toolBarButtonSize, self.toolBarButtonSize))
        
        eventToolbar = QtGui.QHBoxLayout()
        eventToolbar.addWidget(self.btnNewEvent)
        eventToolbar.addStretch(1) 

        # Filter
        self.txtStudyEventFilter = QtGui.QLineEdit()
        self.txtStudyEventFilter.setDisabled(1)
        eventFilterLayout = QtGui.QFormLayout()
        eventFilterLayout.addRow("Filter:", self.txtStudyEventFilter)

        # Data table
        self.tvStudyEvents = QtGui.QTableView()
        self.tvStudyEvents.setAlternatingRowColors(True)
        self.tvStudyEvents.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvStudyEvents.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        #self.tvStudyEvents.setSortingEnabled(True);

        layoutEvents = QtGui.QVBoxLayout(tabEvents)
        layoutEvents.addLayout(eventToolbar)
        layoutEvents.addLayout(eventFilterLayout)
        layoutEvents.addWidget(self.tvStudyEvents)

    def setupCrfs(self):
        """
        """
        tabCrfs = QtGui.QWidget()

        self.tabWidget.addTab(tabCrfs, "CRFs")

        self.txtCrfsFilter = QtGui.QLineEdit()
        self.tvCrfs = QtGui.QTableView()

        self.tvCrfs.setAlternatingRowColors(True)
        self.tvCrfs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvCrfs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tvCrfs.setSortingEnabled(True);

        layoutCrfs = QtGui.QVBoxLayout(tabCrfs)
        layoutCrfsToolbar = QtGui.QGridLayout()

        txtFilter = QtGui.QLabel("Filter:")

        layoutCrfsToolbar.addWidget(txtFilter, 1, 0)
        layoutCrfsToolbar.addWidget(self.txtCrfsFilter, 1, 1)

        layoutCrfs.addLayout(layoutCrfsToolbar)
        layoutCrfs.addWidget(self.tvCrfs)

    def setupItems(self):
        """
        """
        tabItems = QtGui.QWidget()

        self.tabWidget.addTab(tabItems, "Items")

        self.txtItemsFilter = QtGui.QLineEdit()
        self.tvItems = QtGui.QTableView()

        self.tvItems.setAlternatingRowColors(True)
        self.tvItems.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvItems.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tvItems.setSortingEnabled(True);

        layoutItems = QtGui.QVBoxLayout(tabItems)
        layoutItemsToolbar = QtGui.QGridLayout()

        txtFilter = QtGui.QLabel("Filter:")

        layoutItemsToolbar.addWidget(txtFilter, 1, 0)
        layoutItemsToolbar.addWidget(self.txtItemsFilter, 1, 1)

        layoutItems.addLayout(layoutItemsToolbar)
        layoutItems.addWidget(self.tvItems)

    def setupSummary(self):
        """
        """
        # Final step = overview
        tabSummary = QtGui.QWidget()

        # Add tabs to widget
        self.tabWidget.addTab(tabSummary, "Summary")

        self.lblSummary = QtGui.QLabel("")
        self.textBrowserProgress = QtGui.QTextBrowser()
        self.textBrowserProgress.setObjectName(_fromUtf8("textBrowserProgress"))

        self.btnUpload = QtGui.QPushButton()
        self.btnUpload.setIcon(self.uploadIcon)
        self.btnUpload.setIconSize(QtCore.QSize(self.toolBarButtonSize, self.toolBarButtonSize))

        self.progressBar = QtGui.QProgressBar()

        layoutSummary = QtGui.QVBoxLayout(tabSummary)

        # Last step
        layoutSummary.addWidget(self.lblSummary)
        layoutSummary.addWidget(self.textBrowserProgress)
        layoutSummary.addWidget(self.progressBar)
        layoutSummary.addWidget(self.btnUpload)

####    ##    #######  ##    ## 
 ##   ####   ##     ## ###   ## 
 ##     ##   ##     ## ####  ## 
 ##     ##    #######  ## ## ## 
 ##     ##   ##     ## ##  #### 
 ##     ##   ##     ## ##   ### 
####  ######  #######  ##    ##

    def retranslateUi(self, Module):
        """
        """
        self.btnUpload.setText(QtGui.QApplication.translate("MainWindow", "OC data", None, QtGui.QApplication.UnicodeUTF8))