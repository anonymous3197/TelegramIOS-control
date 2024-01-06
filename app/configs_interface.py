from PyQt5 import QtCore, QtGui, QtQuickWidgets,QtWidgets 
import sys
import os
from time import sleep
import json
from os.path import join,dirname
from PyQt5.QtCore import Qt , QThread,pyqtSignal,QThreadPool,QDateTime
from PyQt5.QtWidgets import QWidget,QTableWidgetItem,QFileDialog,QTableWidget,QApplication
from qfluentwidgets import BodyLabel, CardWidget, CheckBox, PushButton, TableWidget, TextEdit,StateToolTip
from UI.config_page_ui import Ui_ConfigsInterface
from modules.ATT import ATAPI
from modules.webDAV import ATT_DAV
from uuid import uuid4

curdir = dirname(__file__)
root_path = dirname(curdir)
temp_path = join(root_path,'Temp')
        #Create Temp if not exist
os.makedirs(temp_path,exist_ok=True)
class ThreadLogReport(QThread):
    SignalLog = pyqtSignal(str)
    SignalAnalytics =pyqtSignal(dict)
    finished = pyqtSignal()
    def __init__(self,ip,parent=None):
        super().__init__(parent)
        self.ip = ip
    def run(self):
        app = ATAPI(self.ip)
        content = app.get_log()
        self.SignalLog.emit(content)
        app = ATT_DAV(self.ip)
        file_temp = join(temp_path,f'analytics_{self.ip}.json')
        app.client.download_async(remote_path='TelegramCS_V3/data/analytics.json',local_path=file_temp)
        sleep(1)
        with open(file_temp, 'r') as json_file:
            data = json.load(json_file)
            self.SignalAnalytics.emit(data)
        os.remove(file_temp)



class ThreadLoadConfigsDevice(QThread):
    deviceSignal = pyqtSignal(dict)
    finished = pyqtSignal()
    def __init__(self,ip,parent=None):
        super().__init__(parent)
        self.ip = str(ip)
    def run(self):
            try:
                app = ATT_DAV(f'192.168.3.{self.ip}')
                result_DAV = app.client.list()
                if result_DAV:
                    file_temp = join(temp_path,f'192.168.3.{self.ip}.json')
                    app.client.download_async(remote_path='TelegramCS_V3/configs/configs.json',local_path=file_temp)
                    with open(file_temp, 'r') as json_file:
                        data = json.load(json_file)
                    current_json = {'Ipdevice': '192.168.3.'+self.ip, **data}
                    self.deviceSignal.emit(current_json)
                    os.remove(file_temp)

            except Exception as e:
                pass
            self.finished.emit()
class ConfigInterface(QWidget,Ui_ConfigsInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.uic = Ui_ConfigsInterface()
        self.uic.setupUi(self)
        self.initUI()
        self.initSlot()
    def initUI(self):
        #initTableView
        self.uic.TableWidgetDevices.setColumnWidth(0,130)
        self.uic.TableWidgetDevices.setColumnWidth(1,130)
        self.uic.TableWidgetDevices.setColumnWidth(2,100)
        self.uic.TableWidgetDevices.setColumnWidth(3,400)
        self.uic.TableWidgetDevices.setSelectionMode(QTableWidget.SingleSelection)

        self.uic.txtLogs.setReadOnly(True)
    def initSlot(self):
        self.uic.btnLoadDevice.clicked.connect(self.loadAllDevices)
        self.uic.TableWidgetDevices.itemSelectionChanged.connect(self.handleItemSelection)
        self.uic.btnEnableEdit.clicked.connect(self.btnEnableEdit_Clicked)
        # self.uic.TableWidgetDevices.itemChanged.connect(self.handleItemChanged)
    def handleItemChanged(self,item):
        row = item.row()
        column = item.column()
        new_value = item.text()
        print(f"Item at row {row}, column {column} changed to: {new_value}")
    def btnEnableEdit_Clicked(self):
        self.uic.TableWidgetDevices.setEditTriggers(QTableWidget.NoEditTriggers)
        
    def handleItemSelection(self):

        selectedIndexes = self.uic.TableWidgetDevices.selectedIndexes()
        if selectedIndexes:
            row = selectedIndexes[0].row()
            rowData = []
            for col in range(self.uic.TableWidgetDevices.columnCount()):
                item = self.uic.TableWidgetDevices.item(row, col)
                rowData.append(item.text())
            
            self.selectedRowData = rowData
            print(f'Selected Row Data: {self.selectedRowData}')
            workerLog = ThreadLogReport(self.selectedRowData[0],self)
            workerLog.SignalLog.connect(self.LogReporter)
            workerLog.SignalAnalytics.connect(self.LogAnalyticsReporter)
            workerLog.start()
    def LogReporter(self, data):
        self.uic.txtLogs.setPlainText('')
        self.uic.txtLogs.setPlainText(data)
    def LogAnalyticsReporter(self,data):
            self.uic.txtAnalyticsReport.setPlainText('')
            json_object = json.dumps(data, indent=4)

            self.uic.txtAnalyticsReport.setPlainText(str(json_object))

    def loadAllDevices(self):
        
        print("Clicked")
        self.count =0
        self.workerThreadGetDevice=[]
        self.stateTooltip = None
        self.stateTooltip = StateToolTip('Running', 'Please wait ..', self)
        self.stateTooltip.move(10, 10)
        self.stateTooltip.show()

        #Clear Table 
        self.uic.TableWidgetDevices.clearContents()
        self.uic.TableWidgetDevices.setRowCount(0)
        for i in range(2,255):
            workerDevice = ThreadLoadConfigsDevice(i,self)
            workerDevice.deviceSignal.connect(self.pushDataToTable)
            workerDevice.finished.connect(self.thread_finished)
            self.workerThreadGetDevice.append(workerDevice)
        for w in self.workerThreadGetDevice:
            w.start()
    def thread_finished(self):
        self.count +=1
        if self.count>=253:
            self.stateTooltip.setContent('Load Devices OK 😆')
            self.stateTooltip.setState(True)
            self.uic.TableWidgetDevices.sortItems(0)
    def pushDataToTable(self, json_data):
        if not json_data:
            return

        # Tạo danh sách các khóa (keys) từ JSON để đặt tên cột
        keys = list(json_data.keys())

        # Lấy số hàng hiện tại
        current_row = self.uic.TableWidgetDevices.rowCount()

        # Thêm một hàng mới vào cuối bảng
        self.uic.TableWidgetDevices.insertRow(current_row)

        # Đổ giá trị từ JSON vào các ô trong hàng mới
        for col, key in enumerate(keys):
            value = json_data.get(key, '')
            item = QTableWidgetItem(str(value))
            self.uic.TableWidgetDevices.setItem(current_row, col, item)
    def dataRevice(self,data):
        self.allIp = data
        for i, dt in enumerate(data):
            for j in range(5):
                self.uic.TableWidgetDevices.setItem(i, j, QTableWidgetItem(dt))
     