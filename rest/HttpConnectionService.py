#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Standard
import os
import sys

# Logging
import logging
import logging.config

# HTTP
import binascii
import requests
from requests.auth import HTTPBasicAuth

# Disable insecure connection warnings
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# String
from string import whitespace

# Datetime
from datetime import datetime

# PyQt - threading
from PyQt4 import QtCore

# JSON
import json

# Domain
from domain.Subject import Subject
from domain.Event import Event
from domain.Crf import Crf
from domain.ItemGroup import ItemGroup
from domain.Item import Item

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
        self._ip = ip
        self._port = port
        self._userDetails = userDetails

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
        return self._ip

    @ip.setter
    def ip(self, value):
        """IP Setter
        """
        self._ip = value

    @property
    def port(self):
        """Port Getter
        """
        return self._port

    @port.setter
    def port(self, value):
        """Port Setter
        """
        self._port = value

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

    def getStudyCasebookSubjects(self, data, thread=None):
        """Get study casebook subjects
        """
        if data:
            ocBaseUrl = data[0]
            studyOid = data[1]

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

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), results)
            return None
        else:
            return results

    def getStudyCasebookSubject(self, ocBaseUrl, studyOid, subjectId):
        """Get casebook of one subject
        SubjectId can be StudySubjectOID (SS_) or StudySubjectID (in new version of OC)
        """
        method = studyOid + "/" + subjectId + "/*/*"
        results = None

        r = self._ocRequest(ocBaseUrl, method)

        if r.status_code == 200:
            if "ClinicalData" in r.json():
                subjectData = r.json()["ClinicalData"]["SubjectData"]
                # Exactly one subject should be reported
                if type(subjectData) is dict:
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

    def getStudyCasebookEvents(self, data, thread=None):
        """Get study casebook subject events
        """
        if data:
            ocUrl = data[0]
            studyOid = data[1]
            studySubjectIdentifier = data[2]

        method = studyOid + "/" + studySubjectIdentifier + "/*/*"
        results = []
        
        r = self._ocRequest(ocUrl, method)

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
                                # Is it only date or datetime (in json the date format looks like this)
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

                                                presentInEventDefinition = fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]

                                                # Form used in multiple Events
                                                if type(presentInEventDefinition) is list:
                                                    for pied in presentInEventDefinition:
                                                        # Only default version forms
                                                        if pied["@IsDefaultVersion"] == "Yes":
                                                            # Only the form that belong to the current event
                                                            if pied["@StudyEventOID"] == event.eventDefinitionOID:
                                                                crf = Crf()
                                                                crf.oid = fd["@OID"]
                                                                event.addCrf(crf)
                                                                break

                                                # Form used in one Event
                                                elif type(presentInEventDefinition) is dict:
                                                    # Only default version forms
                                                    if presentInEventDefinition["@IsDefaultVersion"] == "Yes":
                                                        crf = Crf()
                                                        crf.oid = fd["@OID"]
                                                        event.addCrf(crf)

                                elif type(formDefinition) is dict:
                                    fd = formDefinition
                                    if fd["@OID"] in eventFormOids:
                                        if not event.hasScheduledCrf(fd["@OID"]):

                                            presentInEventDefinition = fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]

                                            # Form used in multiple Events
                                            if type(presentInEventDefinition) is list:
                                                for pied in presentInEventDefinition:
                                                    # Only default version forms
                                                    if pied["@IsDefaultVersion"] == "Yes":
                                                        # Only the form that belong to the current event
                                                        if pied["@StudyEventOID"] == event.eventDefinitionOID:
                                                            crf = Crf()
                                                            crf.oid = fd["@OID"]
                                                            event.addCrf(crf)
                                                            break

                                            # Form used in one Event
                                            elif type(presentInEventDefinition) is dict:
                                                # Only default version forms
                                                if presentInEventDefinition["@IsDefaultVersion"] == "Yes":
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
                            # Is it only date or datetime (in json the date format looks like this)
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

                                            presentInEventDefinition = fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]

                                            # Form used in multiple Events
                                            if type(presentInEventDefinition) is list:
                                                for pied in presentInEventDefinition:
                                                    # Only default version forms
                                                    if pied["@IsDefaultVersion"] == "Yes":
                                                        # Only the form that belong to the current event
                                                        if pied["@StudyEventOID"] == event.eventDefinitionOID:
                                                            crf = Crf()
                                                            crf.oid = fd["@OID"]
                                                            event.addCrf(crf)
                                                            break

                                            # Form used in one Event
                                            elif type(presentInEventDefinition) is dict:
                                                # Only default version forms
                                                if presentInEventDefinition["@IsDefaultVersion"] == "Yes":
                                                    crf = Crf()
                                                    crf.oid = fd["@OID"]
                                                    event.addCrf(crf)

                            elif type(formDefinition) is dict:
                                fd = formDefinition
                                if fd["@OID"] in eventFormOids:
                                    if not event.hasScheduledCrf(fd["@OID"]):

                                        presentInEventDefinition = fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]

                                        # Form used in multiple Events
                                        if type(presentInEventDefinition) is list:
                                            for pied in presentInEventDefinition:
                                                # Only default version forms
                                                if pied["@IsDefaultVersion"] == "Yes":
                                                    # Only the form that belong to the current event
                                                    if pied["@StudyEventOID"] == event.eventDefinitionOID:
                                                        crf = Crf()
                                                        crf.oid = fd["@OID"]
                                                        event.addCrf(crf)
                                                        break

                                        # Form used in one Event
                                        elif type(presentInEventDefinition) is dict:
                                            # Only default version forms
                                            if presentInEventDefinition["@IsDefaultVersion"] == "Yes":
                                                crf = Crf()
                                                crf.oid = fd["@OID"]
                                                event.addCrf(crf)

                            results.append(event)

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), results)
            return None
        else:
            return results

    def getStudyCasebookSubjectWithEvents(self, data, thread=None):
        """Get study casebook subject with events
        """
        if data:
            ocUrl = data[0]
            studyOid = data[1]
            studySubjectIdentifier = data[2]

        method = studyOid + "/" + studySubjectIdentifier + "/*/*"
        result = None
        
        r = self._ocRequest(ocUrl, method)

        if r.status_code == 200:
            if "ClinicalData" in r.json():
                if "SubjectData" in r.json()["ClinicalData"]:
                    
                    subjectData = r.json()["ClinicalData"]["SubjectData"]
                    # Exactly one subject should be reported
                    if type(subjectData) is dict:
                        subj = subjectData

                        subject = Subject()
                        subject.oid = subj["@SubjectKey"]
                        subject.studySubjectId = subj["@OpenClinica:StudySubjectID"]
                        subject.status = subj["@OpenClinica:Status"]

                        if "@OpenClinica:UniqueIdentifier" in subj:
                            subject.uniqueIdentifier = subj["@OpenClinica:UniqueIdentifier"]
                        result = subject

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
                                # Is it only date or datetime (in json the date format looks like this)
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
                                        frm = formData
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

                                itemGroupOids = []
                                formDefinition = r.json()["Study"]["MetaDataVersion"]["FormDef"]
                                if type(formDefinition) is list:
                                    for fd in formDefinition:
                                        if fd["@OID"] in eventFormOids:
                                            if not event.hasScheduledCrf(fd["@OID"]):
                                                
                                                presentInEventDefinition = fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]

                                                # Form used in multiple Events
                                                if type(presentInEventDefinition) is list:
                                                    for pied in presentInEventDefinition:
                                                        # Only default version of non-hidden forms
                                                        if pied["@IsDefaultVersion"] == "Yes" and pied["@HideCRF"] == "No":
                                                            # Only the form that belong to the current event
                                                            if pied["@StudyEventOID"] == event.eventDefinitionOID:
                                                                crf = Crf()
                                                                crf.oid = fd["@OID"]
                                                                event.addCrf(crf)
                                                                break

                                                # Form used in one Event
                                                elif type(presentInEventDefinition) is dict:
                                                    # Only default version of non-hidden forms
                                                    if presentInEventDefinition["@IsDefaultVersion"] == "Yes" and presentInEventDefinition["@HideCRF"] == "No":
                                                        crf = Crf()
                                                        crf.oid = fd["@OID"]
                                                        event.addCrf(crf)

                                                # Collect references to ItemGroups in any case
                                                igRef = fd["ItemGroupRef"]
                                                if type(igRef) is list:
                                                    for igr in igRef:
                                                        itemGroupOids.append(igr["@ItemGroupOID"])
                                                elif type (igRef) is dict:
                                                    igr = igRef
                                                    itemGroupOids.append(igr["@ItemGroupOID"])

                                elif type(formDefinition) is dict:
                                    fd = formDefinition
                                    if fd["@OID"] in eventFormOids:
                                        if not event.hasScheduledCrf(fd["@OID"]):

                                            presentInEventDefinition = fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]

                                            # Form used in multiple Events
                                            if type(presentInEventDefinition) is list:
                                                for pied in presentInEventDefinition:
                                                    # Only default version of non-hidden forms
                                                    if pied["@IsDefaultVersion"] == "Yes" and pied["@HideCRF"] == "No":
                                                        # Only the form that belong to the current event
                                                        if pied["@StudyEventOID"] == event.eventDefinitionOID:
                                                            crf = Crf()
                                                            crf.oid = fd["@OID"]
                                                            event.addCrf(crf)
                                                            break

                                            # Form used in one Event
                                            elif type(presentInEventDefinition) is dict:
                                                # Only default version of non-hidden forms
                                                if presentInEventDefinition["@IsDefaultVersion"] == "Yes" and presentInEventDefinition["@HideCRF"] == "No":
                                                    crf = Crf()
                                                    crf.oid = fd["@OID"]
                                                    event.addCrf(crf)

                                            # Collect references to ItemGroups in any case
                                            igRef = fd["ItemGroupRef"]
                                            if type(igRef) is list:
                                                for igr in igRef:
                                                    itemGroupOids.append(igr["@ItemGroupOID"])
                                            elif type (igRef) is dict:
                                                igr = igRef
                                                itemGroupOids.append(igr["@ItemGroupOID"])

                                # Discover items base on their refOIDs
                                itemOids = []
                                itemGroupDefinition = r.json()["Study"]["MetaDataVersion"]["ItemGroupDef"]
                                if type(itemGroupDefinition) is list:
                                    for igd in itemGroupDefinition:
                                        if igd["@OID"] in itemGroupOids:

                                            groupPresentInForm = igd["OpenClinica:ItemGroupDetails"]["OpenClinica:PresentInForm"]
                                            if type(groupPresentInForm) is list:
                                                for gpif in groupPresentInForm:

                                                    crf = event.getCrf(
                                                        gpif["@FormOID"]
                                                    )

                                                    group = ItemGroup()
                                                    group.oid = igd["@OID"]
                                                    group.name = igd["@Name"]

                                                    iRef = igd["ItemRef"]
                                                    if type(iRef) is list:
                                                        for ir in iRef:
                                                            item = Item()
                                                            item.oid = ir["@ItemOID"]
                                                            group.addItem(item)
                                                            itemOids.append(ir["@ItemOID"])
                                                    elif type(iRef) is dict:
                                                        ir = iRef
                                                        item = Item()
                                                        item.oid = ir["@ItemOID"]
                                                        group.addItem(item)
                                                        itemOids.append(ir["@ItemOID"])

                                                    if crf:
                                                        crf.addItemGroup(group)

                                            elif type(groupPresentInForm) is dict:
                                                crf = event.getCrf(
                                                    groupPresentInForm["@FormOID"]
                                                )

                                                group = ItemGroup()
                                                group.oid = igd["@OID"]
                                                group.name = igd["@Name"]

                                                iRef = igd["ItemRef"]
                                                if type(iRef) is list:
                                                    for ir in iRef:
                                                        item = Item()
                                                        item.oid = ir["@ItemOID"]
                                                        group.addItem(item)
                                                        itemOids.append(ir["@ItemOID"])
                                                elif type(iRef) is dict:
                                                    ir = iRef
                                                    item = Item()
                                                    item.oid = ir["@ItemOID"]
                                                    group.addItem(item)
                                                    itemOids.append(ir["@ItemOID"])

                                                if crf:
                                                    crf.addItemGroup(group)

                                elif type(itemGroupDefinition) is dict:
                                    igd = itemGroupDefinition                                    
                                    if igd["@OID"] in itemGroupOids:
                                        
                                        groupPresentInForm = igd["OpenClinica:ItemGroupDetails"]["OpenClinica:PresentInForm"]
                                        if type(groupPresentInForm) is list:
                                            for gpif in groupPresentInForm:
                                                crf = event.getCrf(
                                                    gpif["@FormOID"]
                                                )

                                                group = ItemGroup()
                                                group.oid = igd["@OID"]
                                                group.name = igd["@Name"]

                                                iRef = igd["ItemRef"]
                                                if type(iRef) is list:
                                                    for ir in iRef:
                                                        item = Item()
                                                        item.oid = ir["@ItemOID"]
                                                        group.addItem(item)
                                                        itemOids.append(ir["@ItemOID"])
                                                elif type(iRef) is dict:
                                                    ir = iRef
                                                    item = Item()
                                                    item.oid = ir["@ItemOID"]
                                                    group.addItem(item)
                                                    itemOids.append(ir["@ItemOID"])

                                                if crf:
                                                    crf.addItemGroup(group)
                                            
                                        elif type(groupPresentInForm) is dict:
                                            crf = event.getCrf(
                                                groupPresentInForm["@FormOID"]
                                            )

                                            group = ItemGroup()
                                            group.oid = igd["@OID"]
                                            group.name = igd["@Name"]

                                            iRef = igd["ItemRef"]
                                            if type(iRef) is list:
                                                for ir in iRef:
                                                    item = Item()
                                                    item.oid = ir["@ItemOID"]
                                                    group.addItem(item)
                                                    itemOids.append(ir["@ItemOID"])
                                            elif type(iRef) is dict:
                                                ir = iRef
                                                item = Item()
                                                item.oid = ir["@ItemOID"]
                                                group.addItem(item)
                                                itemOids.append(ir["@ItemOID"])

                                            if crf:
                                                crf.addItemGroup(group)

                                # Setup items for CRF in event
                                itemDefinition = r.json()["Study"]["MetaDataVersion"]["ItemDef"]
                                if type(itemDefinition) is list:
                                    for itemDef in itemDefinition:
                                        if itemDef["@OID"] in itemOids:
                                            crf = event.getCrf(itemDef["@OpenClinica:FormOIDs"])

                                            item = Item()
                                            item.oid = itemDef["@OID"]
                                            item.name = itemDef["@Name"]
                                            item.dataType = itemDef["@DataType"]
                                            item.description = itemDef["@Comment"]
                                            
                                            if crf:
                                                gr = crf.findGroupForItem(item.oid)
                                                item.itemGroupOid = gr.oid

                                                crf.items.append(item)

                                elif type(itemDefinition) is dict:
                                    itemDef = itemDefinition
                                    if itemDef["@OID"] in itemOids:
                                        crf = event.getCrf(itemDef["@OpenClinica:FormOIDs"])

                                        item = Item()
                                        item.oid = itemDef["@OID"]
                                        item.name = itemDef["@Name"]
                                        item.dataType = itemDef["@DataType"]
                                        item.description = itemDef["@Comment"]
                                        
                                        if crf:
                                            gr = crf.findGroupForItem(item.oid)
                                            item.itemGroupOid = gr.oid

                                            crf.items.append(item)

                                result.studyEventData.append(event)
                        
                        # Only one event reported
                        elif type(eventData) is dict:
                            ed = eventData

                            event = Event()
                            event.eventDefinitionOID = ed["@StudyEventOID"]
                            event.status = ed["@OpenClinica:Status"]
                            dateString = ed["@OpenClinica:StartDate"]

                            format = ""
                            # Is it only date or datetime (in json the date format looks like this)
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

                                            presentInEventDefinition = fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]

                                            # Form used in multiple Events
                                            if type(presentInEventDefinition) is list:
                                                for pied in presentInEventDefinition:
                                                    # Only default version of non-hidden forms
                                                    if pied["@IsDefaultVersion"] == "Yes" and pied["@HideCRF"] == "No":
                                                        # Only the form that belong to the current event
                                                        if pied["@StudyEventOID"] == event.eventDefinitionOID:
                                                            crf = Crf()
                                                            crf.oid = fd["@OID"]
                                                            event.addCrf(crf)
                                                            break

                                            # Form used in one Event
                                            elif type(presentInEventDefinition) is dict:
                                                # Only default version of non-hidden forms
                                                if presentInEventDefinition["@IsDefaultVersion"] == "Yes" and presentInEventDefinition["@HideCRF"] == "No":
                                                    crf = Crf()
                                                    crf.oid = fd["@OID"]
                                                    event.addCrf(crf)

                            elif type(formDefinition) is dict:
                                fd = formDefinition
                                if fd["@OID"] in eventFormOids:
                                    if not event.hasScheduledCrf(fd["@OID"]):

                                        presentInEventDefinition = fd["OpenClinica:FormDetails"]["OpenClinica:PresentInEventDefinition"]

                                        # Form used in multiple Events
                                        if type(presentInEventDefinition) is list:
                                            for pied in presentInEventDefinition:
                                                # Only default version of non-hidden forms
                                                if pied["@IsDefaultVersion"] == "Yes" and pied["@HideCRF"] == "No":
                                                    # Only the form that belong to the current event
                                                    if pied["@StudyEventOID"] == event.eventDefinitionOID:
                                                        crf = Crf()
                                                        crf.oid = fd["@OID"]
                                                        event.addCrf(crf)
                                                        break

                                        # Form used in one Event
                                        elif type(presentInEventDefinition) is dict:
                                            # Only default version of non-hidden forms
                                            if presentInEventDefinition["@IsDefaultVersion"] == "Yes" and presentInEventDefinition["@HideCRF"] == "No":
                                                crf = Crf()
                                                crf.oid = fd["@OID"]
                                                event.addCrf(crf)

                            result.studyEventData.append(event)

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), result)
            return None
        else:
            return result

