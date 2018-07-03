import sys

import hashlib
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from Clases.window_lobby import WindowLobby
from Clases.window_registry import WindowRegistry
import xmlrpc.client
import socket
from Clases.internationalization_module import OPTIONS
from Clases.common import PORT

from PyQt5 import QtGui

SERVER_URL = "http://localhost:8080"


class WindowLogin(QMainWindow):
    def __init__(self, server):
        super().__init__()
        self.client = xmlrpc.client.ServerProxy("http://localhost:8000/")
        self.server = server
        self.selected_language = 'es'
        self.init_UI()
        self.show()

    def init_UI(self):
        # Add core elements for the window
        self.lbl_tittle1 = QLabel("Batalla ", self)
        self.lbl_tittle1.setStyleSheet(
            "font-weight: b  old; color: white; font-family: century gothic; font-size: 29px")
        self.lbl_tittle1.move(55, 50)
        self.img_logo = QLabel(self)
        pixmap = QPixmap("Clases/images/imgTitle.png")
        self.img_logo.setPixmap(pixmap)
        self.img_logo.move(155, 5)
        self.img_logo.setMinimumSize(100, 100)
        self.lbl_tittle2 = QLabel("Naval ", self)
        self.lbl_tittle2.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 29px")
        self.lbl_tittle2.move(252, 50)

        # This window
        self.setFixedSize(400, 650)
        self.center()
        self.setWindowTitle('Inicio de sesión')
        self.setWindowIcon(QtGui.QIcon('Clases/images/b6.ico'))

        # Label username
        self.lbl_username = QLabel("Usuario", self)
        self.lbl_username.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lbl_username.move(50, 180)

        # Text field USERNAME
        self.txt_username = QLineEdit(self)
        self.txt_username.move(50, 220)
        self.txt_username.setStyleSheet("font-weight: bold; color: black; font-family: century gothic; font-size: 16px")
        self.txt_username.setMinimumSize(300, 35)

        # Label password
        self.lbl_password = QLabel("Contraseña", self)
        self.lbl_password.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lbl_password.move(50, 280)
        self.lbl_password.setMinimumSize(300, 35)

        # Text field Password
        self.txt_password = QLineEdit(self)
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.move(50, 320)
        self.txt_password.setStyleSheet("font-weight: bold; color: black; font-family: century gothic; font-size: 16px")
        self.txt_password.setMinimumSize(300, 35)

        # Label empty fields
        self.lbl_empty_fields = QLabel("*Campos vacios", self)
        self.lbl_empty_fields.setStyleSheet(
            "font-weight: bold; color: orange; font-family: century gothic; font-size: 16px")
        self.lbl_empty_fields.move(250, 150)
        self.lbl_empty_fields.setMinimumSize(300, 30)
        self.lbl_empty_fields.setVisible(False)

        # Button to login
        self.btn_login = QPushButton('Iniciar sesión', self)
        # self.btn_login.resize()
        self.btn_login.move(140, 400)
        self.btn_login.setStyleSheet(
            "background-color: #08AE9E; font-weight: bold; color: White; font-family: century gothic; font-size: 16px")
        self.btn_login.clicked.connect(self.login_clicked)
        # cell.clicked.connect(self.buttonClicked)

        # Label password
        self.lbl_question = QLabel("¿No tienes una cuenta?", self)
        self.lbl_question.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 15px")
        self.lbl_question.move(45, 450)
        self.lbl_question.setMinimumSize(300, 35)

        # Label invalid username or password
        self.lbl_invalid_account = QLabel("*Ha ingresado un nombre de usuario o la\ncontraseña incorrectos.", self)
        self.lbl_invalid_account.setStyleSheet(
            "font-weight: bold; color: orange; font-family: century gothic; font-size: 14px")
        self.lbl_invalid_account.move(50, 340)
        self.lbl_invalid_account.setMinimumSize(300, 70)
        self.lbl_invalid_account.setVisible(False)

        self.lbl_account = QLabel("Crea una", self)
        self.lbl_account.setStyleSheet("font-weight: bold; color: ORANGE; font-family: century gothic; font-size: 15px")
        self.lbl_account.move(255, 450)
        self.lbl_account.setMinimumSize(300, 35)
        self.lbl_account.mousePressEvent = self.create_account_clicked

        # Label change language
        self.lbl_change_language = QLabel("Change language", self)
        self.lbl_change_language.setStyleSheet("font-weight: bold;"
                                               "color: white;"
                                               "font-family: century gothic;"
                                               "font-size: 15px")
        self.lbl_change_language.move(150, 600)
        self.lbl_change_language.setMinimumSize(150, 35)

        # ComboBox language change
        self.cb_language = QComboBox(self)
        self.cb_language.addItems(["Español", "English"])
        self.cb_language.setStyleSheet("font-weight: bold;"
                                       "color: black;"
                                       "font-family: century gothic;"
                                       "font-size: 15px;"
                                       "background-color: lightgray;"
                                       "selection-background-color: darckgray;")
        self.cb_language.move(290, 600)
        self.cb_language.currentIndexChanged.connect(self.get_language)
        self.cb_language.currentIndexChanged.connect(self.reset_texts)

        # Set the baackground image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Clases/images/fondo_login.png")))
        self.setPalette(palette)
        self.show()

    # Function to get the selected language.
    def get_language(self, event):
        if self.cb_language.currentText() == "Español":
            self.selected_language = "es"
        if self.cb_language.currentText() == "English":
            self.selected_language = "en"
        print(self.selected_language)
        self.t = OPTIONS.get(self.selected_language, "es")
        print(self.t)

    # Function to assign new values to buttons and labels.
    def reset_texts(self, event):
        t = OPTIONS.get(self.selected_language)
        self.lbl_username.setText(t["username"])
        self.lbl_password.setText(t["password"])
        self.lbl_empty_fields.setText(t["empty_fields"])
        self.btn_login.setText(t["login"])
        self.lbl_question.setText(t["question"])
        self.lbl_invalid_account.setText(t["invalid_account"])
        self.lbl_account.setText(t["account"])
        self.lbl_change_language.setText(t["change_language"])
        print("textos reseteados")

    # Code to initialize the window centered
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_account_clicked(self, event):
        print(self.selected_language)
        self.windowRegistry = WindowRegistry(self.selected_language)
        self.windowRegistry.show()
        # self.setVisible(False)

    def login_clicked(self):
        # Falta obtener la ip de mi propia maquina en lugar del localhost
        self.clean()
        if not self.validate_empty_fields():
            self.username = self.txt_username.text()
            self.password = self.txt_password.text()
            self.password = hashlib.sha256(self.password.encode()).hexdigest()
            hostname = socket.gethostname()
            response = self.client.user_login(self.username, self.password, hostname, PORT)
            print(response)
            status = response["success"]
            print("status de la operacion:")
            print(status)
            if status:
                self.windowLobby = WindowLobby(self.username, [], self.server, self.selected_language)
                self.windowLobby.show()
                self.client.update_list()
                # self.close()
            else:
                self.lbl_invalid_account.setVisible(True)
        else:
            self.lbl_empty_fields.setVisible(True)

    def validate_empty_fields(self):
        return self.txt_username.text() == "" or self.txt_password.text() == ""

    def clean(self):
        self.lbl_empty_fields.setVisible(False)
        self.lbl_invalid_account.setVisible(False)
