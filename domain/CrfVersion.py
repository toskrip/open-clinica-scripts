class CrfVersion():

    def __init__(self, oid, name):

        # Init members
        self.__oid = oid
        self.__name = name


    def oid(self):
        return self.__oid


    def name(self):
        return self.__name


    def atrSize(self):
        return 2

