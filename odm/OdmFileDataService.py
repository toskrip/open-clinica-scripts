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

from domain.CodeList import CodeList
from domain.CodeListItem import CodeListItem
from domain.EventDefinitionCrf import EventDefinitionCrf
from domain.ExportMapping import ExportMapping
from domain.Item import Item
from domain.Study import Study
from domain.StudyEventDefinition import StudyEventDefinition


# Domain
# Preffer C accelerated version of ElementTree for XML parsing
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########

# Namespace maps for reading of XML
nsmaps = { 'odm': 'http://www.cdisc.org/ns/odm/v1.3', 'cdisc' : 'http://www.cdisc.org/ns/odm/v1.3', 'OpenClinica' : 'http://www.openclinica.org/ns/odm_ext_v130/v3.1' }
# ("xsl", "http://www.w3.org/1999/XSL/Transform")
# ("beans", "http://openclinica.org/ws/beans")
# ("studysubject", "http://openclinica.org/ws/studySubject/v1")
# ("OpenClinica", "http://www.openclinica.org/ns/odm_ext_v130/v3.1")

# TODO: theoretically I can use xslt to transform xml metadata into import xml
# TODO: I should check if the loaded XML data conform XML schema for ODM
class OdmFileDataService():
    """File data service dedicated to work with XML files according to ODM schema
    """
    def __init__(self, logger=None):
        """Constructor

        """
        # Logger
        self.logger = logger or logging.getLogger(__name__)

        # Init members
        self.filename = ""

        # Header columns are holding the names of data elements
        self.headers = []

        # This is mandatory rule for naming DICOM Patient ID field in eCRF within RadPlanBio
        self.ocPatientIdItemName = "ITM_PATIENT_ID"
        # This is mandatory rule for naming DICOM Study Instance UID field in eCRF within RadPlanBio
        self.ocStudyUidItemName = "ITM_STUDY_UID"

