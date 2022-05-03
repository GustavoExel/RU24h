"""COLOCAR UM ERROR HANDLING!!!! (COM MESSAGEBOXES E NÃO RAISES QUE CRASHA O PROGRAMA)"""

from PyQt5 import QtCore, QtGui, QtWidgets
# import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyAesCrypt
import pickle
import string
import random
import os
import sys

class Ui_MainWindow(object):
    DATA_DIR = ".data"
    DATA_PATH = ".data/data"
    DRIVER_PATH = "geckodriver.exe"
    ICON_PATH = "icon.png"
    KEY_PATH = ".data/key"

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("RU24h")
        MainWindow.resize(800, 414)
        MainWindow.setWindowIcon(QtGui.QIcon(self.ICON_PATH))
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 781, 321))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 361, 291))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.userList = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.userList.setObjectName("userList")
        self.verticalLayout_2.addWidget(self.userList)
        self.deleteUserButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.deleteUserButton.setObjectName("deleteUserButton")
        self.verticalLayout_2.addWidget(self.deleteUserButton)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 371, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.nameField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.nameField.setObjectName("nameField")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameField)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.idField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.idField.setObjectName("idField")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.idField)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.passwordField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.passwordField.setObjectName("passwordField")
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.passwordField)
        self.verticalLayout.addLayout(self.formLayout)
        self.addUserButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addUserButton.setObjectName("addUserButton")
        self.verticalLayout.addWidget(self.addUserButton)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.scheduleButton = QtWidgets.QPushButton(self.centralwidget)
        self.scheduleButton.setGeometry(QtCore.QRect(570, 340, 211, 31))
        self.scheduleButton.setObjectName("scheduleButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.set_buttons()
        self.read_data()
        self.populate_user_list()

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RU24h"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Gerenciar usuários"))
        self.deleteUserButton.setText(_translate("MainWindow", "Deletar"))
        self.groupBox.setTitle(_translate("MainWindow", "Adicionar usuário"))
        self.label.setText(_translate("MainWindow", "Nome"))
        self.label_2.setText(_translate("MainWindow", "Matrícula"))
        self.label_3.setText(_translate("MainWindow", "Senha"))
        self.addUserButton.setText(_translate("MainWindow", "Adicionar"))
        self.scheduleButton.setText(_translate("MainWindow", "Agendar Refeições"))

    def set_buttons(self):
        self.addUserButton.clicked.connect(self.add_user)
        self.deleteUserButton.clicked.connect(self.delete_user)
        self.scheduleButton.clicked.connect(self.schedule)

    def populate_user_list(self):
        for name, _, _ in self.data:
            self.userList.addItem(name)

    def add_user(self):
        name, id_, password = self.nameField.text(), self.idField.text(), self.passwordField.text()

        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("RU24h")
        msg.setWindowIcon(QtGui.QIcon(self.ICON_PATH))
        if name=="" or id_=="" or password=="":
            msg.setText("Preencha todos os campos!")
            msg.setIcon(QtWidgets.QMessageBox.Critical)

        elif len(id_)!=8:
            msg.setText("Matrícula deve conter 8 caracteres")
            msg.setIcon(QtWidgets.QMessageBox.Critical)

        else:
            msg.setText("Usuário adicionado com sucesso!")
            msg.setIcon(QtWidgets.QMessageBox.Information)

            self.userList.addItem(name)
            self.data.append((name, id_, password))
            self.write_data()

        msg.exec_()
        self.nameField.clear()
        self.idField.clear()
        self.passwordField.clear()

    def delete_user(self):
        selectedItems = self.userList.selectedItems()
        if selectedItems:
            deleted_name = selectedItems[0].text()
            deleted_index = list(map(lambda t:t[0], self.data)).index(deleted_name)
            self.data.pop(deleted_index)
            self.userList.clear()
            self.populate_user_list()
            self.write_data()

    def get_key(self):
        if not os.path.exists(self.KEY_PATH):
            self.generate_key()

        with open(self.KEY_PATH, "rb") as f:
            return pickle.load(f)

    def generate_key(self):
        __key = "".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(128))
        with open(self.KEY_PATH, "wb") as f:
            pickle.dump(__key, f)

    def read_data(self):
        if not os.path.isfile(self.DATA_PATH):
            self.data = []
            return

        tmp = f"{self.DATA_PATH}_temp"
        __key = self.get_key()
        
        pyAesCrypt.decryptFile(self.DATA_PATH, tmp, __key)
        with open(tmp, "rb") as f:
            self.data = pickle.load(f)
        os.remove(tmp)

    def write_data(self):
        if not os.path.exists(self.DATA_DIR):
            os.mkdir(self.DATA_DIR)
            os.system(f"attrib +h {self.DATA_DIR}")
            self.generate_key()

        tmp = f"{self.DATA_PATH}_temp"
        __key = self.get_key()
        
        with open(tmp, "wb") as f:
            pickle.dump(self.data, f)
        pyAesCrypt.encryptFile(tmp, self.DATA_PATH, __key)
        os.remove(tmp)
    
    def schedule(self):
        try:
            self.driver = webdriver.Firefox(executable_path=self.DRIVER_PATH)
            url = "https://sgpru.sistemas.ufsc.br/agendamento/home.xhtml"
            self.driver.get(url)

            find = lambda by,value: WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((by, value)))
            user     = lambda u: find(By.ID, "username").send_keys(u)
            passwd   = lambda p: find(By.ID, "password").send_keys(p)
            login    = lambda:   find(By.NAME, "submit").click()
            menu     = lambda:   find(By.XPATH, "/html/body/div[1]/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/div/form/div/div[2]/div/ul/li[2]/a/span").click()
            meal     = lambda i: Select(find(By.ID, "agendamentoForm:refeicao")).select_by_index(i)
            date     = lambda i: Select(find(By.ID, "agendamentoForm:dtRefeicao")).select_by_index(i)
            schedule = lambda:   find(By.XPATH, "/html/body/div[1]/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div/div/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div/form/div/table/tbody/tr[8]/td[2]/button/span[2]").click()
            quit     = lambda:   find(By.XPATH, "/html/body/div[1]/div[1]/div/form/table/tbody/tr/td/a[2]").click()
            bk2login = lambda:   find(By.XPATH, "/html/body/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div/div[2]/div[2]/table/tbody/tr[1]/td/p/a").click()
            
            for name, id_, password in self.data:
                user(id_)
                passwd(password)
                login()
                for d in [1, 2]:     # [Hoje, Amanhã]
                    for m in [1, 2]: # [Almoço, Jantar]
                        menu()
                        meal(m)
                        date(d)
                        schedule()
                quit()
                bk2login()
        except Exception as f:
            self.raise_error( str(f) )
        self.driver.quit()

    def raise_error(self, text=None):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("RU24h")
        msg.setWindowIcon(QtGui.QIcon(self.ICON_PATH))
        msg.setText("Um erro foi encontrado!" + ("" if text is None else "\n"+text) )
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()

if __name__ == "__main__":
    # Schedule silently
    if len(sys.argv)>1 and sys.argv[1]=="-s":
        ui = Ui_MainWindow()
        ui.read_data()
        ui.schedule()
    # Open GUI
    else:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setup_ui(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())