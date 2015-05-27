#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# System
import sys

# PyQT
from PyQt4 import QtGui, QtCore, uic

# Contexts
from contexts.ConfigDetails import ConfigDetails

# Resource images for buttons
from gui import images_rc

# Application Dialogs
from gui.AboutDialog import AboutDialog

# GUI Messages
import gui.messages

# Application modules GUI
from gui.OcModule import OcModule

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

##      ## #### ##    ## ########   #######  ##      ## 
##  ##  ##  ##  ###   ## ##     ## ##     ## ##  ##  ## 
##  ##  ##  ##  ####  ## ##     ## ##     ## ##  ##  ## 
##  ##  ##  ##  ## ## ## ##     ## ##     ## ##  ##  ## 
##  ##  ##  ##  ##  #### ##     ## ##     ## ##  ##  ## 
##  ##  ##  ##  ##   ### ##     ## ##     ## ##  ##  ## 
 ###  ###  #### ##    ## ########   #######   ###  ### 

EXIT_CODE_RESTART = -123456789 # any value

class MainWindowUI(object):
    """Main Window UI defintion
    """

    def setupUi(self, MainWindow):
        """ Prepare complete GUI for application main window
        """
        # Main window size
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(ConfigDetails().width, ConfigDetails().height)

        appIconPath =":/images/rpb-icon.jpg"
        appIcon = QtGui.QIcon()
        appIcon.addPixmap(QtGui.QPixmap(appIconPath))
        MainWindow.setWindowIcon(appIcon)

        # Central widget is main window in this case
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # Prepare menu bar UI
        self._setupMenuBar(MainWindow)

        # Root layout manager for main window is stack panel
        rootLayout = QtGui.QVBoxLayout(self.centralwidget)

        # Prepare tool bar UI
        rootLayout.addLayout(self._setupToolBar())

        # Prepare main tab for modules UI
        rootLayout.addWidget(self._setupModulesTab())

        self._setupWelcomeModule()
        self._setupStatusBar(MainWindow)

        # Put defined central widget into ManWindow central widget
        self.retranslateUi(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Event handlers
        QtCore.QObject.connect(self, QtCore.SIGNAL("RESTARTREQUIRED"), self.restart)

##     ## ######## ##    ## ##     ## 
###   ### ##       ###   ## ##     ## 
#### #### ##       ####  ## ##     ## 
## ### ## ######   ## ## ## ##     ## 
##     ## ##       ##  #### ##     ## 
##     ## ##       ##   ### ##     ## 
##     ## ######## ##    ##  #######  

    def _setupMenuBar(self, MainWindow):
        """Create application menu bar
        """
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        
        restartAction = QtGui.QAction(QtGui.QIcon(), "&Restart", self)
        restartAction.setShortcut("Ctrl+R")
        restartAction.setStatusTip("Restart application")
        restartAction.triggered.connect(self.restart)

        exitAction = QtGui.QAction(QtGui.QIcon("exit.png"), "&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit application")
        exitAction.triggered.connect(self.quit)

        fileMenu = self.menuBar.addMenu("&File")
        fileMenu.addAction(restartAction)
        fileMenu.addAction(exitAction)
        
        ocAction = QtGui.QAction(QtGui.QIcon(), "&OC module", self)
        ocAction.setShortcut("Ctrl+O")
        ocAction.setStatusTip("Open OC browse module")
        ocAction.triggered.connect(self.loadOcModule)

        modulesMenu = self.menuBar.addMenu("&Modules")
        modulesMenu.addAction(ocAction)
        
        #-----------
        aboutAction = QtGui.QAction(QtGui.QIcon(), "&About", self)
        aboutAction.setShortcut("F1")
        aboutAction.setStatusTip("About application")
        aboutAction.triggered.connect(self.aboutPopup)

        helpMenu = self.menuBar.addMenu("&Help")
        helpMenu.addAction(aboutAction)
        #-----------
        MainWindow.setMenuBar(self.menuBar)

########  #######   #######  ##       ########     ###    ########  
   ##    ##     ## ##     ## ##       ##     ##   ## ##   ##     ## 
   ##    ##     ## ##     ## ##       ##     ##  ##   ##  ##     ## 
   ##    ##     ## ##     ## ##       ########  ##     ## ########  
   ##    ##     ## ##     ## ##       ##     ## ######### ##   ##   
   ##    ##     ## ##     ## ##       ##     ## ##     ## ##    ##  
   ##     #######   #######  ######## ########  ##     ## ##     ## 

    def _setupToolBar(self):
        """Create main window toolbar
        """
        toolBarButtonSize = 25

        modulesButtonsToolbar = QtGui.QGridLayout()

        # Module close button
        self.btnCloseModule = QtGui.QPushButton()
        self.btnCloseModule.setDisabled(True)
        self.btnCloseModule.setMaximumWidth(toolBarButtonSize)
        self.btnCloseModule.setMaximumHeight(toolBarButtonSize)
        self.btnCloseModule.clicked.connect(self.btnCloseModuleClicked)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.btnCloseModuleClicked)

        closeModuleIconPath =':/images/x-mark.png'
        closeIcon = QtGui.QIcon()
        closeIcon.addPixmap(QtGui.QPixmap(closeModuleIconPath));

        self.btnCloseModule.setIcon(closeIcon)
        self.btnCloseModule.setToolTip("Close module [Ctrl+W]")
        self.btnCloseModule.setIconSize(QtCore.QSize(toolBarButtonSize, toolBarButtonSize))

        space = QtGui.QSpacerItem(200, 25)

        # Add all to layout
        modulesButtonsToolbar.addItem(space, 1, 1, 1, 9)
        modulesButtonsToolbar.addWidget(self.btnCloseModule, 1, 10)

        return modulesButtonsToolbar

