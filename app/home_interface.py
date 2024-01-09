import os
from paramiko import SSHClient,AutoAddPolicy
import time
from PyQt5.QtGui import QIcon,QColor

from PyQt5.QtCore import  Qt,QThread,pyqtSignal,QDateTime
from PyQt5.QtWidgets import QWidget,QTableWidgetItem,QFileDialog,QTableWidget
from qfluentwidgets import StateToolTip
from modules.ATT import ATAPI
from modules.webDAV import ATT_DAV
from UI.Ui_homepage import Ui_Frame
from os.path import dirname,join
from .config import cfg
class ThreadLoadDevice(QThread):
    deviceSignal = pyqtSignal(str,bool)
    finished = pyqtSignal()

    def __init__(self,ip,parent=None):
        super().__init__(parent)
        self.ip = str(ip)
    def run(self):
            try:
                
                subnet = cfg.defaultGateWay.value.rsplit('.', 1)[0] + '.'
                host = subnet +self.ip
                app = ATT_DAV(host)
                result = app.client.list()
                if result:
                    client = ATAPI(host)
                    result_state = client.get_running()
                    if result_state != []:
                        self.deviceSignal.emit(host,True)
                    else:
                        self.deviceSignal.emit(host,False)
            except:
                pass
            self.finished.emit()
class ThreadWorker(QThread):
    signalResult = pyqtSignal(str)
    finished = pyqtSignal()
    def __init__(self, target_function,parent=None, *args, **kwargs):
        super().__init__(parent)
        self.target_function = target_function
        self.args = args
        self.kwargs = kwargs

    def run(self):

        try:
            result = self.target_function(*self.args, **self.kwargs)
            action = self.kwargs['title']
            self.signalResult.emit(f'{self.args[0]}: {action}--->{result}')
        except Exception as e:
            print(e)
            self.signalResult.emit(f'Error--->{e}')
        self.finished.emit()
