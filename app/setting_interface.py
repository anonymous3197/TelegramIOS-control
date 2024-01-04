# coding:utf-8
from qfluentwidgets import (SettingCardGroup, PushSettingCard, ScrollArea, InfoBar, PrimaryPushSettingCard, Pivot, qrouter)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QStackedWidget
from PyQt5.QtGui import QDesktopServices
import subprocess


class SettingInterface(ScrollArea):
    """ Setting interface """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.stackedWidget = QStackedWidget(self)

        # setting label
        self.settingLabel = QLabel(self.tr("设置"), self)
        self.__initWidget()
    def __initWidget(self):
            self.resize(1000, 800)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setViewportMargins(0, 80, 0, 20)
            self.setWidget(self.scrollWidget)
            self.setWidgetResizable(True)
            self.setObjectName('settingInterface')
            # initialize style sheet
            self.scrollWidget.setObjectName('scrollWidget')
            self.settingLabel.setObjectName('settingLabel')

      