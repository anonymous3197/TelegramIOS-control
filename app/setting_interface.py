#     Copyright 2023, MCSL Team, mailto:lxhtt@vip.qq.com
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
"""
Settings page.
"""
from .config import cfg
import netifaces as ni

from datetime import datetime

from PyQt5.QtCore import QSize, Qt, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
    QSpacerItem,
    QFrame,
    QAbstractScrollArea,
    QVBoxLayout,
    QApplication,
    QScrollArea
)
from qfluentwidgets import (
    SmoothScrollArea,
    SmoothScrollDelegate,
    BodyLabel,
    CardWidget,
    HyperlinkButton,
    PrimaryPushButton,
    StrongBodyLabel,
    TitleLabel,
    setTheme,
    CustomColorSettingCard,
    SwitchSettingCard,
    OptionsSettingCard,
    SettingCardGroup,
    ComboBoxSettingCard,
    PrimaryPushSettingCard,
    RangeSettingCard,
    MessageBox,
    InfoBarPosition,
    InfoBar,
    FluentIcon as FIF,
    setThemeColor,
)

class MySmoothScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.delegate = SmoothScrollDelegate(self, True)
        self.setFrameShape(QScrollArea.NoFrame)

class SettingInterface(QWidget):
    """设置页"""

    settingsChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsWidget")
        self.gridLayout_3 = QGridLayout(self)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem1, 0, 1, 1, 1)
        self.settingsSmoothScrollArea = SmoothScrollArea(self)
        self.settingsSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.settingsSmoothScrollArea.setFrameShadow(QFrame.Plain)
        self.settingsSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.settingsSmoothScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.settingsSmoothScrollArea.setWidgetResizable(True)
        self.settingsSmoothScrollArea.setObjectName("settingsSmoothScrollArea")
        self.settingsScrollAreaWidgetContents = QWidget()
        self.settingsScrollAreaWidgetContents.setGeometry(QRect(0, 0, 676, 532))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsScrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.settingsScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.settingsScrollAreaWidgetContents.setObjectName("settingsScrollAreaWidgetContents")
        self.verticalLayout = QVBoxLayout(self.settingsScrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.settingsSmoothScrollArea.setWidget(self.settingsScrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.settingsSmoothScrollArea, 2, 1, 1, 1)

        # # # #Hoa Add Setting 
        self.SettingsGroup = SettingCardGroup("SCRIPT SETTING", self.settingsScrollAreaWidgetContents)
        self.autoRunLastServer = SwitchSettingCard(
            icon=FIF.ROBOT,
            title=self.tr("自动开服"),
            content=self.tr("启动MCSL2时自动运行上次运行的服务器。"),
            parent=self.SettingsGroup,
        )
       

        self.RunningScript = ComboBoxSettingCard(
                configItem=cfg.runningFolder,
                icon=FIF.FINGERPRINT,
                title="Running Script Folder", 
                content="Select running script running folder.",
                texts=['TelegramCS_V1', 'TelegramCS_V2', 'TelegramCS_V3', 'TelegramCS_V4'
                ],
                parent=self.SettingsGroup,
            )
        

        self.defaultServer = PrimaryPushSettingCard(
            title="Default Server",
            icon=FIF.SYNC,
            text="Get Default Server",
            content="Server : " + str(cfg.defaultGateWay.value),
            parent=self.SettingsGroup,
            )
      
        
        self.defaultServer.clicked.connect(self.defaultServerClicked)
        self.SettingsGroup.addSettingCard(self.defaultServer)
        self.SettingsGroup.addSettingCard(self.autoRunLastServer)
        self.SettingsGroup.addSettingCard(self.RunningScript)

        self.verticalLayout.addWidget(self.SettingsGroup)
    def defaultServerClicked(self):
            gws = ni.gateways()
            cfg.set(cfg.defaultGateWay, gws['default'][ni.AF_INET][0])
        

        
