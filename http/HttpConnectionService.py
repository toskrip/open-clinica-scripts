#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import os

# Logging
import logging
import logging.config

# HTTP
import requests
from requests.auth import HTTPBasicAuth

# String
from string import whitespace

# Datetime
from datetime import datetime

# JSON
import json

# Domain
from domain.Subject import Subject
from domain.Event import Event
from domain.Crf import Crf

# Utils
from utils.JsonSerializer import JsonSerializer

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########

class HttpConnectionService(object):
    """HTTP connection service
    """

    def __init__(self, ip, port, userDetails):
        """Default constructor
        """
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        # Server IP and port as members
        self.__ip = ip
        self.__port = port
        self.__userDetails = userDetails
        self.__application = ""

        # Proxy settings
        self._proxyEnabled = False
        self._proxyHost = ""
        self._proxyPort = ""
        self._noProxy = ""

        # Proxy authentication
        self._proxyAuthEnabled = False
        self._proxyAuthLogin = ""
        self._proxyAuthPassword = ""

########  ########   #######  ########  ######## ########  ######## #### ########  ######
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ##
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ##
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ##
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ######

    @property
    def ip(self):
        """IP Getter
        """
        return self.__ip

    @ip.setter
    def ip(self, value):
        """IP Setter
        """
        if self.__ip != value:
            self.__ip = value

    @property
    def port(self):
        """Port Getter
        """
        return self.__port

    @port.setter
    def port(self, value):
        """Port Setter
        """
        if self.__port != value:
            self.__port = value

    @property
    def application(self):
        """Application Getter
        """
        return self.__application

    @application.setter
    def application(self, value):
        """Application Setter
        """
        if self.__application != value:
            self.__application = "/" + value

##     ## ######## ######## ##     ##  #######  ########   ######  
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ## 
#### #### ##          ##    ##     ## ##     ## ##     ## ##       
## ### ## ######      ##    ######### ##     ## ##     ##  ######  
##     ## ##          ##    ##     ## ##     ## ##     ##       ## 
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ## 
##     ## ########    ##    ##     ##  #######  ########   ######  

    def setupProxy(self, host, port, noProxy):
        """Enable communication over proxy
        """
        self._proxyHost = host
        self._proxyPort = port
        self._noProxy = noProxy

        self._proxyEnabled = True

    def setupProxyAuth(self, login, password):
        """Enable proxy authentication
        """
        self._proxyAuthLogin = login
        self._proxyAuthPassword = password

        self._proxyAuthEnabled = True

 #######   ######      ######  ##     ## ########        ## ########  ######  ######## 
##     ## ##    ##    ##    ## ##     ## ##     ##       ## ##       ##    ##    ##    
##     ## ##          ##       ##     ## ##     ##       ## ##       ##          ##    
##     ## ##           ######  ##     ## ########        ## ######   ##          ##    
##     ## ##                ## ##     ## ##     ## ##    ## ##       ##          ##    
##     ## ##    ##    ##    ## ##     ## ##     ## ##    ## ##       ##    ##    ##    
 #######   ######      ######   #######  ########   ######  ########  ######     ##    

    def getStudyCasebookSubjects(self, ocBaseUrl, studyOid):
        """Get study casebook subjects
        """
        method = studyOid + "/*/*/*"
        results = []

        r = self._ocRequest(ocBaseUrl, method)

        if r.status_code == 200:
            if "ClinicalData" in r.json():
                subjectData = r.json()["ClinicalData"]["SubjectData"]

                # Multiple subjects
                if type(subjectData) is list:
                    for subj in subjectData:
                        subject = Subject()
                        subject.oid = subj["@SubjectKey"]
                        subject.studySubjectId = subj["@OpenClinica:StudySubjectID"]
                        if "@OpenClinica:UniqueIdentifier" in subj:
                            subject.uniqueIdentifier = subj["@OpenClinica:UniqueIdentifier"]
                        results.append(subject)
                # Only one subject reported
                elif type(subjectData) is dict:
                    subj = subjectData
                    subject = Subject()
                    subject.oid = subj["@SubjectKey"]
                    subject.studySubjectId = subj["@OpenClinica:StudySubjectID"]
                    if "@OpenClinica:UniqueIdentifier" in subj:
                        subject.uniqueIdentifier = subj["@OpenClinica:UniqueIdentifier"]
                    results.append(subject)

        return results

 #######   ######     ######## ##     ## ######## ##    ## ######## 
