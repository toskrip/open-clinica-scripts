#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import sys, os, time

# Logging
import logging
import logging.config

# PyQt
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow, QWidget

# Contexts
from contexts.ConfigDetails import ConfigDetails
from contexts.OCUserDetails import OCUserDetails
from contexts.UserDetails import UserDetails

# Module UI
from gui.OcModuleUI import OcModuleUI
from gui.NewSubjectDialog import NewSubjectDialog
from gui.NewEventDialog import NewEventDialog
from gui.ItemImportDialog import ItemImportDialog

# Services
from rest.HttpConnectionService import HttpConnectionService
from soap.OCConnectInfo import OCConnectInfo
from soap.OCWebServices import OCWebServices
from odm.OdmFileDataService import OdmFileDataService

# Utils
from utils import first

# Workers
from workers.WorkerThread import WorkerThread

##     ##  #######  ########  ##     ## ##       ########
###   ### ##     ## ##     ## ##     ## ##       ##
#### #### ##     ## ##     ## ##     ## ##       ##
## ### ## ##     ## ##     ## ##     ## ##       ######
##     ## ##     ## ##     ## ##     ## ##       ##
##     ## ##     ## ##     ## ##     ## ##       ##
##     ##  #######  ########   #######  ######## ########

class OcModule(QWidget, OcModuleUI):
    """OC data module
    """

    def __init__(self, parent = None):
        """Default Constructor
        """
        # Setup GUI
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)

        # Hide summary of XML for importing data to OC (for user not necessary)
        self.lblSummary.hide()

        # Setup logger - use config file
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        # List of worker threads
        self._threadPool = []

        # Prepares services and main data for this ViewModel
        self.prepareServices()

        # Initialize data structures for UI
        self._studies = []
        self._studySubjects = []

        self.reloadData()

        # Finish UI setup
        self.lblOcConnection.setText("[" + OCUserDetails().username + "] " + ConfigDetails().ocHost)

        # Register handlers
        self.btnReloadStudySubjects.clicked.connect(self.btnReloadStudySubjectsClicked)
        self.btnNewStudySubject.clicked.connect(self.btnNewStudySubjectClicked)
        self.btnNewEvent.clicked.connect(self.btnNewEventClicked)
        self.btnUpload.clicked.connect(self.btnImportClicked)
        self.cmbStudy.currentIndexChanged["QString"].connect(self.cmbStudyChanged)
        self.destroyed.connect(self.handleDestroyed)

