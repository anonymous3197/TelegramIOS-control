from paramiko import SSHClient,AutoAddPolicy
import time
from PyQt5 import QtCore, QtGui, QtQuickWidgets,QtWidgets 
from PyQt5.QtCore import Qt , QThread,pyqtSignal,QThreadPool,QDateTime
from PyQt5.QtWidgets import QWidget,QTableWidgetItem,QFileDialog,QTableWidget
from qfluentwidgets import BodyLabel, CardWidget, CheckBox, PushButton, TableWidget, TextEdit,StateToolTip
from modules.ATT import ATAPI
from modules.webDAV import ATT_DAV
from UI.Ui_homepage import Ui_Frame
class ThreadRunScript(QThread):
    signalResult = pyqtSignal (str)
    def __init__(self,ip,pathScript,mode,parent = None):
        super().__init__(parent)
        self.ip =ip 
        self.pathScript = pathScript
        self.mode= mode
    def run(self):
            if self.mode == "STOP":
                try:
                    app = ATT_DAV(self.ip)
                    content = {"close":1}
                    result = app.update_file(r'TelegramCS_V2/configs/close_configs.json',content)
                    self.signalResult.emit(f'{self.ip}: {self.mode}--->{result}')
                except Exception as e:
                    print(e)
                        
            elif self.mode == "START":
                try:
                    api = ATAPI(self.ip)
                    result = api.run_code(self.pathScript)
                    self.signalResult.emit(f'{self.ip}: {self.mode}--->{result}')

                except:
                    print("Errorrr")
            
                 
                
class ThreadLoadDevice(QThread):
    deviceSignal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self,ip,parent=None):
        super().__init__(parent)
        self.ip = str(ip)
    def run(self):
            try:
                host = "192.168.3." +self.ip
                app = ATT_DAV(f'192.168.3.{self.ip}')
                result = app.client.list()
                if result:
                    self.deviceSignal.emit(host)
            except:
                pass
            self.finished.emit()
class ThreadWorker(QThread):
    signalResult = pyqtSignal(str)

    def __init__(self, target_function,parent=None, *args, **kwargs):
        super().__init__(parent)
        self.target_function = target_function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.target_function(*self.args, **self.kwargs)
            self.signalResult.emit(f'Result--->{self.args[0]} ---->{result}')
        except Exception as e:
            print(e)
            self.signalResult.emit(f'Error--->{e}')

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
        self.uic.TableWidgetDevices.setColumnWidth(0,200)
        self.uic.TableWidgetDevices.setEditTriggers(QTableWidget.NoEditTriggers)
        self.uic.TableWidgetLogs.setColumnWidth(0,170)
        self.uic.TableWidgetLogs.setColumnWidth(1,230)
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
            self.selected_items.append(item.text())
        for selected_item in self.selected_items:
                print(selected_item)
        # In danh sách các mục được chọn
        if len(self.selected_items) ==1:
            for selected_item in self.selected_items:
                self.uic.txtIpDevice.setText(selected_item)
                self.uic.CheckBoxSingle.setChecked(True)
        else:
            self.uic.CheckBoxMultil.setChecked(True)
    def btnWakeup_Clicked(self):
        print("btnWakeup_Clicked ")
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.wakeupIOS,self,ip)
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def wakeupIOS(self,ip):
        print("Sleep Device ~~")
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username='root', password='alpine')
        stdin, stdout, stderr = client.exec_command("activator send libactivator.system.homebutton")
        time.sleep(.4)
        stdin, stdout, stderr = client.exec_command("activator send libactivator.system.homebutton")

        client.close()
        return True


    def btnSleep_Clicked(self):
        print("btnSleep_Clicked ")
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.sleepIOS,self,ip)
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def sleepIOS(self,ip):
        print("Sleep Device ~~")
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username='root', password='alpine')
        stdin, stdout, stderr = client.exec_command("activator send libactivator.system.sleepbutton")
        client.close()
        return True

    def btnClearLogs_Clicked(self):
        print("btnClearLogs_Clicked ")
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.clearLog,self,ip)
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def clearLog(self,ip):
        api = ATAPI(ip)
        result = api.clear_log()
        return result
    def Upload_File(self,ip,local_path,remote_path):
        app = ATT_DAV(ip)
        result = app.upload_folder(local_path,remote_path)
        return result
    def btnUpload_Clicked(self):
        localPath = self.uic.txtPath.toPlainText()
        remotePath =  self.uic.txtPathRemote.toPlainText()
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.Upload_File,self,ip,localPath,remotePath)
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def btnRespring_Clicked(self):
        print("btnRespring_Clicked ")
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.reSpringIOS,self,ip)
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()
    def startScript_Clicked(self):
        pathScript = self.uic.txtPathRemote.toPlainText()
        mode = "START"
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.runScript,self,mode,ip,pathScript)
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()

    def stopScript_Clicked(self):
        print("stopScript_Clicked ")
        pathScript = self.uic.txtPathRemote.toPlainText()
        mode = "STOP"
        workerThread = []
        for ip in self.selected_items:
            worker = ThreadWorker(self.runScript,self,mode,ip,pathScript)
            worker.signalResult.connect(self.showLog)
            workerThread.append(worker)
        for w in workerThread:
            w.start()

    
    def runScript(self,mode,ip,pathScript):
        if mode == "STOP":
            print("Vao day roi nhe")
            app = ATT_DAV(ip)
            content = {"close": 1}
            result = app.update_file(r'TelegramCS_V3/configs/close_configs.json', content)
            return result
        elif mode == "START":
            print("Vao day")
            api = ATAPI(ip)
            result = api.run_code(pathScript)
            return result
       

    def reSpringIOS(self,ip):
        print("Respring Device ~~")
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username='root', password='alpine')
        stdin, stdout, stderr = client.exec_command("activator send libactivator.system.respring")
        time.sleep(5)
        stdin, stdout, stderr = client.exec_command("activator send libactivator.system.homebutton")

        client.close()
        return True


   
    def showLog(self,data):
        current_datetime = QDateTime.currentDateTime()
        datetime_str = current_datetime.toString("dd-MM-yyyy hh:mm:ss")
        current_row = self.uic.TableWidgetLogs.rowCount()
        self.uic.TableWidgetLogs.setRowCount(current_row + 1)
        self.uic.TableWidgetLogs.setItem(current_row, 0, QTableWidgetItem(datetime_str))
        self.uic.TableWidgetLogs.setItem(current_row, 1, QTableWidgetItem(data))
                
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
    def loadAllDevices(self):
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
        
    def UpdateList(self,data):
        current_row = self.uic.TableWidgetDevices.rowCount()
        self.uic.TableWidgetDevices.setRowCount(current_row + 1)
        self.uic.TableWidgetDevices.setItem(current_row, 0, QTableWidgetItem(data))
    def dataRevice(self,data):
        self.allIp = data
        for i, dt in enumerate(data):
            for j in range(5):
                self.uic.TableWidgetDevices.setItem(i, j, QTableWidgetItem(dt))
     