##     ## ##    ##    ##       ##     ## ##       ###   ##    ##    
##     ## ##          ##       ##     ## ##       ####  ##    ##    
##     ## ##          ######   ##     ## ######   ## ## ##    ##    
##     ## ##          ##        ##   ##  ##       ##  ####    ##    
##     ## ##    ##    ##         ## ##   ##       ##   ###    ##    
 #######   ######     ########    ###    ######## ##    ##    ##    

    def getStudyCasebookEvents(self, ocBaseUrl, studyOid, subjectOid):
        """Get study casebook subject events
        """
        method = studyOid + "/" + subjectOid + "/*/*"
        results = []

        r = self._ocRequest(ocBaseUrl, method)

        if r.status_code == 200:
            if "ClinicalData" in r.json():
                if "SubjectData" in r.json()["ClinicalData"]:
                    if "StudyEventData" in r.json()["ClinicalData"]["SubjectData"]:
                        
                        eventData = r.json()["ClinicalData"]["SubjectData"]["StudyEventData"]

                        # Multiple events
                        if type(eventData) is list:
                            for ed in eventData:
                                event = Event()
                                event.eventDefinitionOID = ed["@StudyEventOID"]
                                event.status = ed["@OpenClinica:Status"]

                                dateString = ed["@OpenClinica:StartDate"]
                                format = ""
                                # Is it only date or datetime
                                if len(dateString) == 11:
                                    format = "%d-%b-%Y"
                                elif len(dateString) == 20:
                                    format = "%d-%b-%Y %H:%M:%S"

                                event.startDate = datetime.strptime(dateString, format)
                                event.studyEventRepeatKey = ed["@StudyEventRepeatKey"]

                                # Subject Age At Event is optional (because collect birth date is optional)
                                if "OpenClinica:SubjectAgeAtEvent" in ed:
                                    event.subjectAgeAtEvent = ed["OpenClinica:SubjectAgeAtEvent"]

                                # Resulting eCRFs
                                if "FormData" in ed:
                                    formData = ed["FormData"]

                                    # Multiple forms
                                    if type(formData) is list:
                                        for frm in formData:
                                            crf = Crf()
                                            crf.oid = frm["@FormOID"]
                                            crf.version = frm["@OpenClinica:Version"]
                                            crf.status = frm["@OpenClinica:Status"]
                                            event.addCrf(crf)
                                    # Only one form in event
                                    elif type(formData) is dict:
                                        frm  = formData
                                        crf = Crf()
                                        crf.oid = frm["@FormOID"]
                                        crf.version = frm["@OpenClinica:Version"]
                                        crf.status = frm["@OpenClinica:Status"]
                                        event.addCrf(crf)
                                
                                # + automatically schedule default version only (if it is not)
                                eventFormOids = []

                                eventDefinition = r.json()["Study"]["MetaDataVersion"]["StudyEventDef"]
                                if type(eventDefinition) is list:
                                    for ed in eventDefinition:
                                        formRef = ed["FormRef"]
                                        if type(formRef) is list:
                                            for fr in formRef:
                                                eventFormOids.append(fr["@FormOID"])
                                        elif type(formRef) is dict:
                                            eventFormOids.append(formRef["@FormOID"])
                                elif type(eventDefinition) is dict:
                                    ed = eventDefinition
                                    formRef = ed["FormRef"]
                                    if type(formRef) is list:
                                        for fr in formRef:
                                            eventFormOids.append(fr["@FormOID"])
                                    elif type(formRef) is dict:
                                        eventFormOids.append(formRef["@FormOID"])

                                formDefinition = r.json()["Study"]["MetaDataVersion"]["FormDef"]
                                if type(formDefinition) is list:
                                    for fd in formDefinition:
                                        if fd["@OID"] in eventFormOids:
                                            if not event.hasScheduledCrf(fd["@OID"]):
                                                if fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]["@IsDefaultVersion"] == "Yes":
                                                    crf = Crf()
                                                    crf.oid = fd["@OID"]
                                                    event.addCrf(crf)
                                elif type(formDefinition) is dict:
                                    fd = formDefinition
                                    if fd["@OID"] in eventFormOids:
                                        if not event.hasScheduledCrf(fd["@OID"]):
                                            if fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]["@IsDefaultVersion"] == "Yes":
                                                crf = Crf()
                                                crf.oid = fd["@OID"]
                                                event.addCrf(crf)

                                results.append(event)
                        # Only one event reported
                        elif type(eventData) is dict:
                            ed = eventData

                            event = Event()
                            event.eventDefinitionOID = ed["@StudyEventOID"]
                            event.status = ed["@OpenClinica:Status"]
                            dateString = ed["@OpenClinica:StartDate"]

                            format = ""
                            # Is it only date or datetime
                            if len(dateString) == 11:
                                format = "%d-%b-%Y"
                            elif len(dateString) == 20:
                                format = "%d-%b-%Y %H:%M:%S"

                            event.startDate = datetime.strptime(dateString, format)
                            event.studyEventRepeatKey = ed["@StudyEventRepeatKey"]

                            # Subject Age At Event is optional (because collect birth date is optional)
                            if "OpenClinica:SubjectAgeAtEvent" in ed:
                                event.subjectAgeAtEvent = ed["OpenClinica:SubjectAgeAtEvent"]

                            # Resulting eCRFs
                            if "FormData" in ed:
                                formData = ed["FormData"]

                                # Multiple forms
                                if type(formData) is list:
                                    for frm in formData:
                                        crf = Crf()
                                        crf.oid = frm["@FormOID"]
                                        crf.version = frm["@OpenClinica:Version"]
                                        crf.status = frm["@OpenClinica:Status"]
                                        event.addCrf(crf)
                                # Only one form in event
                                elif type(formData) is dict:
                                    frm  = formData
                                    crf = Crf()
                                    crf.oid = frm["@FormOID"]
                                    crf.version = frm["@OpenClinica:Version"]
                                    crf.status = frm["@OpenClinica:Status"]
                                    event.addCrf(crf)
                            # + automatically schedule default version (if it is not)
                            eventFormOids = []

                            eventDefinition = r.json()["Study"]["MetaDataVersion"]["StudyEventDef"]
                            if type(eventDefinition) is list:
                                for ed in eventDefinition:
                                    formRef = ed["FormRef"]
                                    if type(formRef) is list:
                                        for fr in formRef:
                                            eventFormOids.append(fr["@FormOID"])
                                    elif type(formRef) is dict:
                                        eventFormOids.append(formRef["@FormOID"])
                            elif type(eventDefinition) is dict:
                                ed = eventDefinition
                                formRef = ed["FormRef"]
                                if type(formRef) is list:
                                    for fr in formRef:
                                        eventFormOids.append(fr["@FormOID"])
                                elif type(formRef) is dict:
                                    eventFormOids.append(formRef["@FormOID"])

                            formDefinition = r.json()["Study"]["MetaDataVersion"]["FormDef"]
                            if type(formDefinition) is list:
                                for fd in formDefinition:
                                    if fd["@OID"] in eventFormOids:
                                        if not event.hasScheduledCrf(fd["@OID"]):
                                            if fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]["@IsDefaultVersion"] == "Yes":
                                                crf = Crf()
                                                crf.oid = fd["@OID"]
                                                event.addCrf(crf)
                            elif type(formDefinition) is dict:
                                fd = formDefinition
                                if fd["@OID"] in eventFormOids:
                                    if not event.hasScheduledCrf(fd["@OID"]):
                                        if fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]["@IsDefaultVersion"] == "Yes":
                                            crf = Crf()
                                            crf.oid = fd["@OID"]
                                            event.addCrf(crf)

                            results.append(event)

        return results