##     ##    ###    ##    ## ########  ##       ######## ########   ######
##     ##   ## ##   ###   ## ##     ## ##       ##       ##     ## ##    ##
##     ##  ##   ##  ####  ## ##     ## ##       ##       ##     ## ##
######### ##     ## ## ## ## ##     ## ##       ######   ########   ######
##     ## ######### ##  #### ##     ## ##       ##       ##   ##         ##
##     ## ##     ## ##   ### ##     ## ##       ##       ##    ##  ##    ##
##     ## ##     ## ##    ## ########  ######## ######## ##     ##  ######

    def cmbStudyChanged(self, text):
        """Executed when the concrete study is selected from studies combobox
        """
        # Reset table views
        self.tvStudies.setModel(None)
        self.tvStudySubjects.setModel(None)
        self.tvStudyEvents.setModel(None)
        self.tvCrfs.setModel(None)
        self.tvItems.setModel(None)
        self.textBrowserProgress.clear()

        # Set selected study and reload sites
        self._selectedStudy = first.first(
            study for study in self._studies if study.name.encode("utf-8") == text.toUtf8()
        )
    
        # Reload study sites
        if self._selectedStudy:
            self._logger.debug("Selected study: %s" % (self._selectedStudy.name))
            self.reloadStudySites()

    def tblStudyItemChanged(self, current, previous):
        """Event handler which is triggered when selectedStudy change

        When the study is selected I have to clean all the other data elements
        Which depends on study. It means: StudySubjects, StudyEventDefinitions, StudyEventCRFs
        """
        # Clean the model before loading the new one
        self.tvStudySubjects.setModel(None)
        self.tvStudyEvents.setModel(None)
        self.tvCrfs.setModel(None)
        self.tvItems.setModel(None)  
        self.textBrowserProgress.clear()  

        # Take the first column of selected row from table view
        index = self.studyProxyModel.index(current.row(), 0); 

        # Multicentric
        if len(self._selectedStudy.sites) > 0:
            self._selectedStudySite = first.first(
                studySite for studySite in self._selectedStudy.sites if studySite.identifier.encode("utf-8") == index.data().toPyObject().toUtf8()
            )

        # Get the study metadata
        self.reloadStudyMetadata()

    def btnReloadStudySubjectsClicked(self):
        """Reload study subjects button clicked
        """
        # Reload
        self.reloadSubjects()

    def btnNewStudySubjectClicked(self):
        """New study subject button clicked
        """
        if (self._selectedStudy):
            # Initialize dialog and bind data to UI
            dialog = NewSubjectDialog(self)
            dialog.setData(self._selectedStudy, self._selectedStudySite)

            # When ok commit session transaction
            if dialog.exec_() == QtGui.QDialog.Accepted:
                try:
                    newStudySubject = dialog.newStudySubject
                    self.ocWebServices.createStudySubject(
                        newStudySubject, 
                        self._selectedStudy
                    )
                except:
                    QtGui.QMessageBox.warning(self, "Error", "OC study subject not created.")

            # Reload
            self.reloadSubjects()

    def tblStudySubjectItemChanged(self, current, previous):
        """Event handler which is triggered when selectedStudySubject change
        """
        self.tvStudyEvents.setModel(None)
        self.tvCrfs.setModel(None)
        self.tvItems.setModel(None)
        self.textBrowserProgress.clear()

        # Take the second column (StudySubjectID) of selected row from table view
        column = 1
        index = self.studySubjectProxyModel.index(current.row(), column);
        print index.data().toPyObject()
        if index.data().toPyObject(): 
            self._selectedStudySubject = (
                first.first(
                    subject for subject in self._studySubjects if subject.label.encode("utf-8") == index.data().toPyObject().toUtf8()
                    )
                )

            if self._selectedStudySubject:

                # Load scheduled events for selected subject
                self.reloadEvents()

    def btnNewEventClicked(self):
        """Schedule new study event button clicked
        """
        events = self.ocWebServices.listAllStydyEventDefinitionsByStudy(
            self._selectedStudy
        )

        # Initialize dialog and bind data to UI
        dialog = NewEventDialog(self)
        dialog.setData(
            self._selectedStudy, 
            self._selectedStudySite,
            self._selectedStudySubject,
            events
        )

        # When ok commit session transaction
        if dialog.exec_() == QtGui.QDialog.Accepted:
                newEvent = dialog.selectedEvent

                self.ocWebServices.scheduleStudyEvent(
                    self._selectedStudy, 
                    self._selectedStudySubject, 
                    newEvent
                )

        # Reload
        temp = self._selectedStudySubject
        self.reloadSubjects()
        self._selectedStudySubject = temp
        #self.reloadEvents()
            
    def tblStudyEventItemChanged(self, current, previous):
        """Event handler which is triggered when selectedStudyEventDefintion change

        When the studyEvent is selected. Create a model for the event CRFs view.
        """
        self.textBrowserProgress.clear()
        # Selected studyEventDefinitions
        # Take the first column of selected row from table view
        #index = self.studyEventProxyModel.index(current.row(), 0); 
        #self._selectedStudyEvent = first.first(e for e in self._selectedStudySubject.events if e.name.encode("utf-8") == index.data().toPyObject().toUtf8())

        self._selectedStudyEvent = self._selectedStudySubject.events[current.row()]

        self.reloadCrfs()

    def tblEventCrfItemChanged(self, current, previous):
        """
        """
        self.tvItems.setModel(None)
        self.textBrowserProgress.clear()

        # Take the second column (OID) of selected row from table view
        column = 1
        index = self.crfProxyModel.index(current.row(), column);

        if index.data().toPyObject(): 
            self._selectedCrf = (
                first.first(
                    crf for crf in self._selectedStudyEvent.forms if crf.oid.encode("utf-8") == index.data().toPyObject().toUtf8()
                )
            )

        self.reloadItems()

    def tblCrfFieldItemChanged(self, current, previous):
        """
        """
        self.textBrowserProgress.clear()

        # Take the second column (OID) of selected row from table view
        column = 1
        index = self.itemProxyModel.index(current.row(), column);

        if index.data().toPyObject(): 
            self._selectedItem = (
                first.first(
                    i for i in self._selectedCrf.items if i.oid.encode("utf-8") == index.data().toPyObject().toUtf8()
                )
            )

            # Show the selected import target
            msg = "Selected import target: "
            msg += self._selectedStudy.name + "/"
            if len(self._selectedStudy.sites) > 0:
                msg += self._selectedStudySite.name + "/"
            msg += "StudySubjectID: " + self._selectedStudySubject.label + "/"
            if self._selectedStudyEvent.isRepeating:
                msg += self._selectedStudyEvent.name + " [" + self._selectedStudyEvent.studyEventRepeatKey + "]/"
            else:
                msg += self._selectedStudyEvent.name + "/"
            msg += self._selectedCrf.name + "/"
            msg += self._selectedItem.name 

            self._logger.debug(msg)

            self.textBrowserProgress.append(msg)

    def btnImportClicked(self):
        """Upload button pressed (DICOM upload workflow started)
        """
        QtGui.qApp.processEvents(QtCore.QEventLoop.AllEvents, 1000)

        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

        # Make textBrowser visible
        self.textBrowserProgress.setVisible(True)
        self.textBrowserProgress.append('Wait please:')

        # Disable upload button for now but better is to desable whole UI
        self.btnUpload.setEnabled(False)

        self.performDataImport()

    def handleTaskUpdated(self, data):
        """Move progress bar precento by precento
        """
        if type(data) is list:
            if data[0]:
                processed = data[0]
            if data[1]:
                size = data[1]

            progress = processed * 100 / size
            self.window().statusBar.showMessage("Processed files: [" + str(processed) + "/" + str(size) + "]")
            self.progressBar.setValue(progress)

    def handleDestroyed(self):
        """Kill runnign threads
        """
        self._logger.debug("Destroying module")
        for thread in self._threadPool:
            thread.terminate()
            thread.wait()
            self._logger.debug("Thread killed.")

    def getStudyOid(self):
        """Return study or site OID depending on mono/multi centre configuration
        """
        # Multicentre
        if len(self._selectedStudy.sites) > 0:
            return self._selectedStudySite.oid
        # Monocentre
        else:
            return self._selectedStudy.oid

 ######   #######  ##     ## ##     ##    ###    ##    ## ########   ######
