#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Logging
import logging
import logging.config

# PyQt - threading
from PyQt4 import QtCore

# String
from string import whitespace

# OC
import OCConnectInfo

# For proxy
import socks

# Services
from services.OCDataWsService import OCDataWsService
from services.OCEventWsService import OCEventWsService
from services.OCStudyEventDefinitionWsService import OCStudyEventDefinitionWsService
from services.OCStudySubjectWsService import OCStudySubjectWsService
from services.OCStudyWsService import OCStudyWsService

 ######   #######  ##    ##  ######  ########  ######  
##    ## ##     ## ###   ## ##    ##    ##    ##    ## 
##       ##     ## ####  ## ##          ##    ##       
##       ##     ## ## ## ##  ######     ##     ######  
##       ##     ## ##  ####       ##    ##          ## 
##    ## ##     ## ##   ### ##    ##    ##    ##    ## 
 ######   #######  ##    ##  ######     ##     ######

# WSDL locations for web services
STUDYURL = "ws/study/v1/studyWsdl.wsdl"
DATAURL = "ws/data/v1/dataWsdl.wsdl"
EVENTURL = "ws/event/v1/eventWsdl.wsdl"
STUDYSUBJECTURL = "ws/studySubject/v1/studySubjectWsdl.wsdl"
STUDYEVENTDEFURL = "ws/studyEventDefinition/v1/studyEventDefinitionWsdl.wsdl"

# OC result value after calling ws
STATUSSUCCCESS = "Success"
STATUSFAIL = "Fail"

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########

class OCWebServices():
    """SOAP web services to OpenClinica

    Unify and simplify the access to OC web services methods
    """

    #----------------------------------------------------------------------
    #--------------------------- Constructors -----------------------------

    def __init__(self, ocConnectInfo, proxyHost="", proxyPort="", noProxy="", proxyUsr="", proxyPass="", trace=logging.INFO):
        """Constructor

        Param ocConnectInfo holds the basic OpenClinica connection information
        """
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        self.ocConnectInfo = ocConnectInfo

        proxyStr = None
        if noProxy != "" and noProxy is not whitespace and noProxy in self.ocConnectInfo.baseUrl:
            proxyStr = None
        else:
            if proxyHost != "" and proxyHost is not whitespace and proxyPort != "" and proxyPort is not whitespace:
                proxyStr = proxyHost + ":" + proxyPort

        if proxyStr:
            self._logger.info("OC SOAP web services are going to use: " + proxyStr)
        else:
            self._logger.info("OC SOAP web services are going to be used with enviromental proxy (including no proxy).")

        self._logger.info("OC SOAP web services are going to be used with authentication: " + str(proxyUsr))

        # Define OC WS bindings
        self.studyBinding = OCStudyWsService(self.ocConnectInfo.baseUrl + STUDYURL, proxyStr, proxyUsr, proxyPass, trace)
        self.dataBinding = OCDataWsService(self.ocConnectInfo.baseUrl + DATAURL, proxyStr, proxyUsr, proxyPass, trace)
        self.studySubjectBinding = OCStudySubjectWsService(self.ocConnectInfo.baseUrl + STUDYSUBJECTURL, proxyStr, proxyUsr, proxyPass, trace)
        self.studyEventDefinitionBinding = OCStudyEventDefinitionWsService(self.ocConnectInfo.baseUrl + STUDYEVENTDEFURL, proxyStr, proxyUsr, proxyPass, trace)
        self.eventBinding = OCEventWsService(self.ocConnectInfo.baseUrl + DATAURL, proxyStr, proxyUsr, proxyPass, trace)

        # Define WSSE security
        self.studyBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)
        self.dataBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)
        self.studySubjectBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)
        self.studyEventDefinitionBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)
        self.eventBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    #----------------------------------------------------------------------
    #----------------------------- Studies --------------------------------

    def getStudyMetadata(self, study, thread=None):
        """Get ODM metadata for study

        Param study specifies the study
        Returns XML ODM metadata of the study
        """
        sucessfull = False
        result = ""
        data = None

        result, data =  self.studyBinding.getMetadata(study)

        if result == STATUSSUCCCESS:
            sucessfull = True
        elif result == STATUSFAIL:
            sucessfull = False

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), str(data))
            return None
        else:
            return sucessfull, data


    def listAllStudies(self, data=None, thread=None):
        """Query studies available for the user

        Returns collection of study domain objects
        """
        self._logger.debug("listAllStudies")

        successful = False
        result = ""
        data = None

        result, data = self.studyBinding.listAll()

        if result == STATUSSUCCCESS:
            successful = True
        elif result == STATUSFAIL:
            successful = False

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), data)
            return None
        else:    
            return successful, data

    #----------------------------------------------------------------------
    #----------------------------- Subjects -------------------------------

    def listAllStudySubjectsByStudy(self, data=None, thread=None):
        """Query all study subject by study

        Returns collection of studySubject domain objects
        """
        if data:
            study = data[0]
            metadata = data[1]

        result = self.studySubjectBinding.listAllByStudy(study, metadata)

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), result)
            return None
        else:
            return result


    def listAllStudySubjectsByStudySite(self, data=None, thread=None):
        """Query all study subject by study site

        Returns collection of studySubject domain objects
        """
        if data:
            study = data[0]
            site = data[1]
            metadata = data[2]

        result = self.studySubjectBinding.listAllByStudySite(study, site, metadata)

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), result)
            return None
        else:
            return result


    def createStudySubject(self, studySubject, study, studySite):
        """Create new StudySubject entity in OC
        """
        return self.studySubjectBinding.create(studySubject, study, studySite)


    def isStudySbuject(self, studySubject, study, studySite):
        """Checks if the specified subject belgons to OC studySbujects
        """
        return self.studySubjectBinding.isStudySbuject(studySubject)

    #----------------------------------------------------------------------
    #----------------------------- Study Event ----------------------------

    def scheduleStudyEvent(self, study, site, studySubject, event):
        """Schedule study event for studySbuject
        """
        successful = False
        result = ""

        result = self.eventBinding.schedule(study, site, studySubject, event)

        if result == STATUSSUCCCESS:
            successful = True
        elif result == STATUSFAIL:
            successful = False

        return successful


    def listAllStydyEventDefinitionsByStudy(self, study):
        """Query all study events by study

        Returns collection of studyEventDefinition domain objects
        """
        return self.studyEventDefinitionBinding.listAllByStudy(study)

    #----------------------------------------------------------------------
    #--------------------------------- Data -------------------------------

    def importODM(self, odm):
        """Import ODM structured data into OC

        Param odm is XML formated data according to ODM and study metadata
        Returns result of the import
        """
        successful = False
        result = ""

        result = self.dataBinding.importData(odm)

        if result == STATUSSUCCCESS:
            successful = True
        elif result == STATUSFAIL:
            successful = False

        return successful

