#----------------------------------------------------------------------
#------------------------------ Modules -------------------------------
# Date
from datetime import datetime


#----------------------------------------------------------------------
class Person():
    """Representation of a person
    Subject enrolled into a study can be also person, in that case
    it has attributes as firstname, surname, etc.
    """

    #-------------------------------------------------------------------
    #-------------------- Constuctors ----------------------------------

    def __init__(self):
        """Constructor
        """
        self.__firstname = ""
        self.__surename = ""
        self.__birthdate = None

        self.__birthname = ""
        self.__city = ""
        self.__zipcode = ""

    #-------------------------------------------------------------------
    #-------------------- Properties -----------------------------------

    @property
    def firstname(self):
        """Firstname Getter
        """
        return self.__firstname


    @firstname.setter
    def firstname(self, firstnameValue):
        """PID Setter
        """
        if self.__firstname != firstnameValue:
            self.__firstname = firstnameValue


    @property
    def surename(self):
        """Firstname Getter
        """
        return self.__firstname


    @surename.setter
    def surename(self, surenameValue):
        """PID Setter
        """
        if self.__surename != surenameValue:
            self.__surename = surenameValue


    @property
    def birthdate(self):
        """Birthdate Getter
        """
        return self.__birthdate


    @birthdate.setter
    def birthdate(self, birthdateValue):
        """Birthdate Setter
        """
        if self.__birthdate != birthdateValue:
            self.__birthdate = birthdateValue


    @property
    def birthname(self):
        """Birthname Getter
        """
        if (self.__birthname == ''):
            return self.__surename
        else:
            return self.__birthname


    @birthname.setter
    def birthname(self, birthnameValue):
        """Birthname Setter
        """
        if self.__birthname != birthnameValue:
            self.__birthname = birthnameValue


    @property
    def city(self):
        """City Getter
        """
        return self.__city


    @city.setter
    def city(self, cityValue):
        """City Setter
        """
        if self.__city != cityValue:
            self.__city = cityValue


    @property
    def zipcode(self):
        """ZIP code Getter
        """
        return self.__zipcode


    @zipcode.setter
    def zipcode(self, zipcodeValue):
        """ZIP code Setter
        """
        if self.__zipcode != zipcodeValue:
            self.__zipcode = zipcodeValue