##     ##  #######  ########  ##     ## ##       ########  ######  
###   ### ##     ## ##     ## ##     ## ##       ##       ##    ## 
#### #### ##     ## ##     ## ##     ## ##       ##       ##       
## ### ## ##     ## ##     ## ##     ## ##       ######    ######  
##     ## ##     ## ##     ## ##     ## ##       ##             ## 
##     ## ##     ## ##     ## ##     ## ##       ##       ##    ## 
##     ##  #######  ########   #######  ######## ########  ###### 
    
    def _setupModulesTab(self):
        """Create welcome module selection module
        """
        # Main Modules tab widget
        self.tabModules = QtGui.QTabWidget()
        self.tabModules.setTabPosition(QtGui.QTabWidget.South)

        # Create module tabs
        tabWelcomeModule = QtGui.QWidget()

        # Add tabs to widget
        self.tabModules.addTab(tabWelcomeModule, "Welcome")

        # Tab modules layout
        self.layoutWelcomeModule = QtGui.QVBoxLayout(tabWelcomeModule)

        return self.tabModules

##      ## ######## ##        ######   #######  ##     ## ######## 
##  ##  ## ##       ##       ##    ## ##     ## ###   ### ##       
##  ##  ## ##       ##       ##       ##     ## #### #### ##       
##  ##  ## ######   ##       ##       ##     ## ## ### ## ######   
##  ##  ## ##       ##       ##       ##     ## ##     ## ##       
##  ##  ## ##       ##       ##    ## ##     ## ##     ## ##       
 ###  ###  ######## ########  ######   #######  ##     ## ######## 
 
    def _setupWelcomeModule(self):
        """Create welcome module for application module loading
        """
        # Grid layout
        welcomeGrid = QtGui.QGridLayout()
        self.layoutWelcomeModule.addLayout(welcomeGrid)

        moduleButtonWidth = 100
        moduleButtonHeight = 200
        moduleButtonIconSize = 200

        # Upload
        self.btnLoadOcModule = QtGui.QPushButton()
        self.btnLoadOcModule.setObjectName("LoadOcModule")
        self.btnLoadOcModule.setMinimumWidth(moduleButtonWidth/3)
        self.btnLoadOcModule.setMinimumHeight(moduleButtonHeight)
        self.btnLoadOcModule.clicked.connect(self.btnLoadModuleClicked)

        loadOcModuleIconPath = ":/images/localDicomUpload.png"
        loadOcIcon = QtGui.QIcon()
        loadOcIcon.addPixmap(QtGui.QPixmap(loadOcModuleIconPath));
        self.btnLoadOcModule.setIcon(loadOcIcon)
        self.btnLoadOcModule.setIconSize(QtCore.QSize(moduleButtonIconSize, moduleButtonIconSize))

        # Add to grid layout
        welcomeGrid.addWidget(self.btnLoadOcModule, 0, 0)

 ######  ########    ###    ######## ##     ##  ######  