class HomeInterface(QWidget,Ui_Frame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.uic = Ui_Frame()
        self.uic.setupUi(self)
        self.initUI()
        self.initVariable()
        self.initSlot()
    def initUI(self):
        #initTableView
        self.uic.TableWidgetDevices.setColumnWidth(0,150)
        self.uic.TableWidgetDevices.setColumnWidth(1,100)
        self.uic.TableWidgetDevices.setEditTriggers(QTableWidget.NoEditTriggers)
        self.uic.TableWidgetLogs.setColumnWidth(0,170)
        self.uic.TableWidgetLogs.setColumnWidth(1,400)
        self.uic.TableWidgetLogs.setEditTriggers(QTableWidget.NoEditTriggers)


    def initVariable(self):
        self.allIp =[]
        self.selected_items = []
    def initSlot(self):
        self.uic.btnLoadDevice.clicked.connect(self.loadAllDevices)
        self.uic.CheckBoxMultil.stateChanged.connect(self.toggleCheckbox)
        self.uic.CheckBoxSingle.stateChanged.connect(self.toggleCheckbox)
        self.uic.btnOpenFile.clicked.connect(self._ImportFileScript)
        self.uic.btnUpload.clicked.connect(self.btnUpload_Clicked)
        self.uic.btnClearLogs.clicked.connect(self.btnClearLogs_Clicked)
        self.uic.btnSleep.clicked.connect(self.btnSleep_Clicked)
        self.uic.btnWakeup.clicked.connect(self.btnWakeup_Clicked)
        self.uic.btnDownloadBk.clicked.connect(self.btnDownloadBk_Clicked)

        self.uic.btnRespring.clicked.connect(self.btnRespring_Clicked)
        self.uic.btnStartScript.clicked.connect(self.startScript_Clicked)
        self.uic.btnStopScript.clicked.connect(self.stopScript_Clicked)
        self.uic.TableWidgetDevices.itemSelectionChanged.connect(self.handleItemSelection)
    def handleItemSelection(self):
        # Xóa dữ liệu cũ trong mảng
        self.selected_items.clear()

        # Lấy danh sách các mục được chọn
        selected_items = self.uic.TableWidgetDevices.selectedItems()

        # Thêm các mục được chọn vào mảng
        for item in selected_items:
            #Thêm vào mảng nếu phần tử trong item khác ""
            if item.text() != "":
                self.selected_items.append(item.text())
        for selected_item in self.selected_items:
                print('Selected item:', selected_item)
        # In danh sách các mục được chọn
        if len(self.selected_items) ==1:
            for selected_item in self.selected_items:
                self.uic.txtIpDevice.setText(selected_item)
                self.uic.CheckBoxSingle.setChecked(True)
        else:
            self.uic.CheckBoxMultil.setChecked(True)
    def btnDownloadBk_Clicked(self):
        print("btnDownloadBk_Clicked ")
        self.loadStateTooltip()
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.downloadBk,self,ip,title="Download Backup")
            worker.signalResult.connect(self.showLog)
            worker.finished.connect(self.thread_finished)
            workerThread.append(worker)
        for w in workerThread:
            w.start() 
    def downloadBk(self,ip,title):
        curdir = dirname(__file__)
        root_path = dirname(curdir)

        backup_path = join(root_path,'BackupData')

        app = ATT_DAV(ip)
        results = app.client.list()
        for result in results:
            if 'TelegramCS' in result:
                data_folder = result + 'data'
                local_path = join(backup_path,f'data_{ip}/{data_folder}')
                os.makedirs(dirname(local_path),exist_ok=True)
                app.client.download_sync(remote_path=data_folder,local_path=local_path)
        return True


    def btnWakeup_Clicked(self):
        print("btnWakeup_Clicked ")
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.wakeupIOS,self,ip,title="Wakeup Device")
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def wakeupIOS(self,ip ,title):
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(ip, username='root', password='alpine')
            stdin, stdout, stderr = client.exec_command("activator send libactivator.system.homebutton")
            time.sleep(.4)
            stdin, stdout, stderr = client.exec_command("activator send libactivator.system.homebutton")
            client.close()
            return True
        except Exception as e:
            print(e)
            return False
        


    def btnSleep_Clicked(self):
        print("btnSleep_Clicked ")
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.sleepIOS,self,ip,title="Sleep Device")
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def sleepIOS(self,ip,title):
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(ip, username='root', password='alpine')
            stdin, stdout, stderr = client.exec_command("activator send libactivator.system.sleepbutton")
            client.close()
            return True
        except Exception as e:
            print(e)
            return False

    def btnClearLogs_Clicked(self):
        print("btnClearLogs_Clicked ")
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.clearLog,self,ip,title="Clear Logs")
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def clearLog(self,ip,title):
        try:
            api = ATAPI(ip)
            result = api.clear_log()
            return result
        except Exception as e:
            print(e)
            return False
 
    def btnUpload_Clicked(self):
        localPath = self.uic.txtPath.toPlainText()
        remotePath =  self.uic.txtPathRemote.toPlainText()
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.Upload_File,self,ip,localPath,remotePath,title="Upload File")
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def Upload_File(self,ip,local_path,remote_path,title):
        try:
            app = ATT_DAV(ip)
            result = app.upload_folder(local_path,remote_path)
            return result
        except Exception as e:
            print(e)
            return False
    def btnRespring_Clicked(self):
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.reSpringIOS,self,ip,title="Respring Device")
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def startScript_Clicked(self):
        pathScript = self.uic.txtPathRemote.toPlainText()
        mode = "START"
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.runScript,self,ip,mode,pathScript,title="Start Script")
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()

    def stopScript_Clicked(self):
        pathScript = self.uic.txtPathRemote.toPlainText()
        # pathScript = cfg.runningFolder.value + 'main.py'
        mode = "STOP"
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.runScript,self,ip,mode,pathScript,title="Stop Script")
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()

    
    def runScript(self,ip,mode,pathScript,title):
        if mode == "STOP":
            app = ATT_DAV(ip)
            content = {"close": 1}
            result = app.update_file(f'{cfg.runningFolder}/configs/close_configs.json', content)
            return result
        elif mode == "START":
            api = ATAPI(ip)
            result = api.run_code(pathScript)
            return result
       

    def reSpringIOS(self,ip,title):
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(ip, username='root', password='alpine')
            stdin, stdout, stderr = client.exec_command("activator send libactivator.system.respring")
            time.sleep(5)
            stdin, stdout, stderr = client.exec_command("activator send libactivator.system.homebutton")

            client.close()
            return True
       
        except Exception as e:
            print(e)
            return False


   
    def showLog(self,data):
        current_datetime = QDateTime.currentDateTime()
        datetime_str = current_datetime.toString("dd-MM-yyyy hh:mm:ss")
        current_row = self.uic.TableWidgetLogs.rowCount()
        self.uic.TableWidgetLogs.setRowCount(current_row + 1)
        self.uic.TableWidgetLogs.setItem(current_row, 0, QTableWidgetItem(datetime_str))
        self.uic.TableWidgetLogs.setItem(current_row, 1, QTableWidgetItem(data))
        self.uic.TableWidgetLogs.scrollToBottom()
                
    def _ImportFileScript(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.scriptPath = QFileDialog.getExistingDirectory(self, 'Open File or Folder', '', options=options)
        if not self.scriptPath:
            self.scriptPath, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)', options=options)

        if self.scriptPath:
            print(f'Selected item: {self.scriptPath}')
        self.uic.txtPath.setText(self.scriptPath)
        
    def toggleCheckbox(self):
            sender = self.sender()
            if sender == self.uic.CheckBoxMultil and sender.isChecked():
                self.uic.CheckBoxSingle.setChecked(False)
                self.cbMultil = True
                self.cbSingle = not self.cbMultil

            elif sender == self.uic.CheckBoxSingle and sender.isChecked():
                self.uic.CheckBoxMultil.setChecked(False)
                self.cbSingle = True
                self.cbMultil = not self.cbSingle
    def loadStateTooltip(self):
        self.count =0
        self.workerThreadGetDevice=[]
        self.stateTooltip = None
        self.stateTooltip = StateToolTip('Running', 'Please wait ..', self)
        self.stateTooltip.move(10, 10)
        self.stateTooltip.show()
    def loadAllDevices(self):
            self.loadStateTooltip()
            #Clear Table 
            self.uic.TableWidgetDevices.clearContents()
            self.uic.TableWidgetDevices.setRowCount(0)
            for i in range(2,255):
                workerDevice = ThreadLoadDevice(i,self)
                workerDevice.deviceSignal.connect(self.UpdateList)
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

        
    def UpdateList(self,data,state):
        current_row = self.uic.TableWidgetDevices.rowCount()
        self.uic.TableWidgetDevices.setRowCount(current_row + 1)
        self.uic.TableWidgetDevices.setItem(current_row, 0, QTableWidgetItem(data))
        if state:
            item = QTableWidgetItem()
            item.setIcon(QIcon(r'F:\py_project\TelegramIOS-control\resource\images\green.ico'))
            item.setBackground(QColor('red'))
            self.uic.TableWidgetDevices.setItem(current_row, 1, item)
        else:
            item = QTableWidgetItem()
            item.setIcon(QIcon(r'F:\py_project\TelegramIOS-control\resource\images\red.ico'))
            item.setBackground(QColor('red'))
            self.uic.TableWidgetDevices.setItem(current_row, 1, item)
    def dataRevice(self,data):
        self.allIp = data
        for i, dt in enumerate(data):
            for j in range(5):
                self.uic.TableWidgetDevices.setItem(i, j, QTableWidgetItem(dt))
     