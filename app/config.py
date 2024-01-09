# coding:utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QGuiApplication, QFont
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            ColorConfigItem, OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator, ConfigSerializer, __version__)


class RunningScript(Enum):
    """ Select running script """

    V1 = 'TelegramCS_V1'
    V2 = 'TelegramCS_V2'
    V3 = 'TelegramCS_V3'
    V4 = 'TelegramCS_V4'

class Config(QConfig):
    runningFolder = OptionsConfigItem(
        "Script", "FolderTool", RunningScript.V3, OptionsValidator(RunningScript), EnumSerializer(RunningScript))
    
    defaultGateWay = ConfigItem("Script", "DefaultGateway", "")


    # defaultGateWay = OptionsConfigItem(
    #     "Download",
    #     "saveSameFileException",
    #     "ask",
    #     OptionsValidator(["ask", "overwrite", "stop"]),
    # )

cfg = Config()
qconfig.load('config/config.json', cfg)