from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtCore import Qt, QSize

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen, setThemeColor, NavigationBarPushButton, toggleTheme, setTheme, darkdetect, Theme
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition

from .home_interface import HomeInterface
from .configs_interface import ConfigInterface
# from .setting_interface import SettingInterface
from .setting_interface import SettingInterface


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        setTheme(Theme.LIGHT)
        self.setMicaEffectEnabled(False)

        self.initWindow()
        self.subMainWindow = QWidget(self)
        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.configInterface =ConfigInterface(self)
        self.settingInterface = SettingInterface(self)
        self.initNavigation()
        self.splashScreen.finish()

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Trang chủ'))
        self.addSubInterface(self.configInterface, FIF.CONNECT, self.tr('Configs'))
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Setting'), position=NavigationItemPosition.BOTTOM)

    def toggleTheme(self):
        toggleTheme()

    def initWindow(self):
        # 禁用最大化
        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

        self.resize(1500, 800)
        # self.setWindowIcon(QIcon(r'assets\logo\March7th.ico'))
        self.setWindowTitle("IOS Multil Control v.08.11")
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        


