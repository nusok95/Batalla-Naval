import json
import sys
import hashlib
# import MySQLdb
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtGui
import xmlrpc.client
from Clases.internationalization_module import OPTIONS


# SERVER_URL = "http://localhost:8080"

class WindowRegistry(QMainWindow):
    def __init__(self, selected_language):
        super().__init__()
        self.client = xmlrpc.client.ServerProxy("http://localhost:8000/")
        self.selected_lenguage = selected_language
        print(self.selected_lenguage)
        self.init_UI()
        self.show()
        self.reset_texts()

    def init_UI(self):
        # Add core elements for the window
        self.lbl_tittle1 = QLabel("Batalla ", self)
        self.lbl_tittle1.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 29px")
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
        self.setWindowTitle('Registro')
        self.setWindowIcon(QtGui.QIcon('Clases/images/b6.ico'))

        # Label go_back
        self.lbl_go_back = QLabel("<< Volver", self)
        self.lbl_go_back.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 16px")
        self.lbl_go_back.move(13, -43)
        self.lbl_go_back.setMinimumSize(300, 300)
        self.lbl_go_back.setVisible(True)

        # Label invalid password
        self.lbl_invalid_password = QLabel("*Las contraseñas no coinciden", self)
        self.lbl_invalid_password.setStyleSheet(
            "font-weight: bold; color: orange; font-family: century gothic; font-size: 14px")
        self.lbl_invalid_password.move(50, 258)
        self.lbl_invalid_password.setMinimumSize(300, 580)
        self.lbl_invalid_password.setVisible(False)

        # Label invalid username
        self.lbl_invalid_username = QLabel("*Nombre de usuario ya existente", self)
        self.lbl_invalid_username.setStyleSheet(
            "font-weight: bold; color: orange; font-family: century gothic; font-size: 14px")
        self.lbl_invalid_username.move(50, 98)
        self.lbl_invalid_username.setMinimumSize(300, 580)
        self.lbl_invalid_username.setVisible(False)

        # Label invalid email
        self.lbl_invalid_email = QLabel("*Correo electrónico ya existente", self)
        self.lbl_invalid_email.setStyleSheet(
            "font-weight: bold; color: orange; font-family: century gothic; font-size: 14px")
        self.lbl_invalid_email.move(50, 19)
        self.lbl_invalid_email.setMinimumSize(300, 580)
        self.lbl_invalid_email.setVisible(False)

        # Label empty fields
        self.lbl_empty_fields = QLabel("*Campos vacios", self)
        self.lbl_empty_fields.setStyleSheet(
            "font-weight: bold; color: orange; font-family: century gothic; font-size: 16px")
        self.lbl_empty_fields.move(250, 150)
        self.lbl_empty_fields.setMinimumSize(300, 30)
        self.lbl_empty_fields.setVisible(False)

        # Label username
        self.lb_name = QLabel("Nombre", self)
        self.lb_name.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lb_name.move(50, 150)
        self.lb_name.setMinimumSize(300, 30)

        # Text field NAME
        self.txt_name = QLineEdit(self)
        self.txt_name.move(50, 190)
        self.txt_name.setStyleSheet("font-weight: bold; color: black; font-family: century gothic; font-size: 16px")
        self.txt_name.setMinimumSize(300, 30)

        # Label email
        self.lbl_email = QLabel("Correo electrónico", self)
        self.lbl_email.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lbl_email.move(50, 230)
        self.lbl_email.setMinimumSize(300, 30)

        # Text field EMAIL
        self.txt_email = QLineEdit(self)
        self.txt_email.move(50, 270)
        self.txt_email.setStyleSheet("font-weight: bold; color: black; font-family: century gothic; font-size: 16px")
        self.txt_email.setMinimumSize(300, 30)

        # Label username
        self.lbl_username = QLabel("Usuario", self)
        self.lbl_username.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lbl_username.move(50, 310)

        # Text field USERNAME
        self.txt_username = QLineEdit(self)
        self.txt_username.move(50, 350)
        self.txt_username.setStyleSheet("font-weight: bold; color: black; font-family: century gothic; font-size: 16px")
        self.txt_username.setMinimumSize(300, 30)

        # Label password
        self.lbl_password = QLabel("Contraseña", self)
        self.lbl_password.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lbl_password.move(50, 390)
        self.lbl_password.setMinimumSize(300, 35)

        # Text field Password
        self.txt_password = QLineEdit(self)
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.move(50, 430)
        self.txt_password.setStyleSheet("font-weight: bold; color: black; font-family: century gothic; font-size: 16px")
        self.txt_password.setMinimumSize(300, 30)

        # Label confirm password
        self.lbl_conf_password = QLabel("Confirmar contraseña", self)
        self.lbl_conf_password.setStyleSheet(
            "font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lbl_conf_password.move(50, 470)
        self.lbl_conf_password.setMinimumSize(300, 35)

        # Text field Confirm Password
        self.txt_conf_password = QLineEdit(self)
        self.txt_conf_password.setEchoMode(QLineEdit.Password)
        self.txt_conf_password.move(50, 510)
        self.txt_conf_password.setStyleSheet(
            "font-weight: bold; color: black; font-family: century gothic; font-size: 16px")
        self.txt_conf_password.setMinimumSize(300, 30)

        # Button to register a new user
        self.btn_register = QPushButton('Registrarse', self)
        self.btn_register.resize(self.btn_register.sizeHint())
        self.btn_register.move(150, 580)
        self.btn_register.setStyleSheet(
            "background-color: #08AE9E; font-weight: bold; color: White; font-family: century gothic; font-size: 16px")
        self.btn_register.clicked.connect(self.registry_clicked)

        # Set the baackground image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Clases/images/fondo_login.png")))
        self.setPalette(palette)
        self.show()

    # Code to initialize the window centered
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    '''
    def mousePressEvent(self, *args, **kwargs):
        self.close()
    '''

    def reset_texts(self):
        self.t = OPTIONS.get(self.selected_lenguage)
        self.lbl_invalid_password.setText(self.t["invalid_password"])
        self.lbl_invalid_username.setText(self.t["invalid_username"])
        self.lbl_invalid_email.setText(self.t["invalid_email"])
        self.lbl_empty_fields.setText(self.t["empty_fields"])
        self.lb_name.setText(self.t["name"])
        self.lbl_email.setText(self.t["email"])
        self.lbl_username.setText(self.t["username"])
        self.lbl_password.setText(self.t["password"])
        self.lbl_conf_password.setText(self.t["conf_password"])
        self.btn_register.setText(self.t["register"])

    def registry_clicked(self):
        self.name = self.txt_name.text()
        self.email = self.txt_email.text()
        self.username = self.txt_username.text()
        self.password = self.txt_password.text()

        if not self.validate_empty_fields():
            if (self.txt_password.text() != self.txt_conf_password.text()):
                self.lbl_invalid_password.setVisible(True)
            else:
                data = {"method": "registry", "args": {}}
                self.password = hashlib.sha256(self.password.encode()).hexdigest()
                response = self.client.user_create(self.username, self.name, self.email, self.password)
                print(response)
                status = response["success"]
                print(status)
                if response["success"]:
                    QMessageBox.information(self, 'Battleship', 'Cuenta creada, Hola ')
                    self.close()
                else:
                    self.lbl_invalid_email.setVisible(False)
                    self.lbl_invalid_username.setVisible(False)
                    request_error = response["errors"]
                    print(request_error)
                    if request_error.find("user_email") != -1:
                        self.lbl_invalid_email.setVisible(True)
                    if request_error.find("user_username") != -1:
                        self.lbl_invalid_username.setVisible(True)
        else:
            self.lbl_empty_fields.setVisible(True)
            # False
            # {'success': False, 'errors': "Duplicate entry '' for key 'user_email'"}
            # False
            # {'success': False, 'errors': "Duplicate entry 'alan' for key 'user_username'"}

    def validate_empty_fields(self):
        return self.txt_username.text() == "" or self.txt_name.text() == "" or self.txt_email.text() == "" \
               or self.txt_password.text() == "" or self.txt_conf_password.text() == ""

    def clean(self):
        self.lbl_invalid_password.setVisible(False)
        self.lbl_invalid_username.setVisible(False)
        self.lbl_empty_fields.setVisible(False)
        self.lbl_invalid_email.setVisible(False)
        '''   self.txt_name.setText("")
                self.txt_email.setText("")
                self.txt_username.setText("")
                self.txt_password.setText("")
                self.txt_conf_password.setText("")'''