##    ## ##     ## ###   ### ###   ###   ## ##   ###   ## ##     ## ##    ##
##       ##     ## #### #### #### ####  ##   ##  ####  ## ##     ## ##
##       ##     ## ## ### ## ## ### ## ##     ## ## ## ## ##     ##  ######
##       ##     ## ##     ## ##     ## ######### ##  #### ##     ##       ##
##    ## ##     ## ##     ## ##     ## ##     ## ##   ### ##     ## ##    ##
 ######   #######  ##     ## ##     ## ##     ## ##    ## ########   ######

    def prepareServices(self):
        """Prepare services for this module
        """
        # HTTP connection to RadPlanBio server (Database)
        self.svcHttp = HttpConnectionService(ConfigDetails().ocHost, ConfigDetails().ocPort, UserDetails())

        if ConfigDetails().proxyEnabled:
            self.svcHttp.setupProxy(ConfigDetails().proxyHost, ConfigDetails().proxyPort, ConfigDetails().noProxy)
        if ConfigDetails().proxyAuthEnabled:
            self.svcHttp.setupProxyAuth(ConfigDetails().proxyAuthLogin, ConfigDetails().proxyAuthPassword)

        # Create connection artefact to users main OpenClinica SOAP
        self.ocConnectInfo = OCConnectInfo(ConfigDetails().ocWsHost, OCUserDetails().username)
        self.ocConnectInfo.setPasswordHash(OCUserDetails().passwordHash)

        if ConfigDetails().proxyEnabled:
            self.ocWebServices = OCWebServices(self.ocConnectInfo, ConfigDetails().proxyHost, ConfigDetails().proxyPort, ConfigDetails().noProxy, ConfigDetails().proxyAuthLogin, ConfigDetails().proxyAuthPassword)
        else:
            self.ocWebServices = OCWebServices(self.ocConnectInfo)

        # ODM XML metadata processing
        self.svcOdm = OdmFileDataService()

    def reloadData(self):
        """Initialization of data for UI
        """
        # OpenClinica study
        del self._studies[:]
        self._studies = []
        self._selectedStudy = None
        self._studyMetadata = None

        # OpenClinica study site
        self._selectedStudySite = None

        # OpenClinica study subjects
        del self._studySubjects[:]
        self._studySubjects = []
        self._selectedStudySubject = None

        # Selected sheduled study event for subject
        self._selectedStudyEvent = None

        # Selected event CRF
        self._selectedCrf = None

        # Selected item
        self._selectedItem = None

        # Load studies
        self.reloadStudies()

    def reloadStudies(self):
        """Reload OpenClinica studies (in working thread)
        """
        # Setup loading UI
        self.window().statusBar.showMessage("Loading list of clinical studies...")
        self.window().enableIndefiniteProgess()
        self.tabWidget.setEnabled(False)

        # Create data loading thread
        self._threadPool.append(
            WorkerThread(self.ocWebServices.listAllStudies)
        )

        # Connect slots
        self.connect(
            self._threadPool[len(self._threadPool) - 1],
            QtCore.SIGNAL("finished(QVariant)"),
            self.loadStudiesFinished
        )

        # Start thread
        self._threadPool[len(self._threadPool) - 1].start()

    def reloadStudyMetadata(self):
        """Reload study metadata for selected study
        """
        # Setup loading UI
        self.window().statusBar.showMessage("Loading study metadata...")
        self.window().enableIndefiniteProgess()
        self.tabWidget.setEnabled(False)

        # Create data loading thread
        self._threadPool.append(
            WorkerThread(
                self.ocWebServices.getStudyMetadata, self._selectedStudy
            )
        )

        # Connect slots
        self.connect(
            self._threadPool[len(self._threadPool) - 1],
            QtCore.SIGNAL("finished(QVariant)"),
            self.loadStudyMetadataFinished
        )

        # Start thread
        self._threadPool[len(self._threadPool) - 1].start()

    def reloadStudySites(self):
        """Reload sites for selected OpenClinica sutdy (in memory processing)
        (If it is monocentric study show one default site)
        """
        # Quick way of crating simple viewModel
        self.studySitesModel = QtGui.QStandardItemModel()
        self.studySitesModel.setHorizontalHeaderLabels(["Identifier", "Partner Site", "Study"])

        row = 0
        if len(self._selectedStudy.sites) > 0:
            for site in self._selectedStudy.sites:
                siteIdentifierValue = QtGui.QStandardItem(site.identifier)
                siteNameValue = QtGui.QStandardItem(site.name)
                studyNameValue = QtGui.QStandardItem(self._selectedStudy.name)

                self.studySitesModel.setItem(row, 0, siteIdentifierValue)
                self.studySitesModel.setItem(row, 1, siteNameValue)
                self.studySitesModel.setItem(row, 2, studyNameValue)

                row = row + 1
        else:
            studyIdentifierValue = QtGui.QStandardItem(self._selectedStudy.identifier)
            studyNameValue = QtGui.QStandardItem(self._selectedStudy.name)

            self.studySitesModel.setItem(row, 0, studyIdentifierValue)
            self.studySitesModel.setItem(row, 2, studyNameValue)

            row = row + 1

        # Create a proxy model to enable Sorting and filtering
        self.studyProxyModel = QtGui.QSortFilterProxyModel()
        self.studyProxyModel.setSourceModel(self.studySitesModel)
        self.studyProxyModel.setDynamicSortFilter(True)
        self.studyProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        # Connect to filtering UI element
        QtCore.QObject.connect(self.txtStudyFilter, QtCore.SIGNAL("textChanged(QString)"), self.studyProxyModel.setFilterRegExp)

        self.tvStudies.setModel(self.studyProxyModel)
        self.tvStudies.resizeColumnsToContents()

        # After the view has model, set currentChanged behaviour
        self.tvStudies.selectionModel().currentChanged.connect(self.tblStudyItemChanged)

    def reloadSubjects(self):
        """Reload OpenClinica study subects enrolled into selected study/site in working thread
        """
        # Clear study subjects
        del self._studySubjects[:]
        self._studySubjects = []
        self._selectedStudySubject = None
        self._studySubjects = None
        self._subjectsREST = None

        # Setup loading UI
        self.window().statusBar.showMessage("Loading list of study subjects...")
        self.window().enableIndefiniteProgess()
        self.tabWidget.setEnabled(False)

        # Load subject for whole study or only site if it is multicentre study
        if self._selectedStudy and self._selectedStudy.isMulticentre:
            self._threadPool.append(
                WorkerThread(
                    self.ocWebServices.listAllStudySubjectsByStudySite, 
                    [self._selectedStudy, self._selectedStudySite, self._studyMetadata]
                )
            )
        else:
            self._threadPool.append(
                WorkerThread(
                    self.ocWebServices.listAllStudySubjectsByStudy,
                    [self._selectedStudy, self._studyMetadata]
                )
            )

        # Connect slots
        self.connect(
            self._threadPool[len(self._threadPool) - 1],
            QtCore.SIGNAL("finished(QVariant)"),
            self.loadSubjectsFinished
        )

        # Start thread
        self._threadPool[len(self._threadPool) - 1].start()

        # TODO: it would be much faster if I request REST subject only for the selected one
        # TODO: however we have to migrate to a new version of OC first
        # Need to get OIDs of subjects
        self._threadPool.append(
                WorkerThread(
                    self.svcHttp.getStudyCasebookSubjects, [ConfigDetails().ocHost, self.getStudyOid()]
                )
            )

        # Connect slots
        self.connect(
            self._threadPool[len(self._threadPool) - 1],
            QtCore.SIGNAL("finished(QVariant)"),
            self.loadSubjectsRESTFinished
        )

        # Start thread
        self._threadPool[len(self._threadPool) - 1].start()

    def reloadEvents(self):
        """Reload OpenClinica events scheduled for selected study subject
        """
        # Setup loading UI
        self.window().statusBar.showMessage("Loading subject scheduled events...")
        self.window().enableIndefiniteProgess()
        self.tabWidget.setEnabled(False)

        # Define a job
        # Need to get EventRepeatKeys
        self._threadPool.append(
                WorkerThread(
                        self.svcHttp.getStudyCasebookEvents, 
                        [ConfigDetails().ocHost, self.getStudyOid(), self._selectedStudySubject.oid]
                    )
            )

        # Connect slots
        self.connect(
            self._threadPool[len(self._threadPool) - 1],
            QtCore.SIGNAL("finished(QVariant)"),
            self.loadEventsFinished
        )

        # Start thread
        self._threadPool[len(self._threadPool) - 1].start()

    def reloadCrfs(self):
        """
        """
        self._selectedCrf = None

        # Setup loading UI
        self.window().statusBar.showMessage("Loading list of eCRFs...")
        self.window().enableIndefiniteProgess()
        self.tabWidget.setEnabled(False)

        # Quick way of crating simple viewModel
        self.crfsModel = QtGui.QStandardItemModel()
        self.crfsModel.setHorizontalHeaderLabels(["Name", "OID"])

        row = 0
        for crf in self._selectedStudyEvent.forms:
            nameItem = QtGui.QStandardItem(crf.name)
            oidItem = QtGui.QStandardItem(crf.oid)
           
            self.crfsModel.setItem(row, 0, nameItem)
            self.crfsModel.setItem(row, 1, oidItem)

            row = row + 1

        self.crfProxyModel = QtGui.QSortFilterProxyModel()
        self.crfProxyModel.setSourceModel(self.crfsModel)
        self.crfProxyModel.setDynamicSortFilter(True)
        self.crfProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        QtCore.QObject.connect(
            self.txtCrfsFilter, 
            QtCore.SIGNAL("textChanged(QString)"), 
            self.crfProxyModel.setFilterRegExp
        )

        self.tvCrfs.setModel(self.crfProxyModel)

        self.tvCrfs.resizeColumnsToContents()
        self.tvCrfs.selectionModel().currentChanged.connect(
            self.tblEventCrfItemChanged
        )

        # Update status bar
        self.tabWidget.setEnabled(True)
        self.window().statusBar.showMessage("Ready")
        self.window().disableIndefiniteProgess()

    def reloadItems(self):
        """
        """
        self._selectedItem = None

        # Setup loading UI
        self.window().statusBar.showMessage("Loading list of CRF items...")
        self.window().enableIndefiniteProgess()
        self.tabWidget.setEnabled(False)

        # Quick way of crating simple viewModel
        self.itemModel = QtGui.QStandardItemModel()
        self.itemModel.setHorizontalHeaderLabels(["Name", "OID", "DataType", "Description", "ItemGroupOID"])

        row = 0
        for item in self._selectedCrf.items:
            nameItem = QtGui.QStandardItem(item.name)
            oidItem = QtGui.QStandardItem(item.oid)
            dataTypeItem = QtGui.QStandardItem(item.dataType)
            descriptionItem = QtGui.QStandardItem(item.description)
            itemGroupOidItem = QtGui.QStandardItem(item.itemGroupOid)
           
            self.itemModel.setItem(row, 0, nameItem)
            self.itemModel.setItem(row, 1, oidItem)
            self.itemModel.setItem(row, 2, dataTypeItem)
            self.itemModel.setItem(row, 3, descriptionItem)
            self.itemModel.setItem(row, 4, itemGroupOidItem)

            row = row + 1

        self.itemProxyModel = QtGui.QSortFilterProxyModel()
        self.itemProxyModel.setSourceModel(self.itemModel)
        self.itemProxyModel.setDynamicSortFilter(True)
        self.itemProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        QtCore.QObject.connect(
            self.txtItemsFilter, 
            QtCore.SIGNAL("textChanged(QString)"), 
            self.itemProxyModel.setFilterRegExp
        )

        self.tvItems.setModel(self.itemProxyModel)

        self.tvItems.resizeColumnsToContents()
        self.tvItems.selectionModel().currentChanged.connect(
            self.tblCrfFieldItemChanged
        )

        # Update status bar
        self.tabWidget.setEnabled(True)
        self.window().statusBar.showMessage("Ready")
        self.window().disableIndefiniteProgess()

    def performDataImport(self):
        """Perform upload of anonymised DICOM data and import of DICOM Patient ID, and Study Intance UID into OpenClinica
        Called after agter annonymise is finished
        """
        self.textBrowserProgress.append("Importing data into eCRF...")

        # Dialog asking for value (depending on data type)
        itemImportDialog = ItemImportDialog()
        itemImportDialog.setModel(self._selectedItem)

        # Show dialog
        if itemImportDialog.exec_():
            # Mapping will be passed to DICOM service via worker parameters
            # Generate ODM XML for selection

            self._selectedItem.value = itemImportDialog.item.value
            
            odm = self.svcOdm.generateOdmXmlForStudyItem(
                    self.getStudyOid(),
                    self._selectedStudySubject,
                    self._selectedStudyEvent,
                    self._selectedCrf,
                    self._selectedItem
                )

            self._logger.debug(odm)

            importSucessfull = self.ocWebServices.importODM(odm)
            if importSucessfull:
                self.textBrowserProgress.append("Import to OpenClinica sucessfull...")
            else:
                self.textBrowserProgress.append("Import Error. Cannot continue.")

            self.tabWidget.setEnabled(True)
            self.window().statusBar.showMessage("Ready")
            self.window().disableIndefiniteProgess()
            self.Message("Import finished.")
        else:
            self.tabWidget.setEnabled(True)
            self.window().statusBar.showMessage("Ready")
            self.window().disableIndefiniteProgess()

        self.btnUpload.setDisabled(False)

        return

    def loadStudiesFinished(self, studies):
        """Finished loading studies from server
        """
        self._studies = studies.toPyObject()
        self._studies .sort(cmp = lambda x, y: cmp(x.name(), y.name()))

        # And prepare ViewModel for the GUI
        studiesModel = QtGui.QStandardItemModel()
        for study in self._studies:
           text = QtGui.QStandardItem(study.name)
           studiesModel.appendRow([text])
        self.cmbStudy.setModel(studiesModel)

        # Select the first study
        self._selectedStudy = self._studies[0]

        # Update status bar
        self.tabWidget.setEnabled(True)
        self.window().statusBar.showMessage("Ready")
        self.window().disableIndefiniteProgess()

    def loadStudyMetadataFinished(self, metadata):
        """Finished loading metadata from server
        """
        self._studyMetadata = metadata.toPyObject()

        # Update status bar
        self.tabWidget.setEnabled(False)
        self.window().statusBar.showMessage("Ready")
        self.window().disableIndefiniteProgess()

        # Reload study subjects with scheduled events (extedn them with metadata)
        self.reloadSubjects()

    def loadSubjectsFinished(self, subjects):
        """Finished loading of SOAP subject data
        """
        self._studySubjects = subjects.toPyObject()
        self.syncSubjectAndRESTSubjects()

    def loadSubjectsRESTFinished(self, subjects):
        """Finished loading of REST subject data
        """         
        self._subjectsREST = subjects.toPyObject()
        self.syncSubjectAndRESTSubjects()

    def syncSubjectAndRESTSubjects(self):
        """Syncrhonize results from SOAP and REST subject loading
        """
        # In case the REST worker finished sooner than the SOAP worker
        if self._studySubjects != None and self._subjectsREST != None:

            # Create the ViewModels for Views
            self.subjectsModel = QtGui.QStandardItemModel()
            self.subjectsModel.setHorizontalHeaderLabels(["PersonID", "StudySubjectID", "SecondaryID", "Gender", "Enrollment date", "OID"])

            row = 0
            for studySubject in self._studySubjects:
                # Always mandatory
                labelItem = QtGui.QStandardItem(studySubject.label)
                enrollmentDateItem = QtGui.QStandardItem(studySubject.enrollmentDate)

                # Optional
                secondaryLabelItem = QtGui.QStandardItem("")
                if studySubject.secondaryLabel != None:
                    secondaryLabelItem = QtGui.QStandardItem(studySubject.secondaryLabel)

                # Not everything has to be collected (depend on study setup)
                pidItem = QtGui.QStandardItem("")
                genderItem = QtGui.QStandardItem("")
                if studySubject.subject != None:
                    if studySubject.subject.uniqueIdentifier != None:
                        pidItem = QtGui.QStandardItem(studySubject.subject.uniqueIdentifier)
                    if studySubject.subject.gender != None:
                        genderItem = QtGui.QStandardItem(studySubject.subject.gender)

                oidItem = QtGui.QStandardItem("")
                for sREST in self._subjectsREST:
                    if sREST.studySubjectId == studySubject.label:
                        oidItem = QtGui.QStandardItem(sREST.oid)
                        studySubject.oid = sREST.oid

                self.subjectsModel.setItem(row, 0, pidItem)
                self.subjectsModel.setItem(row, 1, labelItem)
                self.subjectsModel.setItem(row, 2, secondaryLabelItem)
                self.subjectsModel.setItem(row, 3, genderItem)
                self.subjectsModel.setItem(row, 4, enrollmentDateItem)
                self.subjectsModel.setItem(row, 5, oidItem)

                row = row + 1

            # Create a proxy model to enable Sorting and filtering
            self.studySubjectProxyModel = QtGui.QSortFilterProxyModel()
            self.studySubjectProxyModel.setSourceModel(self.subjectsModel)
            self.studySubjectProxyModel.setDynamicSortFilter(True)
            self.studySubjectProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

            # Connect to filtering UI element
            QtCore.QObject.connect(self.txtStudySubjectFilter, QtCore.SIGNAL("textChanged(QString)"), self.studySubjectProxyModel.setFilterRegExp)

            # Set the models Views
            self.tvStudySubjects.setModel(self.studySubjectProxyModel)

            # Resize the width of columns to fit the content
            self.tvStudySubjects.resizeColumnsToContents()

            # After the view has model, set currentChanged behaviour
            self.tvStudySubjects.selectionModel().currentChanged.connect(self.tblStudySubjectItemChanged)

            self.tabWidget.setEnabled(True)
            self.window().statusBar.showMessage("Ready")
            self.window().disableIndefiniteProgess()

    def loadEventsFinished(self, events):
        """Finished loading events data
        """
        eventsREST = events.toPyObject()

        # Quick way of crating simple viewModel
        self.eventsModel = QtGui.QStandardItemModel()
        self.eventsModel.setHorizontalHeaderLabels(["Name", "Description", "Category", "Type", "Repeating", "Start date", "Status"])

        row = 0
        for event in self._selectedStudySubject.events:
            nameItem = QtGui.QStandardItem(event.name)
            descriptionItem = QtGui.QStandardItem(event.description)
            categoryItem = QtGui.QStandardItem(event.category) 
            typeItem = QtGui.QStandardItem(event.eventType)
            isRepeatingItem = QtGui.QStandardItem(str(event.isRepeating))
            startDateItem = QtGui.QStandardItem("{:%d-%m-%Y}".format(event.startDate))

            # Enhance with information from REST
            statusItem = QtGui.QStandardItem()
            for e in eventsREST:
                if e.eventDefinitionOID == event.eventDefinitionOID and e.startDate.isoformat() == event.startDate.isoformat():
                    event.status = e.status
                    event.studyEventRepeatKey = e.studyEventRepeatKey
                    if event.isRepeating:
                        nameItem = QtGui.QStandardItem(event.name + " [" + event.studyEventRepeatKey + "]")
                    statusItem = QtGui.QStandardItem(event.status)
                    event.forms = e.forms
            
            self.eventsModel.setItem(row, 0, nameItem)
            self.eventsModel.setItem(row, 1, descriptionItem)
            self.eventsModel.setItem(row, 2, categoryItem)
            self.eventsModel.setItem(row, 3, typeItem)
            self.eventsModel.setItem(row, 4, isRepeatingItem)
            self.eventsModel.setItem(row, 5, startDateItem)
            self.eventsModel.setItem(row, 6, statusItem)

            row = row + 1

        self.studyEventProxyModel = QtGui.QSortFilterProxyModel()
        self.studyEventProxyModel.setSourceModel(self.eventsModel)
        self.studyEventProxyModel.setDynamicSortFilter(True)
        self.studyEventProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        QtCore.QObject.connect(self.txtStudyEventFilter, QtCore.SIGNAL("textChanged(QString)"), self.studyEventProxyModel.setFilterRegExp)

        self.tvStudyEvents.setModel(self.studyEventProxyModel)

        self.tvStudyEvents.resizeColumnsToContents()
        self.tvStudyEvents.selectionModel().currentChanged.connect(self.tblStudyEventItemChanged)

        # Update status bar
        self.tabWidget.setEnabled(True)
        self.window().statusBar.showMessage("Ready")
        self.window().disableIndefiniteProgess()

