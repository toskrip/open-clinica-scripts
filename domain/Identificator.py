
class Identificator():
    """Represents ID object returned from Mainzelliste pseudonymisation

    """

    def __init__(self, idString, idType, isTentative):
        """Constructor

        Create Patient Identificator
        """
        # Initialise members
        self.idString = idString
        self.idType = idType
        self.isTentative = isTentative


    def __str__(self):
        """ToString

        Print the class itself
        """
        print "Patient ID:\n idString: " + self.idString + "\nidType: " + self.idType + "\nisTentative: " + self.isTentative

