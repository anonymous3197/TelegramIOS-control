# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\py_project\TelegramIOS\UI\dev.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(757, 457)
        self.ScrollArea = ScrollArea(Frame)
        self.ScrollArea.setGeometry(QtCore.QRect(380, 260, 71, 71))
        self.ScrollArea.setWidgetResizable(True)
        self.ScrollArea.setObjectName("ScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 69, 69))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.StrongBodyLabel = StrongBodyLabel(Frame)
        self.StrongBodyLabel.setGeometry(QtCore.QRect(360, 240, 111, 19))
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.BodyLabel = BodyLabel(Frame)
        self.BodyLabel.setGeometry(QtCore.QRect(210, 270, 63, 19))
        self.BodyLabel.setObjectName("BodyLabel")
        self.StrongBodyLabel_2 = StrongBodyLabel(Frame)
        self.StrongBodyLabel_2.setGeometry(QtCore.QRect(250, 130, 111, 19))
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.StrongBodyLabel.setText(_translate("Frame", "Strong body label"))
        self.BodyLabel.setText(_translate("Frame", "Body label"))
        self.StrongBodyLabel_2.setText(_translate("Frame", "Strong body label"))
from qfluentwidgets import BodyLabel, ScrollArea, StrongBodyLabel