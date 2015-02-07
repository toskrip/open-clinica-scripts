class CodeList:
    """CodeList is the representation for list data type

    It is possible to encode values into enumeration. When the data for import
    is created, we should check if input data conform the decoded values in
    code list. Basically check if input data is provided in proper normalised
    format
    """
    def __init__(self, oid, name, dataType):
        """Constructor
        """
        self.oid = oid
        self.name = name
        self.dataType = dataType

        self.listItems = []