########  ########  #### ##     ##    ###    ######## ######## 
##     ## ##     ##  ##  ##     ##   ## ##      ##    ##       
##     ## ##     ##  ##  ##     ##  ##   ##     ##    ##       
########  ########   ##  ##     ## ##     ##    ##    ######   
##        ##   ##    ##   ##   ##  #########    ##    ##       
##        ##    ##   ##    ## ##   ##     ##    ##    ##       
##        ##     ## ####    ###    ##     ##    ##    ########   


    def _ocRequest(self, ocUrl, method):
        """Generic OpenClinica (RESTfull URL) GET request
        """
         # xml, html
        dataFormat = "json"

        s = requests.Session()
        loginCredentials = {"j_username": self._userDetails.username.lower(), "j_password": self._userDetails.clearpass}

        auth = None
        if self._proxyAuthEnabled:
            auth = HTTPBasicAuth(self._proxyAuthLogin, self._proxyAuthPassword)
            self._logger.info("Connecting with authentication: " + str(self._proxyAuthLogin))

        # Ensure that URL ends with /
        if not ocUrl.endswith("/"):
            ocUrl += "/"

        # Application proxy enabled
        if self._proxyEnabled:
            if self._noProxy != "" and self._noProxy is not whitespace and self._noProxy in "https://" + self.__ip:
                self._logger.info("Connecting without proxy because of no proxy: " + self._noProxy)
                r = s.post(
                    ocUrl + "j_spring_security_check",
                    loginCredentials,
                    auth=auth,
                    verify=False,
                    proxies={}
                )
                r = s.get(
                    ocUrl + "rest/clinicaldata/" + dataFormat + "/view/" + method,
                    auth=auth,
                    verify=False,
                    proxies={}
                )
            else:
                proxies = {"http": "http://" + self._proxyHost + ":" + self._proxyPort, "https": "https://" + self._proxyHost + ":" + self._proxyPort}
                self._logger.info("Connecting with application defined proxy: " + str(proxies))
                r = s.post(
                    ocUrl + "j_spring_security_check",
                    loginCredentials,
                    auth=auth,
                    verify=False,
                    proxies=proxies
                )
                r = s.get(
                    ocUrl + "rest/clinicaldata/" + dataFormat + "/view/" + method,
                    auth=auth,
                    verify=False,
                    proxies=proxies
                )
        # Use system proxy
        else:
            proxies = requests.utils.get_environ_proxies("https://" + self._ip)
            
            # TODO: disabling proxy for now
            proxies = None
            
            self._logger.info("Using system proxy variables (no proxy applied): " + str(proxies))
            r = s.post(
                ocUrl + "j_spring_security_check",
                loginCredentials,
                auth=auth,
                verify=False,
                proxies=proxies
            )
            r = s.get(
                ocUrl + "rest/clinicaldata/" + dataFormat + "/view/" + method,
                auth=auth,
                verify=False,
                proxies=proxies
            )

        return r        