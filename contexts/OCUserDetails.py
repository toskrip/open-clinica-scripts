#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Singleton
from utils.SingletonType import SingletonType

class OCUserDetails(object):
    """Logged user details
    """

    __metaclass__ = SingletonType

    def __init__(self):
        """Default Constructor
        """
        self.username = ""
        self.passwordHash = ""
        self.connected = False