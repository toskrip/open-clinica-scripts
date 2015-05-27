#----------------------------------------------------------------------
#------------------------------ Modules -------------------------------
# PyQt
from datetime import datetime
import sys

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT

from domain.Person import Person
from domain.StudySubject import StudySubject
from domain.Subject import Subject
from utils import first


# Standard
# Date
# Domain
# Utils
#----------------------------------------------------------------------
class NewSubjectDialog(QtGui.QDialog):
    """New subject
    """

    #----------------------------------------------------------------------
    #--------------------------- Constructors -----------------------------

    def __init__(self, parent = None):
        """
        """
        QtGui.QDialog.__init__(self, parent)

        #------------------------------------------------------
        #-------------------- GUI -----------------------------
        self.width = 640
        self.height = 500
        self.setFixedSize(self.width, self.height);
        self.setWindowTitle("Create study subject dialog")

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

        #-----------------------------------------------------------
        #------------------ Services ----------------------------
        self.svcPseudonymisation = None

    #----------------------------------------------------------------------
    #--------------------------- Setup UI  --------------------------------

    def __setupDialogFieldsUI(self):
        """
        """
        # Dialog grid
        layout = QtGui.QGridLayout()
        self.studySubjectGroup = QtGui.QGroupBox("Create a new study subject: ")
        self.studySubjectGroup.setLayout(layout)

        lblMandatory1 = QtGui.QLabel("*")
        lblMandatory2 = QtGui.QLabel("*")
        lblMandatory3 = QtGui.QLabel("*")
        lblMandatory4 = QtGui.QLabel("*")
        lblMandatory5 = QtGui.QLabel("*")
        lblMandatory6 = QtGui.QLabel("*")

        # Study subject
        lblStudy = QtGui.QLabel("Study and site: ")
        self.lblStudyAndSite = QtGui.QLabel("")
        lblEnrollmentDate = QtGui.QLabel("Enrollemnt date: ")
        self.dateEnrollment = QtGui.QDateEdit()
        self.dateEnrollment.setDisplayFormat("yyyy-MM-dd")
        self.btnShowEnrollmentDateCalendar = QtGui.QPushButton("...")
        self.calEnrollment = QtGui.QCalendarWidget()

        layout.addWidget(lblStudy, 0, 0)
        layout.addWidget(self.lblStudyAndSite, 0, 1, 1, 4)
        layout.addWidget(lblEnrollmentDate, 2, 0)
        layout.addWidget(self.dateEnrollment, 2, 1)
        layout.addWidget(self.btnShowEnrollmentDateCalendar, 2, 4)
        layout.addWidget(lblMandatory1, 2, 5)

        # Subject person PID
        lblPidGenerator = QtGui.QLabel("PID generator: ")
        self.lblPidg = QtGui.QLabel()

        lblName = QtGui.QLabel("Name: ")
        self.txtPatientName = QtGui.QLineEdit()
        lblSurname = QtGui.QLabel("Surname: ")
        self.txtPatientSurname = QtGui.QLineEdit()
        lblBirthName = QtGui.QLabel("Birthname: ")
        self.txtPatientBirthName = QtGui.QLineEdit()
        lblBirthdate = QtGui.QLabel("Birth date: ")
        self.dateBirthdate = QtGui.QDateEdit()
        self.dateBirthdate.setDisplayFormat("yyyy-MM-dd")
        self.btnShowBirthdateDateCalendar = QtGui.QPushButton("...")

        self.rbtnMale = QtGui.QRadioButton("m")
        self.rbtnFemale = QtGui.QRadioButton("f")
        genderSeparatorGroup = QtGui.QGroupBox("Gender: ")
        genderSeparatorBox= QtGui.QHBoxLayout();
        genderSeparatorGroup.setLayout(genderSeparatorBox)
        genderSeparatorBox.addWidget(self.rbtnMale)
        genderSeparatorBox.addWidget(self.rbtnFemale)
        genderSeparatorBox.addStretch(1)

        lblCity = QtGui.QLabel("City: ")
        self.txtLivingCity = QtGui.QLineEdit()
        lblZip = QtGui.QLabel("ZIP code: ")
        self.txtZipCode = QtGui.QLineEdit()

        lblPid = QtGui.QLabel("PID: ")
        self.txtPid = QtGui.QLineEdit()
        self.txtPid.setEnabled(False)
        self.btnGeneratePid = QtGui.QPushButton("Generate PID")
        self.btnPatientData = QtGui.QPushButton("Patient Data")
        self.btnPatientData.setVisible(False)
        self.btnPatientData.setToolTip("show associated patient data according PID")

        layout.addWidget(lblPidGenerator, 3, 0)
        layout.addWidget(self.lblPidg, 3, 1, 1, 4)
        layout.addWidget(lblName, 4, 0)
        layout.addWidget(self.txtPatientName, 4, 1, 1, 4)
        layout.addWidget(lblMandatory2, 4, 5)
        layout.addWidget(lblSurname, 5, 0)
        layout.addWidget(self.txtPatientSurname, 5, 1, 1, 4)
        layout.addWidget(lblMandatory3, 5, 5)
        layout.addWidget(genderSeparatorGroup, 6, 0)
        layout.addWidget(lblMandatory4, 6, 1)
        layout.addWidget(lblBirthdate, 7, 0)
        layout.addWidget(self.dateBirthdate, 7, 1)
        layout.addWidget(self.btnShowBirthdateDateCalendar, 7, 4)
        layout.addWidget(lblMandatory5, 7, 5)
        layout.addWidget(lblCity, 8, 0)
        layout.addWidget(self.txtLivingCity, 8, 1, 1, 4)
        layout.addWidget(lblZip, 9, 0)
        layout.addWidget(self.txtZipCode, 9, 1, 1, 4)

        layout.addWidget(lblPid, 10, 0)
        layout.addWidget(self.txtPid, 10, 1)
        layout.addWidget(self.btnGeneratePid, 10, 2)
        layout.addWidget(self.btnPatientData, 10, 3)
        layout.addWidget(lblMandatory6, 10, 5)

        # Surenes
        self.chbSureness = QtGui.QCheckBox("I am sure that provided data\nis correct.")
        self.chbSureness.setVisible(False)
        layout.addWidget(self.chbSureness, 11, 0)

        space = QtGui.QSpacerItem(0, 1000)
        layout.addItem(space, 13, 0)

        self.connect(self.calEnrollment, QtCore.SIGNAL('selectionChanged()'), self.enrollmentDateChanged)

        self.btnGeneratePid.clicked.connect(self.btnGeneratePidClicked)
        self.btnPatientData.clicked.connect(self.btnPatientDataCicked)

        self.rbtnMale.toggled.connect(self.rbtnMaleToggled)
        self.rbtnFemale.toggled.connect(self.rbtnFemaleToggled)

        return self.studySubjectGroup

    #----------------------------------------------------------------------
    #--------------------------- Set View Model ---------------------------

    def setData(self, study, site):
        """
        """
        self.lblStudyAndSite.setText(study.name() + " : " + site.name)
        self.lblPidg.setText(self.svcPseudonymisation.connectInfo.baseUrl)
        self.dateEnrollment.setDate(datetime.now())

    #----------------------------------------------------------------------
    #----------------------------- Event Handlers -------------------------

    def btnGeneratePidClicked(self):
        """
        """
        # Clear
        self.txtPid.setText("")

        person = Person()
        self.newStudySubject.subject.person = person

        person.firstname = self.txtPatientName.text()
        person.surname = self.txtPatientSurname.text()
        person.birthdate = self.dateBirthdate.date().toPyDate()

        if (self.txtLivingCity.text() != ""):
            person.city = self.txtLivingCity.text()
        if (self.txtZipCode.text() != ""):
            person.zippcode = self.txtZipCode.text()

        try:
            if self.svcPseudonymisation is not None:
                sessionId, uri1 = self.svcPseudonymisation.newSession()
                tokenId, uri2 = self.svcPseudonymisation.newPatientToken(sessionId)

                # Not sure about patient data
                if self.chbSureness.isChecked() != True:
                    # Tentative says if id is temorally
                    # PID is generated (new if new)
                    pid, tentative = self.svcPseudonymisation.createPatientJson(tokenId, person)
                    self.svcPseudonymisation.deleteSession(sessionId)

                    if pid != "":
                        self.newStudySubject.subject.uniqueIdentifier = pid
                        self.txtPid.setText(pid)
                        self.btnPatientData.setVisible(True)
                    else:
                        # Show dialog to check and correct data if sure that select checkbox and genrate PID again
                        # than sureness has to be set true
                        # and genrated PID will be marged as tentative
                        self.chbSureness.setVisible(True)
                        QtGui.QMessageBox.warning(self, 'Warning', "There is a possible matching patient already registered.\nCheck and correct the data and click generate again.\nIf you are sure that the data is correct check the I am sure that data is correct check box and generate button again.")
                # Sure about patient data
                else:
                    pid, tentative = self.svcPseudonymisation.createSurePatientJson(tokenId, person)
                    self.svcPseudonymisation.deleteSession(sessionId)

                    if pid != "":
                        self.newStudySubject.subject.uniqueIdentifier = pid
                        self.txtPid.setText(pid)
                        self.btnPatientData.setVisible(True)
        except:
            QtGui.QMessageBox.warning(self, 'Error', 'During PID generation.')


    def btnPatientDataCicked(self):
        #
        pid = str(self.txtPid.text())
        if self.svcPseudonymisation is not None:
            sessionId, uri1 = self.svcPseudonymisation.newSession()
            tokenId, uri2 = self.svcPseudonymisation.readPatientToken(sessionId, pid)

            self.svcPseudonymisation.getPatient(tokenId)
            self.svcPseudonymisation.deleteSession(sessionId)
        #except:
        #    pass


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

        # TODO ISO date
        # put it to ui
        self.txtEnrollment.setText(pydate.isoformat())

    #----------------------------------------------------------------------
    #------------------- Dialog Buttons Handlers --------------------------

    def handleOk(self):
        """OK Button Click
        """
        self.newStudySubject.enrollmentDate = self.dateEnrollment.date().toPyDate()
        # TODO: self.isValid()
        if (self.txtPid.text() != ""):
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Data is not valied.')


    def handleCancel(self):
        """Cancel Button Click
        """
        self.reject()