##     ## ######## ######## ##     ##  #######  ########   ######
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ##
#### #### ##          ##    ##     ## ##     ## ##     ## ##
## ### ## ######      ##    ######### ##     ## ##     ##  ######
##     ## ##          ##    ##     ## ##     ## ##     ##       ##
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ##
##     ## ########    ##    ##     ##  #######  ########   ######

    def isFileLoaded(self):
        """Determine whether the filename is provided to the service
        """
        return self.filename != ""

    def setFilename(self, filename):
        """Setup data filename for the service
        """
        if self.filename != filename:
            self.filename = filename

    def getFilename(self):
        """Get the name of the data fila
        """
        return str(self.filename)

    def loadHeaders(self):
        """Load items headers from xml metadata

        """
        if (self.isFileLoaded) :
            documentTree = ET.ElementTree(file=self.filename)

            for element in documentTree.iterfind('.//odm:ItemDef', namespaces=nsmaps):
                self.headers.append(element.attrib['Comment'])

    def loadStudy(self):
        """Extract Study domain object according to ODM from metadata XML
        """
        study = None

        # Check if file path is setup
        if (self.isFileLoaded) :
            documentTree = ET.ElementTree(file=self.filename)

            # Locate Study data in XML file via XPath
            for element in documentTree.iterfind('.//odm:Study', namespaces=nsmaps):
                study = Study()
                study.setOid(element.attrib['OID'])

                for studyName in documentTree.iterfind('.//odm:Study[@OID="' + study.oid() + '"]/odm:GlobalVariables/odm:StudyName', namespaces=nsmaps):
                    study.setName(studyName.text)

                for studyDescription in documentTree.iterfind('.//odm:Study[@OID="' + study.oid() + '"]/odm:GlobalVariables/odm:StudyDescription', namespaces=nsmaps):
                    study.setDescription(studyDescription.text)

                # # In case I need this information later
                # for studyProtocolName in documentTree.iterfind('.//odm:Study[@OID="' + study.oid() + '"]/odm:GlobalVariables/odm:ProtocolName', namespaces=nsmaps):
                #     print studyProtocolName.text

        # The resulting study element
        return study

    def loadStudyEvents(self):
        """Extract a list of Study Event domain objects according to ODM from metadata XML
        """
        studyEvents = []

        # Check if file path is setup
        if (self.isFileLoaded):
            documentTree = ET.ElementTree(file=self.filename)

            # First obtain list of references (OIDs) to study events defined in ODM -> Study -> MetaDataVersion -> Protocol
            studyEventRefs = []

            for studyEventRef in documentTree.iterfind('.//odm:StudyEventRef', namespaces=nsmaps):
                studyEventRefs.append(studyEventRef.attrib['StudyEventOID'])

                # # In case I need this information later
                # print studyEventRef.attrib['Mandatory']
                # print studyEventRef.attrib['OrderNumber']

            # Now for each study event reference find study event definition
            for eventRef in studyEventRefs:
                for element in documentTree.iterfind('.//odm:StudyEventDef[@OID="' + eventRef + '"]', namespaces=nsmaps):
                    studyEvent = StudyEventDefinition()

                    studyEvent.setOid(element.attrib['OID'])
                    studyEvent.setName(element.attrib['Name'])
                    studyEvent.setRepeating(element.attrib['Repeating'])
                    studyEvent.setType(element.attrib['Type'])

                    studyEvents.append(studyEvent)

        # Return resulting study event defintion elements
        return studyEvents

    def loadEventCrfs(self, studyEventDef):
        """Extract a list of EventDefinitionCrf domain objects according to ODM from metadata XML
        """
        eventCrfs = []

        # Check if file path is setup
        if (self.isFileLoaded):
            documentTree = ET.ElementTree(file=self.filename)

            # First collect ForRef elements as a childrens of selected Study Event Definition
            formRefs = []

            for formRef in  documentTree.iterfind('.//odm:StudyEventDef[@OID="' + studyEventDef.oid() + '"]/odm:FormRef', namespaces=nsmaps):
                formRefs.append(formRef.attrib['FormOID'])

                # # If this information needed later
                # formRef.attrib['Mandatory']

            # Now search FormDefs according to FormRefs
            for formRef in formRefs:
                for form in documentTree.iterfind('.//odm:FormDef[@OID="' + formRef + '"]', namespaces=nsmaps):
                    eventCrf = EventDefinitionCrf()

                    eventCrf.setOid(form.attrib['OID'])
                    eventCrf.setName(form.attrib['Name'])
                    eventCrf.setRepeating(form.attrib['Repeating'])

                    eventCrfs.append(eventCrf)

        # Return resulting study event crf forms
        return eventCrfs

    def loadCrfItem(self, formOid, itemOid, metadata):
        """Load CRF item details from ODM metadata
        """
        item = None

        self.logger.info("CRF form OID: " +  formOid)
        self.logger.info("CRF item OID: " + itemOid)

        # Check if file path is setup
        if (metadata):
            documentTree = ET.ElementTree((ET.fromstring(str(metadata))))

            # Locate ItemDefs data in XML file via XPath
            for itemElement in documentTree.iterfind('.//odm:ItemDef[@OID="' + itemOid + '"]', namespaces=nsmaps):
                # Check FormOID, normally I would do it in XPath but python does not support contaions wildcard
                if itemElement.attrib["{http://www.openclinica.org/ns/odm_ext_v130/v3.1}FormOIDs"].find(formOid) != -1:
                    item = Item()
                    item.oid = itemElement.attrib['OID']
                    item.name = itemElement.attrib['Name']
                    item.description = itemElement.attrib['Comment']
                    item.dataType = itemElement.attrib['DataType']

                    for itemDetails in itemElement:
                        if (str(itemDetails.tag)).strip() == "{http://www.openclinica.org/ns/odm_ext_v130/v3.1}ItemDetails":
                            for detailsElement in itemDetails:
                                if (str(detailsElement.tag)).strip() == "{http://www.openclinica.org/ns/odm_ext_v130/v3.1}ItemPresentInForm":
                                    for presentForm in detailsElement:
                                        if (str(presentForm.tag)).strip() == "{http://www.openclinica.org/ns/odm_ext_v130/v3.1}LeftItemText":
                                            item.label = presentForm.text

        # Return resulting CRT item
        return item

    def loadExportMapping(self, eventCrf):
        """
        """
        exportMapping = []

        if (self.isFileLoaded) :
            documentTree = ET.ElementTree(file=self.filename)

            # First obtain item group refs for provided crf
            itemGroupRefs = []

            for groupRef in  documentTree.iterfind('.//odm:FormDef[@OID="' + eventCrf.oid() + '"]/odm:ItemGroupRef', namespaces=nsmaps):
                itemGroupRefs.append(groupRef.attrib['ItemGroupOID'])

            # Now accumulate Item Refs for all groups
            itemRefs = []

            for groupRef in itemGroupRefs:
                for itemRef in documentTree.iterfind('.//odm:ItemGroupDef[@OID="' + groupRef + '"]/odm:ItemRef', namespaces=nsmaps):
                    itemRefs.append(itemRef.attrib['ItemOID'])

            # Finally find all ItemDefs according to ItemRef
            for itemRef in itemRefs:
                for element in documentTree.iterfind('.//odm:ItemDef[@OID="' + itemRef + '"]', namespaces=nsmaps):
                    exportMap = ExportMapping(element.attrib['Comment'])
                    exportMap.name = element.attrib['Name']
                    exportMap.metadataOid = element.attrib['OID']
                    exportMap.dataType = element.attrib['DataType']

                    # for text, integer and float get also length
                    if exportMap.dataType == "text" or exportMap.dataType == "integer" or exportMap.dataType == "float":
                        exportMap.length = int(element.attrib['Length'])

                    # Determine if the Item values are encoded via codeList
                    codeListRef = documentTree.find('.//odm:ItemDef[@OID="' + exportMap.metadataOid + '"]/cdisc:CodeListRef', namespaces=nsmaps)

                    if codeListRef is not None:
                        # Get the CodeListOID for identification of CodeList
                        clr = codeListRef.attrib['CodeListOID']
                        codeListElement = documentTree.find('.//cdisc:CodeList[@OID="' + clr + '"]', namespaces=nsmaps)

                        # Create CodeList
                        oid = codeListElement.attrib['OID']
                        name = codeListElement.attrib['Name']
                        dataType = codeListElement.attrib['DataType']
                        codeList = CodeList(oid, name, dataType)

                        # Looking for code list items
                        if codeListElement is not None:
                            codeListItems = []
                            for codeListItemElement in documentTree.iterfind('.//cdisc:CodeList[@OID="' + clr + '"]/cdisc:CodeListItem', namespaces=nsmaps):
                                codedValue = codeListItemElement.attrib['CodedValue']
                                decodedValue = ""
                                codeListItem = CodeListItem(codedValue, decodedValue)
                                codeListItems.append(codeListItem)

                            i = 0;
                            for textElement in documentTree.iterfind('.//cdisc:CodeList[@OID="' + clr + '"]/cdisc:CodeListItem/cdisc:Decode/cdisc:TranslatedText', namespaces=nsmaps):
                                decodedValue = textElement.text
                                codeListItems[i].decodedValue = decodedValue
                                i = i + 1

                            codeList.listItems = codeListItems
                            exportMap.codeList = codeList

                    exportMapping.append(exportMap)

            # Extend them about infromation from ItemRef elements (mandatory fields)
            for exportMapElement in exportMapping:
                for element in documentTree.iterfind('.//cdisc:ItemRef[@ItemOID="' + exportMapElement.metadataOid + '"]', namespaces=nsmaps):
                    if element.attrib['Mandatory'] == "Yes":
                        exportMapElement.mandatory = True
                    elif element.attrib['Mandatory'] == "No":
                        exportMapElement.mandatory = False

        return exportMapping

    def printData(self):
        """Print the content of file to the console
        """
        if (self.isFileLoaded) :
            documentTree = ET.ElementTree(file=self.filename)

            for element in documentTree.iter():
                print element.tag, element.attrib

    def generateOdmXmlForStudy(self, studyOid, subject, event, reportText, crfDicomPatientField, crfDicomStudyField, crfSRTextField=None):
        """Create the XML ODM structured data string for import
        """
        odm = ET.Element("ODM")

        # Study - Study OID
        clinicalData = ET.SubElement(odm, "ClinicalData")
        clinicalData.set("StudyOID", studyOid)
        clinicalData.set("MetaDataVersionOID", 'v1.0.0')

        # Subject - Study Subject ID
        subjectData = ET.SubElement(clinicalData, "SubjectData")
        subjectData.set("SubjectKey", subject.oid)

        # Event
        studyEventData = ET.SubElement(subjectData, "StudyEventData")
        studyEventData.set("StudyEventOID", event.eventDefinitionOID)
        studyEventData.set("StudyEventRepeatKey", event.studyEventRepeatKey)

        # CRF form
        formData = ET.SubElement(studyEventData, "FormData")
        formData.set("FormOID", crfDicomStudyField.formOid)

        # Item group
        itemGroupData = ET.SubElement(formData, "ItemGroupData")
        itemGroupData.set("ItemGroupOID", crfDicomStudyField.groupOid)
        itemGroupData.set("TransactionType", "Insert")

        # DICOM Patient ID - PID
        itemData = ET.SubElement(itemGroupData, "ItemData")
        itemData.set("ItemOID", crfDicomPatientField.crfitemoid)
        itemData.set("Value", subject.subject.uniqueIdentifier)

        # DICOM Study UID
        itemData = ET.SubElement(itemGroupData, "ItemData")
        itemData.set("ItemOID", crfDicomStudyField.oid)
        itemData.set("Value", crfDicomStudyField.value)

        # DICOM SR text
        if crfSRTextField:
            itemData = ET.SubElement(itemGroupData, "ItemData")
            itemData.set("ItemOID", crfSRTextField.crfitemoid)
            itemData.set("Value", reportText)

        documentTree = ET.ElementTree(odm)

        xmlstring = ET.tostring(odm, encoding="UTF-8")
        xmlstring = xmlstring.replace("<?xml version='1.0' encoding='UTF-8'?>", "")

        return xmlstring

    def generateOdmXmlForStudyFromMetadata(self, studyOid, subject, studyEventDefinition, studyEventCrf, itemValues, metadata):
        """Obsolate: DO NOT USE!
        """
        odm = ET.Element('ODM')

        clinicalData = ET.SubElement(odm, 'ClinicalData')
        clinicalData.set('StudyOID', studyOid)
        clinicalData.set('MetaDataVersionOID', 'v1.0.0')

        fileSubjectCounter = 0

        subjectData = ET.SubElement(clinicalData, 'SubjectData')
        subjectData.set('SubjectKey', subject.oid)

        studyEventData = ET.SubElement(subjectData, 'StudyEventData')
        studyEventData.set('StudyEventOID', studyEventDefinition.oid())

        formData = ET.SubElement(studyEventData, 'FormData')
        formData.set('FormOID', studyEventCrf.defaultCrfVersion().oid())

        items = []
        for ivalue in itemValues:
            item = Item()
            item.value = ivalue
            items.append(item)

        patientIdItemOid = self.getItemOidFromMetadata(metadata, studyEventCrf.defaultCrfVersion().oid(), self.ocPatientIdItemName)
        studyUidItemOid = self.getItemOidFromMetadata(metadata, studyEventCrf.defaultCrfVersion().oid(), self.ocStudyUidItemName)

        items[0].oid = patientIdItemOid
        items[1].oid = studyUidItemOid

        itemGroupPatientOid = self.getItemGroupOidFromMetadata(metadata, patientIdItemOid)
        itemGroupStudyOid = self.getItemGroupOidFromMetadata(metadata, studyUidItemOid)

        # Both should be in the same group
        if (itemGroupPatientOid == itemGroupStudyOid):

            itemGroupData = ET.SubElement(formData, 'ItemGroupData')
            itemGroupData.set('ItemGroupOID', itemGroupStudyOid)
            itemGroupData.set('TransactionType', 'Insert')

            for item in items:
                itemData = ET.SubElement(itemGroupData, 'ItemData')
                itemData.set('ItemOID', item.oid)
                itemData.set('Value', item.value)

        xmlstring = ET.tostring(odm, encoding="UTF-8")
        xmlstring = xmlstring.replace("<?xml version='1.0' encoding='UTF-8'?>", "")

        return xmlstring

    def getItemOidFromMetadata(self, metadata, formOid, itemName):
        """Get item OID from metadata when form and itemName are known

        Param metadata study metadata
        Param formOid specify which form to search in metadata
        Param itemName specify which item to search
        Return string OID value of specified itemName from metadata or None
        """
        documentTree = ET.ElementTree((ET.fromstring(str(metadata))))

        itemOids = []

        # Locate ItemDefs data in XML file via XPath
        for item in documentTree.iterfind('.//odm:ItemDef[@OpenClinica:FormOIDs="' + formOid + '"]' + '[@Name="' + itemName + '"]', namespaces=nsmaps):
            itemOids.append(item.attrib['OID'])

        if len(itemOids) == 1:
            return itemOids[0]
        else:
            return None

    def getItemGroupOidFromMetadata(self, metadata, itemOid):
        """
        Param metadata study metadata
        Param itemOid specifies the oid of item which group we are searching
        Retrun string OID value of found ItemGroupDef or None
        """
        documentTree = ET.ElementTree((ET.fromstring(str(metadata))))

        itemGroupOids = []

        groupFound = False
        # Locate ItemGroupDefs data in XML file via XPath
        for group in documentTree.iterfind('.//odm:ItemGroupDef', namespaces=nsmaps):
            for element in group:
                if (str(element.tag)).strip() == "{http://www.cdisc.org/ns/odm/v1.3}ItemRef":
                    if element.attrib['ItemOID'] == itemOid:
                        itemGroupOids.append(group.attrib['OID'])
                        groupFound = True
                        break;

            if groupFound:
                break

        if len(itemGroupOids) == 1:
            return itemGroupOids[0]
        else:
            return None

    def getRadPlanBioDicomItemNamesFromMetadata():
        pass