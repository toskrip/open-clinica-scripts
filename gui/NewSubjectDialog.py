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
from datetime import date
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT

# Domain
from domain.StudySubject import StudySubject
from domain.Subject import Subject

# Utils
from utils import first

class NewSubjectDialog(QtGui.QDialog):
    """New subject dialog
    """

    def __init__(self, parent = None):
        """Default constructor
        """
        QtGui.QDialog.__init__(self, parent)

        #------------------------------------------------------
        #-------------------- GUI -----------------------------
        self.width = 300
        self.height = 300
        self.setFixedSize(self.width, self.height);
        self.setWindowTitle("Create a new study subject")

        # Dialog layout root
        rootLayout = QtGui.QVBoxLayout(self)

        # Metadata field for mapping UI
        rootLayout.addWidget(self.__setupDialogFieldsUI())

        # Dialog buttons
        btnLayout = QtGui.QGridLayout()
        btnLayout.setSpacing(10)
        rootLayout.addLayout(btnLayout)

        self.btnOk = QtGui.QPushButton("Create")
        self.btnCancel = QtGui.QPushButton("Cancel")

        btnLayout.addWidget(self.btnOk, 1, 0)
        btnLayout.addWidget(self.btnCancel, 1, 1)

        #----------------------------------------------------------
        #----------------- Event handlers -------------------------

        self.btnOk.clicked.connect(self.handleOk)
        self.btnCancel.clicked.connect(self.handleCancel)

        #-----------------------------------------------------------
        #------------------ View Models ----------------------------
        self.newStudySubject = StudySubject()
        self.newStudySubject.subject = Subject()

        # Based on study subject id generation
        # if manual than specify
        # even if automatic it has to be empty string
        self.newStudySubject.label = "xxb"

        # Based on metadata (can be optional)
        self.newStudySubject.subject.uniqueIdentifier = "DD-ST-xxb"

    def __setupDialogFieldsUI(self):
        """
        """
        # Dialog grid
        layout = QtGui.QGridLayout()
        self.studySubjectGroup = QtGui.QGroupBox("Create a new study subject: ")
        self.studySubjectGroup.setLayout(layout)

        lblMandatory = QtGui.QLabel("*")

        # Study subject
        lblStudy = QtGui.QLabel("Study and site: ")
        self.lblStudyAndSite = QtGui.QLabel("")
        lblEnrollmentDate = QtGui.QLabel("Enrollemnt date: ")
        self.dateEnrollment = QtGui.QDateEdit()
        self.dateEnrollment.setDisplayFormat("yyyy-MM-dd")
        self.calEnrollment = QtGui.QCalendarWidget()

        layout.addWidget(lblStudy, 0, 0)
        layout.addWidget(self.lblStudyAndSite, 0, 1, 1, 4)
        layout.addWidget(lblEnrollmentDate, 2, 0)
        layout.addWidget(self.dateEnrollment, 2, 1)

        layout.addWidget(lblMandatory, 2, 5)

        self.rbtnMale = QtGui.QRadioButton("m")
        self.rbtnFemale = QtGui.QRadioButton("f")
        genderSeparatorGroup = QtGui.QGroupBox("Gender: ")
        genderSeparatorBox= QtGui.QHBoxLayout();
        genderSeparatorGroup.setLayout(genderSeparatorBox)
        genderSeparatorBox.addWidget(self.rbtnMale)
        genderSeparatorBox.addWidget(self.rbtnFemale)
        genderSeparatorBox.addStretch(1)

        layout.addWidget(genderSeparatorGroup, 6, 0)
        layout.addWidget(lblMandatory, 6, 1)

        space = QtGui.QSpacerItem(0, 1000)
        layout.addItem(space, 13, 0)

        self.connect(self.calEnrollment, QtCore.SIGNAL('selectionChanged()'), self.enrollmentDateChanged)
        self.rbtnMale.toggled.connect(self.rbtnMaleToggled)
        self.rbtnFemale.toggled.connect(self.rbtnFemaleToggled)

        return self.studySubjectGroup

    #----------------------------------------------------------------------
    #--------------------------- Set View Model ---------------------------

    def setData(self, study, site):
        """
        """
        if study and site:
            studyInfo = study.name + " : " + site.name
        else:
            studyInfo = study.name

        self.lblStudyAndSite.setText(studyInfo)
        self.dateEnrollment.setDate(date.today())

    #----------------------------------------------------------------------
    #----------------------------- Event Handlers -------------------------

    def rbtnMaleToggled(self, enabled):
        if enabled:
            self.newStudySubject.subject.gender = "m"


    def rbtnFemaleToggled(self, enabled):
        if enabled:
            self.newStudySubject.subject.gender = "f"


    def enrollmentDateChanged(self):
        # Fetch the currently selected date, this is a QDate object
        date = self.calEnrollment.selectedDate()
        # This is a gives us the date contained in the QDate as a native
        # python date[time] object
        pydate = date.toPyDate()

        self.txtEnrollment.setText(pydate.isoformat())

    #----------------------------------------------------------------------
    #------------------- Dialog Buttons Handlers --------------------------

    def handleOk(self):
        """OK Button Click
        """
        self.newStudySubject.enrollmentDate = self.dateEnrollment.date().toPyDate()
        self.accept()

    def handleCancel(self):
        """Cancel Button Click
        """
        self.reject()

