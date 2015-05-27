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
        newIconRes = ':/images/new.png'
        reloadIconRes = ':/images/reload.png'
        saveIconRes = ':/images/save.png'
        detailsIconRes = ':/images/details.png'
        deleteIconRes = ':/images/delete.png'
        reloadIconRes = ':/images/reload.png'

        self.reloadIcon = QtGui.QIcon()
        self.reloadIcon.addPixmap(QtGui.QPixmap(reloadIconRes));

        self.newIcon = QtGui.QIcon()
        self.newIcon.addPixmap(QtGui.QPixmap(newIconRes))

        self.saveIcon = QtGui.QIcon()
        self.saveIcon.addPixmap(QtGui.QPixmap(saveIconRes))

        self.deleteIcon = QtGui.QIcon()
        self.deleteIcon.addPixmap(QtGui.QPixmap(deleteIconRes))

        self.detailsIcon = QtGui.QIcon()
        self.detailsIcon.addPixmap(QtGui.QPixmap(detailsIconRes))

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
        self.setupDicomStudies()

        tab4 = QtGui.QWidget()
        tab5 = QtGui.QWidget()

        # Add tabs to widget
        #self.tabWidget.addTab(tab4, "Study event CRFs")
        self.tabWidget.addTab(tab5, "Summary")

        # Create table views
        self.txtStudyEventCrfFilter = QtGui.QLineEdit()
        self.tvStudyEventCrfs = QtGui.QTableView()

        self.lblSummary = QtGui.QLabel("")
        self.textBrowserProgress = QtGui.QTextBrowser()
        self.textBrowserProgress.setObjectName(_fromUtf8("textBrowserProgress"))

        toolBarButtonSize = 20
        self.btnUpload = QtGui.QPushButton()
        uploadIconPath = ":/images/localDicomUpload.png"
        uploadIcon = QtGui.QIcon()
        uploadIcon.addPixmap(QtGui.QPixmap(uploadIconPath));
        self.btnUpload.setIcon(uploadIcon)
        self.btnUpload.setIconSize(QtCore.QSize(toolBarButtonSize, toolBarButtonSize))

        self.progressBar = QtGui.QProgressBar()

        # Behaviour for the table views
        self.tvStudyEventCrfs.setAlternatingRowColors(True)
        self.tvStudyEventCrfs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvStudyEventCrfs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        # Define layout for tab1 (as a child)

        layoutTab4 = QtGui.QVBoxLayout(tab4)
        layoutTab5 = QtGui.QVBoxLayout(tab5)

        # Add table view into the layour of tab1
        layoutTab4.addWidget(self.txtStudyEventCrfFilter)
        layoutTab4.addWidget(self.tvStudyEventCrfs)

        # Last step
        layoutTab5.addWidget(self.lblSummary)
        layoutTab5.addWidget(self.textBrowserProgress)
        layoutTab5.addWidget(self.progressBar)
        layoutTab5.addWidget(self.btnUpload)

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
        tabSubjects = QtGui.QWidget()

        self.tabWidget.addTab(tabSubjects, "Study subjects")

        self.txtStudySubjectFilter = QtGui.QLineEdit()
        self.tvStudySubjects = QtGui.QTableView()

        self.tvStudySubjects.setAlternatingRowColors(True)
        self.tvStudySubjects.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvStudySubjects.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tvStudySubjects.setSortingEnabled(True);

        layoutSubjects = QtGui.QVBoxLayout(tabSubjects)
        layoutSubjectsToolbar = QtGui.QGridLayout()

        txtFilter = QtGui.QLabel("Filter:")
        layoutSubjectsToolbar.addWidget(txtFilter, 1, 0)
        layoutSubjectsToolbar.addWidget(self.txtStudySubjectFilter, 1, 1)

        layoutSubjects.addLayout(layoutSubjectsToolbar)
        layoutSubjects.addWidget(self.tvStudySubjects)

    def setupEvents(self):
        """
        """
        tabEvents = QtGui.QWidget()

        self.tabWidget.addTab(tabEvents, "Study events")

        self.txtStudyEventFilter = QtGui.QLineEdit()
        self.txtStudyEventFilter.setDisabled(1)
        self.tvStudyEvents = QtGui.QTableView()

        self.tvStudyEvents.setAlternatingRowColors(True)
        self.tvStudyEvents.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvStudyEvents.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        #self.tvStudyEvents.setSortingEnabled(True);

        layoutEvents = QtGui.QVBoxLayout(tabEvents)
        layoutEventsToolbar = QtGui.QGridLayout()

        txtFilter = QtGui.QLabel("Filter:")
        layoutEventsToolbar.addWidget(txtFilter, 1, 0)
        layoutEventsToolbar.addWidget(self.txtStudyEventFilter, 1, 1)

        layoutEvents.addLayout(layoutEventsToolbar)
        layoutEvents.addWidget(self.tvStudyEvents)

    def setupDicomStudies(self):
        """
        """
        tabDicomStudies = QtGui.QWidget()

        self.tabWidget.addTab(tabDicomStudies, "DICOM")

        self.txtDicomStudiesFilter = QtGui.QLineEdit()
        self.tvDicomStudies = QtGui.QTableView()

        self.tvDicomStudies.setAlternatingRowColors(True)
        self.tvDicomStudies.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tvDicomStudies.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tvDicomStudies.setSortingEnabled(True);

        layoutDicomStudies = QtGui.QVBoxLayout(tabDicomStudies)
        layoutDicomStudiesToolbar = QtGui.QGridLayout()

        txtFilter = QtGui.QLabel("Filter:")

        layoutDicomStudiesToolbar.addWidget(txtFilter, 1, 0)
        layoutDicomStudiesToolbar.addWidget(self.txtDicomStudiesFilter, 1, 1)

        layoutDicomStudies.addLayout(layoutDicomStudiesToolbar)
        layoutDicomStudies.addWidget(self.tvDicomStudies)

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