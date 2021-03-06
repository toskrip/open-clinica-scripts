#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######



# Standard
import sys
from datetime import datetime

# PyQt
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT

# Domain
from domain.Event import Event
from domain.StudySubject import StudySubject
from domain.Subject import Subject

# Utils
from utils import first

class NewEventDialog(QtGui.QDialog):
    """New subject
    """

    def __init__(self, parent = None):
        """Default Constructor
        """
        QtGui.QDialog.__init__(self, parent)

        #------------------------------------------------------
        #-------------------- GUI -----------------------------
        # self.width = 640
        # self.height = 500
        # self.setFixedSize(self.width, self.height);
        self.setWindowTitle("Shedule study event for subject dialog")

        # Dialog layout root
        rootLayout = QtGui.QVBoxLayout(self)

        # Metadata field for mapping UI
        rootLayout.addWidget(self.__setupDialogFieldsUI())

        # Dialog buttons
        btnLayout = QtGui.QGridLayout()
        btnLayout.setSpacing(10)
        rootLayout.addLayout(btnLayout)

        self.btnOk = QtGui.QPushButton("Schedule")
        self.btnCancel = QtGui.QPushButton("Cancel")

        btnLayout.addWidget(self.btnOk, 1, 0)
        btnLayout.addWidget(self.btnCancel, 1, 1)

        #----------------------------------------------------------
        #----------------- Event handlers -------------------------

        self.btnOk.clicked.connect(self.handleOk)
        self.btnCancel.clicked.connect(self.handleCancel)

        #-----------------------------------------------------------
        #------------------ View Models ----------------------------
        self.selectedEvent = None


    #----------------------------------------------------------------------
    #--------------------------- Setup UI  --------------------------------

    def __setupDialogFieldsUI(self):
        """
        """
        # Dialog grid
        layout = QtGui.QGridLayout()
        eventGroup = QtGui.QGroupBox("Shedule study event for subject: ")
        eventGroup.setLayout(layout)

        lblMandatory1 = QtGui.QLabel("*")

        lblStudy = QtGui.QLabel("Study and site: ")
        self.lblStudyAndSite = QtGui.QLabel("")

        lblSubjectText = QtGui.QLabel("Subject: ")
        self.lblSubject = QtGui.QLabel("")

        lblStudyEventText = QtGui.QLabel("Choose study event: ")
        self.cmbStudyEvents = QtGui.QComboBox()

        layout.addWidget(lblStudy, 0, 0)
        layout.addWidget(self.lblStudyAndSite, 0, 1, 1, 4)

        layout.addWidget(lblSubjectText, 1, 0)
        layout.addWidget(self.lblSubject, 1, 1, 1, 4)

        layout.addWidget(lblStudyEventText, 2, 0)
        layout.addWidget(self.cmbStudyEvents, 2, 1, 1, 4)
        layout.addWidget(lblMandatory1, 2, 5)

        space = QtGui.QSpacerItem(0, 1000)
        # layout.addItem(space, 3, 0)

        self.cmbStudyEvents.currentIndexChanged['QString'].connect(self.cmbStudyEventsChanged)

        return eventGroup

    #----------------------------------------------------------------------
    #--------------------------- Set View Model ---------------------------

    def setData(self, study, site, subject, studyEvents):
        """
        """
        if study and site:
            studyText = study.name + " : " + site.name
        else:
            studyText = study.name 

        self.lblStudyAndSite.setText(studyText)
        self.lblSubject.setText(subject.label)

        self.studyEvents = studyEvents
        self.unsheduledEvents = []

        for event in studyEvents:
            exists = False

            if (not exists):
                self.unsheduledEvents.append(event.oid)

        self.cmbStudyEvents.addItems(self.unsheduledEvents)

    #----------------------------------------------------------------------
    #----------------------------- Event Handlers -------------------------

    def cmbStudyEventsChanged(self, text):
        """
        """
        self.selectedEvent = first.first(
            unsheduledEvent for unsheduledEvent in self.studyEvents  if unsheduledEvent.oid == text
        )

    #----------------------------------------------------------------------
    #------------------- Dialog Buttons Handlers --------------------------

    def handleOk(self):
        """OK Button Click
        """
        if (self.selectedEvent is not None):
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, "Error", "Data is not valied")


    def handleCancel(self):
        """Cancel Button Click
        """
        self.reject()