##     ## ########  ######   ######     ###     ######   ########  ######
###   ### ##       ##    ## ##    ##   ## ##   ##    ##  ##       ##    ##
#### #### ##       ##       ##        ##   ##  ##        ##       ##
## ### ## ######    ######   ######  ##     ## ##   #### ######    ######
##     ## ##             ##       ## ######### ##    ##  ##             ##
##     ## ##       ##    ## ##    ## ##     ## ##    ##  ##       ##    ##
##     ## ########  ######   ######  ##     ##  ######   ########  ######

    def Question(self, string):
        """Question message box
        """
        reply = QtGui.QMessageBox.question(self, "Question", string, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.btnUpload.setEnabled(False)
        else:
            self.btnUpload.setEnabled(True)

    def Error(self, string):
        """Error message box
        """
        QtGui.QMessageBox.critical(self, "Error", string)
        self.btnUpload.setEnabled(True)

    def Warning(self, string):
        """Warning message box
        """
        QtGui.QMessageBox.warning(self, "Warning", string)
        self.btnUpload.setEnabled(True)

    def Message(self, string):
        """Called from message event, opens a small window with the message
        """
        QtGui.QMessageBox.about(self, "Info", string)
        self.btnUpload.setEnabled(True)

    def LogMessage(self, string):
        """Called from log event in thread and adds log into textbrowser UI
        """
        self.textBrowserProgress.append(string)
