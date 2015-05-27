#----------------------------------------------------------------------
#------------------------------ Modules -------------------------------
# PyQt
import logging
import logging.config
import sys, os, shutil, time, datetime

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QMainWindow, QWidget

from OCUserDetails import OCUserDetails
from UserDetails import UserDetails
from gui.CreateSubjectModuleUI import CreateSubjectModuleUI
from gui.NewEventDialog import NewEventDialog
from gui.NewSubjectDialog import NewSubjectDialog
from services.AppConfigurationService import AppConfigurationService
from services.HttpConnectionService import HttpConnectionService
from services.MainzellisteConnectInfo import MainzellisteConnectInfo
from services.OCConnectInfo import OCConnectInfo
from services.OCWebServices import OCWebServices
from services.PseudonymisationService import PseudonymisationService
from utils import first


# Standard
# Logging
# Utils
# GUI
# Database Model
# Services
#----------------------------------------------------------------------
class CreateSubjectModule(QWidget, CreateSubjectModuleUI):
    """PullDataRequest Module view class
    """

    #----------------------------------------------------------------------
    #--------------------------- Constructors -----------------------------

    def __init__(self, parent = None):
        """Constructor of ExportModule View
        """
        QWidget.__init__(self, parent)
        self.parent = parent

        #-----------------------------------------------------------------------
        #----------------------- Logger ----------------------------------------
        self.logger = logging.getLogger(__name__)
        logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
        #-----------------------------------------------------------------------
        #---------------------- App config --------------------------------------
        self.appConfig = AppConfigurationService()
        #-----------------------------------------------------------------------
        #--------------------- Create Module UI --------------------------------
        self.setupUi(self)
        #-----------------------------------------------------------------------
        #----------------------- Services --------------------------------------
        # There are two http services, one for communicating with my own
        # site server/database
        section = "RadPlanBioServer"
        hostname = self.appConfig.get(section)["host"]
        port = self.appConfig.get(section)["port"]
        self.svcHttp = HttpConnectionService(hostname, port, UserDetails())

        #TODO: SiteName according to user account
        self.mySite = self.svcHttp.getPartnerSiteByName("DKTK-DRESDEN")
        baseUrl = self.mySite.edc.soapbaseurl

        # Create connection artefact to OC
        self.ocConnectInfo = OCConnectInfo(baseUrl, OCUserDetails().username)
        self.ocConnectInfo.setPassword(OCUserDetails().password)
        self.ocWebServices = OCWebServices(self.ocConnectInfo)

        # Create REST mainzellieste
        userName = self.mySite.pidg.adminusername
        password = self.mySite.pidg.adminpassword
        baseUrl =  self.mySite.pidg.generatorbaseurl
        apiKey = self.mySite.pidg.apikey

        connectInfo = MainzellisteConnectInfo(baseUrl, userName, password, apiKey)
        self.svcPseudonymisation = PseudonymisationService(connectInfo)
        #-----------------------------------------------------------------------
        #----------------------- On Create -------------------------------------
        self.reloadSites()
        #-----------------------------------------------------------------------
        #---------- Load modules buttons - events definitions ------------------
        self.btnNew.clicked.connect(self.btnNewClicked)
        self.btnReload.clicked.connect(self.btnReloadClicked)
        self.tvStudies.selectionModel().currentChanged.connect(self.tvStudyChanged)

    #----------------------------------------------------------------------
    #------------------- Module buttons Handlers --------------------------

    def btnNewClicked(self):
        """
        """
        index = self.tabCreateSubjectModule.currentIndex()

        if index == 1:
            # Initialize dialog and bind data to UI
            dialog = NewSubjectDialog(self)
            dialog.svcPseudonymisation = self.svcPseudonymisation
            dialog.setData(self.selectedStudy, self.selectedStudySite)

            # Show dialog
            dialogResult = dialog.exec_()

            # When ok commit session transaction
            if dialogResult == QtGui.QDialog.Accepted:
                try:
                    newStudySubject = dialog.newStudySubject
                    self.ocWebServices.createStudySubject(newStudySubject, self.selectedStudy, self.selectedStudySite)
                except:
                    QtGui.QMessageBox.warning(self, 'Error', 'OC study subject not created.')

            # Reload
            index = self.tabCreateSubjectModule.currentIndex()
            self.loadModuleData(index)
        elif index == 2:
            studyEvents = self.ocWebServices.listAllStydyEventDefinitionsByStudy(self.selectedStudy)

            dialog = NewEventDialog(self)
            dialog.setData(self.selectedStudy, self.selectedStudySite, self.selectedSubject, studyEvents)

            # Show dialog
            dialogResult = dialog.exec_()

            # When ok commit session transaction
            if dialogResult == QtGui.QDialog.Accepted:
                #try:
                unsheduledEvent = dialog.selectedEvent
                self.ocWebServices.scheduleStudyEvent(self.selectedStudy, self.selectedStudySite, self.selectedSubject, unsheduledEvent)
                #except:
                #    QtGui.QMessageBox.warning(self, 'Error', 'OC study event was not sheduled.')

            # Reload
            index = self.tabCreateSubjectModule.currentIndex()
            self.loadModuleData(index)


    def btnReloadClicked(self):
        """
        """
        index = self.tabCreateSubjectModule.currentIndex()
        self.loadModuleData(index)

    #----------------------------------------------------------------------
    #------------------- TableView Handlers -------------------------------

    def tvStudyChanged(self, current, previous):
        self.tvSubjects.setModel(None)

        index = current.row()

        self.selectedStudy = None
        self.selectedStudySite = None

        counter = 0
        found = False
        for study in self.studies:
            for site in study.sites:
                if counter == index:
                    self.selectedStudy = study
                    self.selectedStudySite = site
                    found = True
                    break
                else:
                    counter = counter + 1

            if found:
                break

        if found:
            self.reloadSubjects()


    def tvSubjectChanged(self, current, previous):
        index = current.row()

        self.selectedSubject = self.subjects[index]

        self.reloadEvents()


    def tvEventsChanged(self, current, previous):
        index = current.row()

        self.selectedEvent = self.events[index]


    #----------------------------------------------------------------------
    #------------------------ Module commands -----------------------------

    def loadModuleData(self, selectedIndex):
        if selectedIndex == 0:
            self.reloadSites()
            self.tvStudies.selectionModel().currentChanged.connect(self.tvStudyChanged)
        elif selectedIndex == 1:
            self.reloadSubjects()
            self.tvSubjects.selectionModel().currentChanged.connect(self.tvSubjectChanged)
        elif selectedIndex == 2:
            self.reloadSubjects()
            self.tvSubjects.selectionModel().currentChanged.connect(self.tvSubjectChanged)

            self.selectedSubject = first.first(subject for subject in self.subjects  if subject.subject.uniqueIdentifier == self.selectedSubject.subject.uniqueIdentifier)

            self.reloadEvents()
            self.tvEvents.selectionModel().currentChanged.connect(self.tvEventsChanged)


    def reloadSites(self):
        successfull, self.studies = self.ocWebServices.listAllStudies()

        # Quick way of crating simple viewModel
        self.studySitesModel = QtGui.QStandardItemModel()
        self.studySitesModel.setHorizontalHeaderLabels(["OID", "Partner Site", "Study"])

        row = 0
        for study in self.studies:
            if len(study.sites) > 0:
                for site in study.sites:
                    siteOidValue = QtGui.QStandardItem(site.oid)
                    siteNameValue = QtGui.QStandardItem(site.name)
                    studyNameValue = QtGui.QStandardItem(study.name())

                    self.studySitesModel.setItem(row, 0, siteOidValue)
                    self.studySitesModel.setItem(row, 1, siteNameValue)
                    self.studySitesModel.setItem(row, 2, studyNameValue)

                    row = row + 1

        self.tvStudies.setModel(self.studySitesModel)
        self.tvStudies.resizeColumnsToContents()


    def reloadSubjects(self):
        self.subjects = self.ocWebServices.listAllStudySubjectsByStudySite(self.selectedStudy, self.selectedStudySite)

        # Quick way of crating simple viewModel
        self.subjectsModel = QtGui.QStandardItemModel()
        self.subjectsModel.setHorizontalHeaderLabels(["PID", "Gender", "Enrollment date"])

        row = 0
        for studySubject in self.subjects:
            pidItem = QtGui.QStandardItem(studySubject.subject.uniqueIdentifier)
            genderItem = QtGui.QStandardItem(studySubject.subject.gender)
            enrollmentDateItem = QtGui.QStandardItem(studySubject.enrollmentDate)

            self.subjectsModel.setItem(row, 0, pidItem)
            self.subjectsModel.setItem(row, 1, genderItem)
            self.subjectsModel.setItem(row, 2, enrollmentDateItem)

            row = row + 1

        self.tvSubjects.setModel(self.subjectsModel)
        self.tvSubjects.resizeColumnsToContents()


    def reloadEvents(self):
        self.events = self.selectedSubject.events

        # Quick way of crating simple viewModel
        self.eventsModel = QtGui.QStandardItemModel()
        self.eventsModel.setHorizontalHeaderLabels(["Event OID", "Start date"])

        row = 0
        for event in self.events:
            oidItem = QtGui.QStandardItem(event.eventDefinitionOID)
            startDateItem = QtGui.QStandardItem(event.startDate.isoformat())

            self.eventsModel.setItem(row, 0, oidItem)
            self.eventsModel.setItem(row, 1, startDateItem)

            row = row + 1

        self.tvEvents.setModel(self.eventsModel)
        self.tvEvents.resizeColumnsToContents()