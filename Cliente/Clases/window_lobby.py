from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
import xmlrpc.client
from Clases.cell import Cell
from Clases.ship import Barco
from Clases.window_battle import WindowBattle
from Clases.internationalization_module import OPTIONS
import time
from Clases.common import ServerThread
from Clases.common import PORT
import socket
import json


class WindowLobby(QMainWindow):
    def __init__(self, username, connected_users, server, selected_language):
        super().__init__()
        self.username = username
        self.connected = connected_users
        self.server = server
        self.server.add_function(self.update_list)
        self.server.add_function(self.start_battle)
        self.server.add_function(self.get_map)
        self.server.add_function(self.set_map)
        self.server.add_function(self.activate_board)
        self.server.add_function(self.received_shoot)
        self.server.add_function(self.close_application)
        self.client = xmlrpc.client.ServerProxy("http://localhost:8000/")
        self.selected_lenguage = selected_language
        self.init_UI()
        self.reset_texts()
        self.show()

    def init_UI(self):
        # Add core elements for the window
        self.lbl_tittle1 = QLabel("Batalla ", self)
        self.lbl_tittle1.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 29px")
        self.lbl_tittle1.move(450, 50)
        self.img_logo = QLabel(self)
        pixmap = QPixmap("Clases/images/imgTitle.png")
        self.img_logo.setPixmap(pixmap)
        self.img_logo.move(550, 5)
        self.img_logo.setMinimumSize(100, 100)
        self.lbl_tittle2 = QLabel("Naval ", self)
        self.lbl_tittle2.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 29px")
        self.lbl_tittle2.move(650, 50)

        # Button score
        self.btn_score = QPushButton('Ver puntuación', self)
        self.btn_score.resize(350, 60)
        self.btn_score.move(370, 250)
        self.btn_score.setStyleSheet(
            "background-color: #08AE9E; font-weight: bold; color: White; font-family: century gothic; font-size: 18px")

        # Button Log out
        self.btn_logout = QPushButton('Cerrar Sesión', self)
        self.btn_logout.resize(350, 60)
        self.btn_logout.move(370, 450)
        self.btn_logout.setStyleSheet(
            "background-color: #08AE9E; font-weight: bold; color: White; font-family: century gothic; font-size: 18px")
        self.btn_logout.clicked.connect(self.logout_clicked)

        # Button Send
        self.btn_send = QPushButton("Enviar", self)
        self.btn_send.resize(165, 35)
        self.btn_send.move(900, 580)
        self.btn_send.setStyleSheet(
            "background-color: #08AE9E; font-weight: bold; color: White; font-family: century gothic; font-size: 16px")
        self.btn_send.clicked.connect(self.play_clicked)

        # LabeL username
        self.lbl_username = QLabel(self.username, self)
        self.lbl_username.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 17px")
        self.lbl_username.move(1130, 95)

        # Label FRIENDS
        self.lbl_friends = QLabel("Amigos", self)
        self.lbl_friends.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 18px")
        self.lbl_friends.move(900, 133)

        # ListWidget list friends
        self.list_friends = QListWidget(self)
        self.list_friends.move(900, 170)
        self.list_friends.setMinimumSize(250, 400)
        self.list_friends.setStyleSheet(
            "background-color: #0277bd; font-weight: bold; color: White; font-family: century gothic; font-size: 15px")
        # "background-color: WHITE; font-weight: bold; color: BLACK; font-family: century gothic; font-size: 15px")

        # This window
        self.setFixedSize(1200, 650)
        self.center()
        self.setWindowTitle('Batalla Naval')
        self.setWindowIcon(QtGui.QIcon('Clases/images/b6.ico'))

        # Set the baackground image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Clases/images/fondo.png")))
        self.setPalette(palette)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_list)
        # self.timer.start(3000)
        self.windowGame = WindowBattle(self.selected_lenguage)
        self.windowGame.hide()
        self.show()

    def reset_texts(self):
        self.t = OPTIONS.get(self.selected_lenguage)
        self.btn_score.setText(self.t["score"])
        self.btn_logout.setText(self.t["logout"])
        self.btn_send.setText(self.t["send"])
        # self.lbl_exit.setText(self.t["exit"])
        self.lbl_friends.setText(self.t["friends"])

    # Code to initialize the window centered
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def play_clicked(self):
        opponent = self.list_friends.currentItem().text()
        self.windowGame.show()
        self.windowGame.add_players(self.username, opponent)
        self.client.start_battle(self.username, opponent)
        self.client.update_state(opponent, "playing")
        self.client.update_state(self.username, "playing")
        self.hide()

    def logout_clicked(self):
        response = self.client.user_logout(self.username)
        print(response)
        QMessageBox.information(self, 'Events - Slot', response['message'])
        self.setVisible(False)

    def update_list(self, user_list):
        self.list_friends.clear()
        if self.username in user_list:
            user_list.remove(self.username)
        print("updating list", user_list)
        if user_list:
            self.list_friends.addItems(user_list)

    def start_battle(self, username, opponent):
        print(username, opponent)
        self.windowGame.show()
        self.windowGame.add_players(self.username, opponent)
        self.setVisible(False)
        print("Closing windows")

    def get_map(self):
        print("getting map")
        map = self.windowGame.get_map()
        print(map)
        return json.dumps(map)

    def set_map(self, map):
        self.windowGame.set_map(map)

    def activate_board(self, boolean):
        self.windowGame.active_board(boolean)

    def received_shoot(self, cell):
        self.windowGame.received_shoot(cell)

    def close_application(self):
        self.close()