##    ##    ##      ## ##      ##    ##     ## ##    ## 
##          ##     ##   ##     ##    ##     ## ##       
 ######     ##    ##     ##    ##    ##     ##  ######  
      ##    ##    #########    ##    ##     ##       ## 
##    ##    ##    ##     ##    ##    ##     ## ##    ## 
 ######     ##    ##     ##    ##     #######   ###### 

    def _setupStatusBar(self, MainWindow):
        """Create status bar
        """
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))

        MainWindow.setStatusBar(self.statusBar)

    def enableIndefiniteProgess(self):
        """Show indefinite progress right in status bar
        """
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setMaximumHeight(16)
        self.progressBar.setMaximumWidth(200)
        self.progressBar.setTextVisible(False)
        self.statusBar.addPermanentWidget(self.progressBar, 0)

        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)

    def disableIndefiniteProgess(self):
        """Hide indefinite progress from status bar
        """
        self.statusBar.removeWidget(self.progressBar);

##     ##    ###    ##    ## ########  ##       ######## ########   ######  
##     ##   ## ##   ###   ## ##     ## ##       ##       ##     ## ##    ## 
##     ##  ##   ##  ####  ## ##     ## ##       ##       ##     ## ##       
######### ##     ## ## ## ## ##     ## ##       ######   ########   ######  
##     ## ######### ##  #### ##     ## ##       ##       ##   ##         ## 
##     ## ##     ## ##   ### ##     ## ##       ##       ##    ##  ##    ## 
##     ## ##     ## ##    ## ########  ######## ######## ##     ##  ###### 

    def restart(self):
        """Restart event handler
        """
        QtGui.qApp.exit(EXIT_CODE_RESTART)

    def quit(self):
        """Quit (exit) event handler
        """
        reply = QtGui.QMessageBox.question(self, "Question", gui.messages.QUE_EXIT, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            QtGui.qApp.quit()

    def btnLoadModuleClicked(self):
        """ Load module handler
        """
        name = str(self.sender().objectName())
        self.btnCloseModule.setDisabled(False)

        if name == "LoadOcModule":
            self.loadOcModule()

    def loadOcModule(self):
        """Load OC data module
        """
        if self.connectToOpenClinica():
            self.tabOcLoadModule = QtGui.QWidget()
            self.tabModules.addTab(self.tabOcLoadModule, "Load OC")
            self.layoutOcModule = QtGui.QVBoxLayout(self.tabOcLoadModule)

            self.ocLoadModule = OcModule(self.tabOcLoadModule)
            self.layoutOcModule.addLayout(self.ocLoadModule.rootLayout)

            self.tabModules.setCurrentIndex(self.tabModules.count() - 1)

    def btnCloseModuleClicked(self):
        """Close module handler
        """
        # Currently selected tab module
        index = self.tabModules.currentIndex()

        # Always keep welcome tab module
        if (index != 0):
            self.tabModules.widget(index).deleteLater()
            self.tabModules.widget(index).close()
            self.tabModules.removeTab(index)
        
        if self.tabModules.count() == 1:
            self.btnCloseModule.setDisabled(True)

        self.tabModules.setCurrentIndex(0)
        self.tabModules.setTabEnabled(0, True)

    def aboutPopup(self):
        """Show about dialog
        """
        self.dialog = AboutDialog(self)
        self.dialog.exec_()

####    ##    #######  ##    ## 
 ##   ####   ##     ## ###   ## 
 ##     ##   ##     ## ####  ## 
 ##     ##    #######  ## ## ## 
 ##     ##   ##     ## ##  #### 
 ##     ##   ##     ## ##   ### 
####  ######  #######  ##    ##

    def retranslateUi(self, MainWindow):
        """
        """
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", ConfigDetails().name, None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadOcModule.setText(QtGui.QApplication.translate("MainWindow", "Load OpenClinica module", None, QtGui.QApplication.UnicodeUTF8))