########  ########  #### ##     ##    ###    ######## ######## 
##     ## ##     ##  ##  ##     ##   ## ##      ##    ##       
##     ## ##     ##  ##  ##     ##  ##   ##     ##    ##       
########  ########   ##  ##     ## ##     ##    ##    ######   
##        ##   ##    ##   ##   ##  #########    ##    ##       
##        ##    ##   ##    ## ##   ##     ##    ##    ##       
##        ##     ## ####    ###    ##     ##    ##    ######## 

    def _getRequest(self, method):
        """Generic GET request to RadPlanBio server
        """
        contentLength = 0
        body = None

        site = "MySiteForAuthorisation"

        s = requests.Session()
        s.headers.update({ "Content-Type": "application/json",  "Content-Length": contentLength, "Site": site, "Username" : self.__userDetails.username, "Password" : self.__userDetails.password })

        auth = None
        if self._proxyAuthEnabled:
            auth = HTTPBasicAuth(self._proxyAuthLogin, self._proxyAuthPassword)
            self._logger.info("Connecting with authentication: " + str(self._proxyAuthLogin))

        # Application proxy enabled
        if self._proxyEnabled:
            if self._noProxy != "" and self._noProxy is not whitespace and self._noProxy in "https://" + self.__ip:
                self._logger.info("Connecting without proxy because of no proxy: " + self._noProxy)
                r = s.get("https://" + self.__ip + ":" + str(self.__port) + self.__application + method.encode("utf-8"), auth=auth, verify=False, proxies={})
            else:
                proxies = { "http" : "http://" + self._proxyHost + ":" + self._proxyPort, "https" : "https://" + self._proxyHost + ":" + self._proxyPort}
                self._logger.info("Connecting with application defined proxy: " + str(proxies))
                r = s.get("https://" + self.__ip + ":" + str(self.__port) + self.__application + method.encode("utf-8"), auth=auth, verify=False, proxies=proxies)
        # Use system proxy
        else:
            proxies = requests.utils.get_environ_proxies("https://" + self.__ip)
            self._logger.info("Using system proxy variables (no proxy applied): " + str(proxies))
            r = s.get("https://" + self.__ip + ":" + str(self.__port) + self.__application + method.encode("utf-8"), auth=auth, verify=False, proxies=proxies)

        return r

    def _postRequest(self, method, body, contentType):
        """Generic POST request to RadPlanBio server
        """
        contentLength = len(body)

        site = "MySiteForAuthorisation"

        s = requests.Session()
        s.headers.update({ "Content-Type": contentType,  "Content-Length": contentLength, "Site": site, "Username" : self.__userDetails.username, "Password" : self.__userDetails.password })

        auth = None
        if self._proxyAuthEnabled:
            auth = HTTPBasicAuth(self._proxyAuthLogin, self._proxyAuthPassword)
            self._logger.info("Connecting with authentication: " + str(self._proxyAuthLogin))

        # Application proxy enabled
        if self._proxyEnabled:
            if self._noProxy != "" and self._noProxy is not whitespace and self._noProxy in "https://" + self.__ip:
                self._logger.info("Connecting without proxy because of no proxy: " + self._noProxy)
                r = s.post("https://" + self.__ip + ":" + str(self.__port) + self.__application + method.encode("utf-8"), auth=auth, data=body, verify=False, proxies={})
            else:
                proxies = { "http" : "http://" + self._proxyHost + ":" + self._proxyPort, "https" : "https://" + self._proxyHost + ":" + self._proxyPort}
                self._logger.info("Connecting with application defined proxy: " + str(proxies))
                r = s.post("https://" + self.__ip + ":" + str(self.__port) + self.__application + method.encode("utf-8"), auth=auth, data=body, verify=False, proxies=proxies)
        # Use system proxy
        else:
            proxies = requests.utils.get_environ_proxies("https://" + self.__ip)
            self._logger.info("Using system proxy variables (no proxy applied): " + str(proxies))
            r = s.post("https://" + self.__ip + ":" + str(self.__port) + self.__application + method.encode("utf-8"), auth=auth, data=body, verify=False, proxies=proxies)

        return r        

    def _ocRequest(self, ocBaseUrl, method):
        """Generic OpenClinica (restfull URL) GET request
        """
        contentLength = 0
        body = None

         # xml, html
        format = "json"

        s = requests.Session()
        loginCredentials = { "j_username": self.__userDetails.username, "j_password" : self.__userDetails.clearpass }

        auth = None
        if self._proxyAuthEnabled:
            auth = HTTPBasicAuth(self._proxyAuthLogin, self._proxyAuthPassword)
            self._logger.info("Connecting with authentication: " + str(self._proxyAuthLogin))

        # Ensure that base URL ends with /
        if ocBaseUrl.endswith("/") == False:
            ocBaseUrl += "/"

        # Application proxy enabled
        if self._proxyEnabled:
            if self._noProxy != "" and self._noProxy is not whitespace and self._noProxy in "https://" + self.__ip:
                self._logger.info("Connecting without proxy because of no proxy: " + self._noProxy)
                r = s.post(ocBaseUrl + "j_spring_security_check", loginCredentials, auth=auth, verify=False, proxies={})
                r = s.get(ocBaseUrl + "rest/clinicaldata/" + format + "/view/" + method, auth=auth, verify=False, proxies={})
            else:
                proxies = { "http" : "http://" + self._proxyHost + ":" + self._proxyPort, "https" : "https://" + self._proxyHost + ":" + self._proxyPort}
                self._logger.info("Connecting with application defined proxy: " + str(proxies))
                r = s.post(ocBaseUrl + "j_spring_security_check", loginCredentials, auth=auth, verify=False, proxies=proxies)
                r = s.get(ocBaseUrl + "rest/clinicaldata/" + format + "/view/" + method, auth=auth, verify=False, proxies=proxies)
        # Use system proxy
        else:
            proxies = requests.utils.get_environ_proxies("https://" + self.__ip)
            self._logger.info("Using system proxy variables (no proxy applied): " + str(proxies))
            
            r = s.post(ocBaseUrl + "j_spring_security_check", loginCredentials, auth=auth, verify=False, proxies=proxies)
            r = s.get(ocBaseUrl + "rest/clinicaldata/" + format + "/view/" + method, auth=auth, verify=False, proxies=proxies)

        return r