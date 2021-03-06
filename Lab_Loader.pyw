#! ./venv/Scripts/pythonw
import sys
import os
import platform
import json
import subprocess
import re
from pathlib import Path, PurePosixPath
from PyQt5 import QtCore, QtWidgets
import requests
import pysftp


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        app.setStyle(QtWidgets.QStyleFactory.create('WindowsVista'))
        MainWindow.setEnabled(True)
        MainWindow.resize(657, 405)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())

        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(657, 405))
        self.centralwidget.setMaximumSize(QtCore.QSize(657, 405))
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_1_selectProject = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1_selectProject.setGeometry(QtCore.QRect(55, 75, 120, 45))
        self.pushButton_1_selectProject.setMinimumSize(QtCore.QSize(120, 45))
        self.pushButton_1_selectProject.setMaximumSize(QtCore.QSize(120, 16777215))
        self.pushButton_1_selectProject.setObjectName("pushButton_1_selectProject")

        self.pushButton_2_selectLab = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2_selectLab.setGeometry(QtCore.QRect(55, 152, 120, 45))
        self.pushButton_2_selectLab.setMinimumSize(QtCore.QSize(120, 45))
        self.pushButton_2_selectLab.setMaximumSize(QtCore.QSize(120, 0))
        self.pushButton_2_selectLab.setObjectName("pushButton_2_selectLab")

        self.pushButton_3_loadLab = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3_loadLab.setGeometry(QtCore.QRect(55, 229, 120, 45))
        self.pushButton_3_loadLab.setMinimumSize(QtCore.QSize(120, 45))
        self.pushButton_3_loadLab.setMaximumSize(QtCore.QSize(120, 0))
        self.pushButton_3_loadLab.setObjectName("pushButton_3_loadLab")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 330, 631, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.comboBox_projectSelection = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_projectSelection.setGeometry(QtCore.QRect(250, 80, 171, 31))
        self.comboBox_projectSelection.setObjectName("comboBox_projectSelection")
        self.comboBox_projectSelection.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.comboBox_projectSelection.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)

        self.comboBox_LabSelection = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_LabSelection.setGeometry(QtCore.QRect(250, 155, 171, 31))
        self.comboBox_LabSelection.setObjectName("comboBox_LabSelection")
        self.comboBox_LabSelection.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.comboBox_LabSelection.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)

        self.comboBox_ModeSelection = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_ModeSelection.setGeometry(QtCore.QRect(250, 230, 171, 31))
        self.comboBox_ModeSelection.setObjectName("comboBox_ModeSelection")
        self.comboBox_ModeSelection.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.comboBox_ModeSelection.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_ModeSelection.addItem('CSR1000v Mode')
        self.comboBox_ModeSelection.addItem('vIOS Mode')

        self.error_dialog = QtWidgets.QErrorMessage()

        MainWindow.setCentralWidget(self.centralwidget)

        self.GetDir = []
        self.projectJson_list = []

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lab Loader"))
        self.pushButton_1_selectProject.setText(
            _translate("MainWindow", "Select Project"))
        self.pushButton_1_selectProject.clicked.connect(self.selectProject)
        self.pushButton_2_selectLab.setText(
            _translate("MainWindow", "Select Lab"))
        self.pushButton_2_selectLab.clicked.connect(self.selectLab)
        self.pushButton_3_loadLab.setText(_translate("MainWindow", "Load Lab"))
        self.pushButton_3_loadLab.clicked.connect(self.loadLab)

    def selectProject(self, MainWindow):
        self.comboBox_projectSelection.clear()
        self.GNS3_IP = self.get_IP()
        GetProjectList = requests.get(
            'http://' + self.GNS3_IP + ':3080/v2/projects')
        self.projectJson_list = GetProjectList.json()
        self.comboBox_projectSelection.addItems(sorted([i['name'] for i in GetProjectList.json()]))

    def get_IP(self):
        if os.name == 'nt':
            file = open(str(Path.home()) + os.path.join(r'\AppData', 'Roaming', 'GNS3', 'gns3_server.ini'),
                        'r').readlines()
        else:
            file = open(str(Path.home()) + os.path.join('/.config', 'GNS3', 'gns3_server.conf'),
                        'r').readlines()
        reg = re.compile(
            r"""(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}
            (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)""", re.X)
        for line in file:
            IPAddr = reg.search(line)
            if IPAddr:
                return IPAddr.group(0)

    def selectLab(self):
        self.comboBox_LabSelection.clear()
        for _, dirs, _ in os.walk(os.path.join('files', 'INE.VIRL.initial.configs', 'advanced.technology.labs')):
            dirs.sort()
            for dirname in dirs:
                self.comboBox_LabSelection.addItem(dirname)

    def loadLab(self):
        if str(self.comboBox_ModeSelection.currentText()) == 'vIOS Mode':
            check_bin = 'whereis mcopy'
            if os.name == 'nt':
                is32bit = (platform.architecture()[0] == '32bit')
                system32 = os.path.join(os.environ['SystemRoot'], 'SysNative' if is32bit else 'System32')
                bash = os.path.join(system32, 'bash.exe')
                check_bin = subprocess.check_output(bash + ' -c ' + '\"' + check_bin + '\"')
                if check_bin != b"mcopy:\n":
                    self.IOSv_loadLab()
            else:
                check_bin = subprocess.check_output(check_bin, shell=True)
                if check_bin != b"mcopy:\n":
                    self.IOSv_loadLab()
            self.error_dialog.showMessage('Error:\r\nmcopy is most likely not installed.\r\nTry installing mtools.')
        if str(self.comboBox_ModeSelection.currentText()) == 'CSR1000v Mode':
            check_bin = 'whereis mkisofs'
            if os.name == 'nt':
                is32bit = (platform.architecture()[0] == '32bit')
                system32 = os.path.join(os.environ['SystemRoot'], 'SysNative' if is32bit else 'System32')
                bash = os.path.join(system32, 'bash.exe')
                check_bin = subprocess.check_output(bash + ' -c ' + '\"' + check_bin + '\"')
                if check_bin != b"mkisofs:\n":
                    self.CSR1000v_loadLab()
                else:
                    self.error_dialog.showMessage('Error:\r\nmkisofs is most likely not installed.\r\nTry installing cdrtools or cdrkit.')
            else:
                check_bin = subprocess.check_output(check_bin, shell=True)
                if check_bin != b"mkisofs:\n":
                    self.CSR1000v_loadLab()
                else:
                    self.error_dialog.showMessage('Error:\r\nmkisofs is most likely not installed.\r\nTry installing cdrtools or cdrkit.')
        check_bin = 'whereis mcopy'
        


    def IOSv_loadLab(self):
        projectSelection = str(self.comboBox_projectSelection.currentText())
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        for i in self.projectJson_list:
            if i['name'] == projectSelection:
                project_id = i['project_id']
                project_filename = i['filename']

        GetProjectfile = requests.get(
            'http://' + self.GNS3_IP + ':3080/v2/projects/' + project_id + '/files/' + project_filename)
        projectJson = GetProjectfile.json()
        dirpath = os.path.join('files', 'INE.VIRL.initial.configs', 'advanced.technology.labs', str(self.comboBox_LabSelection.currentText()))
        progress = 0
        self.progressBar.setProperty("value", progress)
        if os.name == 'nt':
            is32bit = (platform.architecture()[0] == '32bit')
            system32 = os.path.join(os.environ['SystemRoot'], 'SysNative' if is32bit else 'System32')
            bash = os.path.join(system32, 'bash.exe')
        for filename in os.listdir(dirpath):
            if filename[:1] == 'r':
                string1 = 'md5sum ' + str(PurePosixPath(Path(dirpath))) + '/' + filename + ' | cut -d \' \' -f 1 > files/ios_config_checksum'
                string2 = 'cp ' + str(PurePosixPath(Path(dirpath))) + '/' + filename + ' files/ios_config.txt'
                string3 = 'cp files/IOSv_startup_config_template.img files/IOSv_startup_config_' + filename[:-4] + '.img'
                string4 = 'mcopy -i files/IOSv_startup_config_' + filename[:-4] + '.img@@63S files/ios_config.txt ::'
                string5 = 'mcopy -i files/IOSv_startup_config_' + filename[:-4] + '.img@@63S files/ios_config_checksum ::'
                string6 = 'md5sum files/IOSv_startup_config_' + filename[:-4] + '.img | cut -d \' \' -f 1 > files/IOSv_startup_config_' + filename[:-4] + '.img.md5sum'
                string7 = 'md5sum files/IOSv_startup_config_' + filename[:-4] + '.img | cut -d \' \' -f 1'
                if os.name == 'nt':
                    subprocess.call(bash + ' -c ' + '\"' + string1 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string2 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string3 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string4 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string5 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string6 + '\"')
                    string7 = subprocess.check_output(bash + ' -c ' + '\"' + string7 + '\"')
                else:
                    subprocess.call(string1, shell=True)
                    subprocess.call(string2, shell=True)
                    subprocess.call(string3, shell=True)
                    subprocess.call(string4, shell=True)
                    subprocess.call(string5, shell=True)
                    subprocess.call(string6, shell=True)
                    string7 = subprocess.check_output(string7, shell=True)
                string7 = string7[:-1].decode("utf -8")
                for p in projectJson["topology"]["nodes"]:
                    if p["name"] == "R" + filename[1:-4]:
                        p["properties"]["hdc_disk_image_md5sum"] = string7
                        node_id = p["node_id"]
                with pysftp.Connection(self.GNS3_IP, username='gns3', password='gns3', cnopts=cnopts) as sftp:
                    with sftp.cd('/opt/gns3/images/QEMU/'):
                        sftp.put('files/IOSv_startup_config_' + filename[:-4] + '.img.md5sum')
                        sftp.put('files/IOSv_startup_config_' + filename[:-4] + '.img')
                    sftp.close()
                with pysftp.Connection(self.GNS3_IP, username='gns3', password='gns3', cnopts=cnopts) as sftp:
                    for remotedir in sftp.listdir('/opt/gns3/projects/'+project_id+'/project-files/qemu/'):
                        if remotedir == node_id:
                            with sftp.cd('/opt/gns3/projects/'+project_id+'/project-files/qemu/'+node_id):
                                for remotefile in sftp.listdir():
                                    sftp.remove(remotefile)
                    sftp.close()
                os.remove("files/ios_config_checksum")
                os.remove("files/ios_config.txt")
                os.remove('files/IOSv_startup_config_' + filename[:-4] + '.img.md5sum')
                os.remove('files/IOSv_startup_config_' + filename[:-4] + '.img')
                progress = progress + 100/len(os.listdir(dirpath))
                self.progressBar.setProperty("value", progress)
        self.progressBar.setProperty("value", 100)


    def CSR1000v_loadLab(self):
        projectSelection = str(self.comboBox_projectSelection.currentText())
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        for i in self.projectJson_list:
            if i['name'] == projectSelection:
                project_id = i['project_id']
                project_filename = i['filename']

        GetProjectfile = requests.get(
            'http://' + self.GNS3_IP + ':3080/v2/projects/' + project_id + '/files/' + project_filename)
        projectJson = GetProjectfile.json()
        dirpath = os.path.join('files', 'INE.VIRL.initial.configs', 'advanced.technology.labs', str(self.comboBox_LabSelection.currentText()))
        progress = 0
        self.progressBar.setProperty("value", progress)
        if os.name == 'nt':
            is32bit = (platform.architecture()[0] == '32bit')
            system32 = os.path.join(os.environ['SystemRoot'], 'SysNative' if is32bit else 'System32')
            bash = os.path.join(system32, 'bash.exe')
        for filename in os.listdir(dirpath):
            if filename[:1] == 'r':
                string1 = 'cp ' + str(PurePosixPath(Path(dirpath))) + '/' + filename + ' files/iosxe_config.txt'
                string2 = 'mkisofs -l -o files/csr_config_' + filename[:-4] + '.iso files/iosxe_config.txt'
                string3 = 'md5sum files/csr_config_' + filename[:-4] + '.iso | cut -d \' \' -f 1'
                if os.name == 'nt':
                    subprocess.call(bash + ' -c ' + '\"' + string1 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string2 + '\"')
                    string3 = subprocess.check_output(bash + ' -c ' + '\"' + string3 + '\"')
                else:
                    subprocess.call(string1, shell=True)
                    subprocess.call(string2, shell=True)
                    string3 = subprocess.check_output(string3, shell=True)
                for p in projectJson["topology"]["nodes"]:
                    if p["name"] == "R" + filename[1:-4]:
                        p["properties"]["cdrom_image_md5sum"] = string3
                        node_id = p["node_id"]
                with pysftp.Connection(self.GNS3_IP, username='gns3', password='gns3', cnopts=cnopts) as sftp:
                    with sftp.cd('/opt/gns3/images/QEMU/'):
                        sftp.put('files/csr_config_' + filename[:-4] + '.iso')
                    sftp.close()
                with pysftp.Connection(self.GNS3_IP, username='gns3', password='gns3', cnopts=cnopts) as sftp:
                    for remotedir in sftp.listdir('/opt/gns3/projects/'+project_id+'/project-files/qemu/'):
                        if remotedir == node_id:
                            with sftp.cd('/opt/gns3/projects/'+project_id+'/project-files/qemu/'+node_id):
                                for remotefile in sftp.listdir():
                                    sftp.remove(remotefile)
                    sftp.close()
                os.remove("files/iosxe_config.txt")
                os.remove('files/csr_config_' + filename[:-4] + '.iso')
                progress = progress + 100/len(os.listdir(dirpath))
                self.progressBar.setProperty("value", progress)
        self.progressBar.setProperty("value", 100)


    def IOSvL2_loadLab(self):
        projectSelection = str(self.comboBox_projectSelection.currentText())
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        for i in self.projectJson_list:
            if i['name'] == projectSelection:
                project_id = i['project_id']
                project_filename = i['filename']

        GetProjectfile = requests.get(
            'http://' + self.GNS3_IP + ':3080/v2/projects/' + project_id + '/files/' + project_filename)
        projectJson = GetProjectfile.json()
        dirpath = os.path.join('files', 'INE.VIRL.initial.configs', 'advanced.technology.labs', str(self.comboBox_LabSelection.currentText()))
        progress = 0
        self.progressBar.setProperty("value", progress)
        if os.name == 'nt':
            is32bit = (platform.architecture()[0] == '32bit')
            system32 = os.path.join(os.environ['SystemRoot'], 'SysNative' if is32bit else 'System32')
            bash = os.path.join(system32, 'bash.exe')
        for filename in os.listdir(dirpath):
            if filename[:2] == 'sw':
                string1 = 'md5sum ' + str(PurePosixPath(Path(dirpath))) + '/' + filename + ' | cut -d \' \' -f 1 > files/ios_config_checksum'
                string2 = 'cp ' + str(PurePosixPath(Path(dirpath))) + '/' + filename + ' files/ios_config.txt'
                string3 = 'cp files/IOSv_startup_config_template.img files/IOSv_startup_config_' + filename[:-4] + '.img'
                string4 = 'mcopy -i files/IOSv_startup_config_' + filename[:-4] + '.img@@63S files/ios_config.txt ::'
                string5 = 'mcopy -i files/IOSv_startup_config_' + filename[:-4] + '.img@@63S files/ios_config_checksum ::'
                string6 = 'md5sum files/IOSv_startup_config_' + filename[:-4] + '.img | cut -d \' \' -f 1 > files/IOSv_startup_config_' + filename[:-4] + '.img.md5sum'
                string7 = 'md5sum files/IOSv_startup_config_' + filename[:-4] + '.img | cut -d \' \' -f 1'
                if os.name == 'nt':
                    subprocess.call(bash + ' -c ' + '\"' + string1 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string2 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string3 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string4 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string5 + '\"')
                    subprocess.call(bash + ' -c ' + '\"' + string6 + '\"')
                    string7 = subprocess.check_output(bash + ' -c ' + '\"' + string7 + '\"')
                else:
                    subprocess.call(string1, shell=True)
                    subprocess.call(string2, shell=True)
                    subprocess.call(string3, shell=True)
                    subprocess.call(string4, shell=True)
                    subprocess.call(string5, shell=True)
                    subprocess.call(string6, shell=True)
                    string7 = subprocess.check_output(string7, shell=True)
                string7 = string7[:-1].decode("utf -8")
                for p in projectJson["topology"]["nodes"]:
                    if p["name"] == "SW" + filename[2:-4]:
                        p["properties"]["hdc_disk_image_md5sum"] = string7
                        node_id = p["node_id"]
                with pysftp.Connection(self.GNS3_IP, username='gns3', password='gns3', cnopts=cnopts) as sftp:
                    with sftp.cd('/opt/gns3/images/QEMU/'):
                        sftp.put('files/IOSv_startup_config_' + filename[:-4] + '.img.md5sum')
                        sftp.put('files/IOSv_startup_config_' + filename[:-4] + '.img')
                    sftp.close()
                with pysftp.Connection(self.GNS3_IP, username='gns3', password='gns3', cnopts=cnopts) as sftp:
                    for remotedir in sftp.listdir('/opt/gns3/projects/'+project_id+'/project-files/qemu/'):
                        if remotedir == node_id:
                            with sftp.cd('/opt/gns3/projects/'+project_id+'/project-files/qemu/'+node_id):
                                for remotefile in sftp.listdir():
                                    sftp.remove(remotefile)
                    sftp.close()
                os.remove("files/ios_config_checksum")
                os.remove("files/ios_config.txt")
                os.remove('files/IOSv_startup_config_' + filename[:-4] + '.img.md5sum')
                os.remove('files/IOSv_startup_config_' + filename[:-4] + '.img')
                progress = progress + 100/len(os.listdir(dirpath))
                self.progressBar.setProperty("value", progress)
        self.progressBar.setProperty("value", 100)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
sys.exit(app.exec_())
