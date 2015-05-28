class CrfVersion():

    def __init__(self, oid, name):

        # Init members
        self._oid = oid
        self._name = name


    @property
    def oid(self):
        return self._oid

    @property
    def name(self):
        return self._name

