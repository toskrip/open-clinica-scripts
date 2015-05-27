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

# GUI Messages
import gui.messages

# Services
from rest.HttpConnectionService import HttpConnectionService
from soap.OCConnectInfo import OCConnectInfo
from soap.OCWebServices import OCWebServices
from odm.OdmFileDataService import OdmFileDataService

# Utils
from utils import first

# View Models
from viewModels.StudyEventDefinitionCrfTableModel import StudyEventDefinitionCrfTableModel
from viewModels.StudyEventDefinitionTableModel import StudyEventDefinitionTableModel
from viewModels.StudySubjectTableModel import StudySubjectTableModel
from viewModels.StudyTableModel import StudyTableModel

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
        self.logger = logging.getLogger(__name__)
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
        self.btnUpload.clicked.connect(self.btnUploadClicked)
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
        self.tvDicomStudies.setModel(None)
        self.textBrowserProgress.clear()

        # Set selected study and reload sites
        self._selectedStudy = first.first(
            study for study in self._studies if study.name().encode("utf-8") == text.toUtf8()
        )
        
        # Reload study sites
        self.reloadStudySites()

    def tblStudyItemChanged(self, current, previous):
        """Event handler which is triggered when selectedStudy change

        When the study is selected I have to clean all the other data elements
        Which depends on study. It means: StudySubjects, StudyEventDefinitions, StudyEventCRFs
        """
        # Clean the model before loading the new one
        self.tvStudySubjects.setModel(None)
        self.tvStudyEvents.setModel(None)
        self.tvDicomStudies.setModel(None)   
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

    def tblStudySubjectItemChanged(self, current, previous):
        """Event handler which is triggered when selectedStudySubject change
        """
        self.tvStudyEvents.setModel(None)
        self.tvDicomStudies.setModel(None)
        self.textBrowserProgress.clear()

        # Take the first column of selected row from table view
        index = self.studySubjectProxyModel.index(current.row(), 1);
        if index.data().toPyObject(): 
            self._selectedStudySubject = (
                first.first(
                    subject for subject in self._studySubjects if subject.label().encode("utf-8") == index.data().toPyObject().toUtf8()
                    )
                )

            # TODO: enable this when you migrate to a new version of OC
            # I need to load a SubjectKey
            # ssREST = self.svcHttp.getStudyCasebookSubject(
            #         ConfigDetails().ocHost, 
            #         self.getStudyOid(), 
            #         self._selectedStudySubject.label
            #     )
            # if ssREST != None:
            #     self._selectedStudySubject.oid = ssREST.oid
            #     self.logger.debug("Loaded subject key: " + self._selectedStudySubject.oid)

            # Load scheduled events for selected subject
            self.reloadEvents()
            
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
        self.reloadDicomFields()

    def tblDicomStudiesItemChanged(self, current, previous):
        """Event handler which is triggered whan Dicom Studies item change
        """
        self.textBrowserProgress.clear()

        # Take the fifth column (OID) of selected row from table view
        index = self.dicomFieldsProxyModel.index(current.row(), 5);
        if index.data().toPyObject():
            self._selectedCrfDicomField = first.first(field for field in self._crfDicomFields if field.oid.encode("utf-8") == index.data().toPyObject().toUtf8())

            # Get the appropriate DICOM patient CRF field depending on selected study
            for patientField in self._crfFieldsDicomPatientAnnotation:
                if (patientField.eventdefinitionoid == self._selectedCrfDicomField.eventOid and\
                    patientField.formoid == self._selectedCrfDicomField.formOid and\
                    patientField.groupoid == self._selectedCrfDicomField.groupOid):
                    self._selectedCrfDicomPatientField = patientField
                    break

            for reportField in self._crfFieldDicomReportAnnotation:
                if (reportField.eventdefinitionoid == self._selectedCrfDicomField.eventOid and\
                    reportField.formoid == self._selectedCrfDicomField.formOid and\
                    reportField.groupoid == self._selectedCrfDicomField.groupOid and\
                    reportField.crfitemoid.replace("SRTEXT","") in self._selectedCrfDicomField.oid):
                    self._selectedCrfSRTextField = reportField
                    break

            reportText = ""

            # Generate ODM XML for selection
            odm = self.fileMetaDataService.generateOdmXmlForStudy(
                        self.getStudyOid(),
                        self._selectedStudySubject,
                        self._selectedStudyEvent,
                        reportText,
                        self._selectedCrfDicomPatientField,
                        self._selectedCrfDicomField,
                        self._selectedCrfSRTextField
                    )

            self.logger.debug(odm)

            # Show the preliminary XML (wihtout DICOM study UID - will be generated)
            self.lblSummary.setText(odm)
            self.lblSummary.setWordWrap(True)

            # Show the selected upload target
            msg = "Selected upload target: "
            msg += self._selectedStudy.name() + "/"
            if len(self._selectedStudy.sites) > 0:
                msg += self._selectedStudySite.name + "/"
            msg += self._selectedStudySubject.label + " ["
            msg += self._selectedStudySubject.subject.uniqueIdentifier + "]" + "/"
            if self._selectedStudyEvent.isRepeating:
                msg += self._selectedStudyEvent.name + " [" + self._selectedStudyEvent.studyEventRepeatKey + "]/"
            else:
                msg += self._selectedStudyEvent.name + "/"
            msg += self._selectedCrfDicomField.label

            self.textBrowserProgress.append(msg)

    def btnUploadClicked(self):
        """Upload button pressed (DICOM upload workflow started)
        """
        QtGui.qApp.processEvents(QtCore.QEventLoop.AllEvents, 1000)

        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

        self.directory = self.selectFolderDialog()
        
        if self.directory is not None:
            # Make textBrowser visible
            self.textBrowserProgress.setVisible(True)
            self.textBrowserProgress.append('Wait please:')

            # Disable upload button for now but better is to desable whole UI
            self.btnUpload.setEnabled(False)

            # Start the workflow: analyse the type of DICOM
            #self.performDicomAnalysis()
            self.performDicomDataPreparation()

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
        self.logger.debug("Destroying module")
        for thread in self._threadPool:
            thread.terminate()
            thread.wait()
            self.logger.debug("Thread killed.")

    def getStudyOid(self):
        """Return study or site OID depending on mono/multi centre configuration
        """
        # Multicentre
        if len(self._selectedStudy.sites) > 0:
            return self._selectedStudySite.oid
        # Monocentre
        else:
            return self._selectedStudy.oid()

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
        self.fileMetaDataService = OdmFileDataService()

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

        # Selected sheduled studye event for subject
        self._selectedStudyEvent = None

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
        self._threadPool.append(WorkerThread(self.ocWebServices.listAllStudies))

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
        self._threadPool.append(WorkerThread(self.ocWebServices.getStudyMetadata, self._selectedStudy))

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
                studyNameValue = QtGui.QStandardItem(self._selectedStudy.name())

                self.studySitesModel.setItem(row, 0, siteIdentifierValue)
                self.studySitesModel.setItem(row, 1, siteNameValue)
                self.studySitesModel.setItem(row, 2, studyNameValue)

                row = row + 1
        else:
            studyIdentifierValue = QtGui.QStandardItem(self._selectedStudy.identifier())
            studyNameValue = QtGui.QStandardItem(self._selectedStudy.name())

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
            self._threadPool.append(WorkerThread(self.ocWebServices.listAllStudySubjectsByStudySite, [self._selectedStudy, self._selectedStudySite, self._studyMetadata]))
        else:
            self._threadPool.append(WorkerThread(self.ocWebServices.listAllStudySubjectsByStudy, [self._selectedStudy, self._studyMetadata]))

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
                        self.svcHttp.getStudyCasebookEvents, [ConfigDetails().ocHost, self.getStudyOid(), self._selectedStudySubject.oid]
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
        
    def reloadDicomFields(self):
        """Reload annotations for OpenClinica eCRF fields
        """
        # Setup loading UI
        self.window().statusBar.showMessage("Loading list of DICOM field values...")
        self.window().enableIndefiniteProgess()
        self.tabWidget.setEnabled(False)

        studyoid = self.getStudyOid()
        sspid = self._selectedStudySubject.subject.uniqueIdentifier
        eventDefOid = self._selectedStudyEvent.eventDefinitionOID
        studyEventRepeatKey = self._selectedStudyEvent.studyEventRepeatKey

        # Get annotation for selected event, which you want to retrieve values for
        annotations = []
        for crfAnnotation in self._crfFieldsAnnotation:
            if crfAnnotation.eventdefinitionoid == self._selectedStudyEvent.eventDefinitionOID:
                annotations.append(crfAnnotation)

        # Create data loading thread
        self._threadPool.append(WorkerThread(self.svcHttp.getCrfItemsValues, [studyoid, sspid, eventDefOid, studyEventRepeatKey, annotations]))

        # Connect slots
        self.connect(
            self._threadPool[len(self._threadPool) - 1],
            QtCore.SIGNAL("finished(QVariant)"),
            self.loadDicomFieldsFinished
        )

        # Start thread
        self._threadPool[len(self._threadPool) - 1].start()

    def selectFolderDialog(self):
        """User selects a directory with the DICOM study files
        """
        try:
            dirPath = QtGui.QFileDialog.getExistingDirectory(None, "Please select the folder with patient DICOM study files")
            if dirPath == "":
                return None

            isReadable = os.access(str(dirPath),  os.R_OK)
            QtGui.qApp.processEvents(QtCore.QEventLoop.AllEvents, 1000)
            
            if isReadable == False:
                self.Error("The client is not allowed to read data from the selected folder!")
                self.logger.error("No read access to selected folder.")
                return None
        except UnicodeEncodeError:
            self.Error("The path to the selected folder contains unsupported characters (unicode), please use only ascii characters in names of folders!")
            self.logger.error("Unsupported unicode folder path selected.")
            return None    

        return str(dirPath)

    def performDicomUpload(self):
        """Perform upload of anonymised DICOM data and import of DICOM Patient ID, and Study Intance UID into OpenClinica
        Called after agter annonymise is finished
        """
        self.textBrowserProgress.append("Importing anonymised information into eCRF...")

        self._selectedCrfDicomField.value = self.svcDicom.StudyUID
        reportText = self.svcDicom.getReportSerieText()

        # Generate ODM XML for selection
        odm = self.fileMetaDataService.\
            generateOdmXmlForStudy(\
                self.getStudyOid(),\
                self._selectedStudySubject,\
                self._selectedStudyEvent,\
                reportText,\
                self._selectedCrfDicomPatientField,\
                self._selectedCrfDicomField,\
                self._selectedCrfSRTextField)

        self.logger.debug(odm)

        # Show the preliminary XML (wihtout DICOM study UID - will be generated)
        self.lblSummary.setText(odm)
        self.lblSummary.setWordWrap(True)

        importSucessfull = self.ocWebServices.importODM(odm)
        if importSucessfull:
            self.textBrowserProgress.append("Import to OpenClinica sucessfull...")

            # Start uploading DICOM data
            # Create thread
            self._threadPool.append(WorkerThread(self.svcDicom.uploadDicomData, self.svcHttp))
            # Connect finish event
            self._threadPool[len(self._threadPool) - 1].finished.connect(self.DicomUploadFinishedMessage)
            # Connect message eventscd
            self.connect(
                self._threadPool[len(self._threadPool) - 1],
                QtCore.SIGNAL("message(QString)"),
                self.Message
            )
            self.connect(
                self._threadPool[len(self._threadPool) - 1],
                QtCore.SIGNAL("log(QString)"),
                self.LogMessage
            )
            # Progress
            self.connect(
                    self._threadPool[len(self._threadPool) - 1],
                    QtCore.SIGNAL("taskUpdated"),
                    self.handleTaskUpdated
            )
            # Start thread
            self._threadPool[len(self._threadPool) - 1].start()
        else:
            self.textBrowserProgress.append("Import Error. Cannot continue.")
            return

        return

    def loadStudiesFinished(self, studies):
        """Finished loading studies from server
        """
        self._studies = studies.toPyObject()
        self._studies .sort(cmp = lambda x, y: cmp(x.name(), y.name()))

        # And prepare ViewModel for the GUI
        studiesModel = QtGui.QStandardItemModel()
        for study in self._studies:
           text = QtGui.QStandardItem(study.name())
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
                if studySubject.secondaryLabel() != None:
                    secondaryLabelItem = QtGui.QStandardItem(studySubject.secondaryLabel())

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

            # Enhacne with information from REST
            statusItem = QtGui.QStandardItem()
            for e in eventsREST:
                if e.eventDefinitionOID == event.eventDefinitionOID and e.startDate.isoformat() == event.startDate.isoformat():
                    event.status = e.status
                    event.studyEventRepeatKey = e.studyEventRepeatKey
                    if event.isRepeating:
                        nameItem = QtGui.QStandardItem(event.name + " [" + event.studyEventRepeatKey + "]")
                    statusItem = QtGui.QStandardItem(event.status)
                    event.setForms(e.forms)
            
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

    def loadDicomFieldsFinished(self, crfFieldValues):
        """Finished loading DICOM field CRFs values from server
        """
        retrievedValue = crfFieldValues.toPyObject()

        # Get annotation for selected event
        row = 0
        dicomFieldsModel = QtGui.QStandardItemModel()
        dicomFieldsModel.setHorizontalHeaderLabels(["Label", "Description", "Data type", "Field value", "Annotation", "OID"])
        self._crfDicomFields = []

        for crfAnnotation in self._crfFieldsAnnotation:
            # Only annotation in event
            if crfAnnotation.eventdefinitionoid == self._selectedStudyEvent.eventDefinitionOID:
                # Only form (versions) which are scheduled (default versions are scheduled authomatically)
                if self._selectedStudyEvent.hasScheduledCrf(crfAnnotation.formoid):

                    value = str(retrievedValue[row])

                    field = CrfDicomField(crfAnnotation.crfitemoid, \
                        value,\
                        crfAnnotation.annotationtype.name,\
                        crfAnnotation.eventdefinitionoid,\
                        crfAnnotation.formoid,\
                        crfAnnotation.groupoid)

                    self._crfDicomFields.append(field)

                    i = self.fileMetaDataService.loadCrfItem(crfAnnotation.formoid, crfAnnotation.crfitemoid, self._studyMetadata)
                    if i is not None:
                        field.label = i.label
                        itemLabelValue = QtGui.QStandardItem(i.label)
                        itemDescriptionValue = QtGui.QStandardItem(i.description)
                        itemDataTypeValue = QtGui.QStandardItem(i.dataType)
                        itemValueValue = QtGui.QStandardItem(value)
                        itemAnnotationType = QtGui.QStandardItem(crfAnnotation.annotationtype.name)
                        itemCrfFieldOid = QtGui.QStandardItem(field.oid)

                        dicomFieldsModel.setItem(row, 0, itemLabelValue)
                        dicomFieldsModel.setItem(row, 1, itemDescriptionValue)
                        dicomFieldsModel.setItem(row, 2, itemDataTypeValue)
                        dicomFieldsModel.setItem(row, 3, itemValueValue)
                        dicomFieldsModel.setItem(row, 4, itemAnnotationType)
                        dicomFieldsModel.setItem(row, 5, itemCrfFieldOid)

                        row = row + 1

        # Create a proxy model to enable Sorting and filtering
        self.dicomFieldsProxyModel = QtGui.QSortFilterProxyModel()
        self.dicomFieldsProxyModel.setSourceModel(dicomFieldsModel)
        self.dicomFieldsProxyModel.setDynamicSortFilter(True)
        self.dicomFieldsProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        # Connect to filtering UI element
        QtCore.QObject.connect(self.txtDicomStudiesFilter, QtCore.SIGNAL("textChanged(QString)"), self.dicomFieldsProxyModel.setFilterRegExp)

        # Set model to View
        self.tvDicomStudies.setModel(self.dicomFieldsProxyModel)

        # Resize the width of columns to fit the content
        self.tvDicomStudies.resizeColumnsToContents()

        # After the view has model, set currentChanged behaviour
        self.tvDicomStudies.selectionModel().currentChanged.connect(self.tblDicomStudiesItemChanged)

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

    def DicomUploadFinishedMessage(self):
        """ Called after uploadDataThread finished, after the data were uploaded to
        the RadPlanBio server
        """
        # Enable upload button
        self.btnUpload.setEnabled(True)
        self.window().statusBar.showMessage("Ready")
