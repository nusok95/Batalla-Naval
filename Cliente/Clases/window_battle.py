import sys

from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from Clases.internationalization_module import OPTIONS

import json

from PyQt5 import QtGui

from Clases.cell import Cell
from Clases.ship import Barco

from random import randint, random
import xmlrpc.client


class WindowBattle(QMainWindow):
    def __init__(self, selected_language):
        super().__init__()
        self.selected_language = selected_language
        self.init_UI()
        self.reset_text()

    def add_players(self, username, opponent):
        self.username = username
        self.opponent = opponent
        self.client = xmlrpc.client.ServerProxy("http://localhost:8000/")
        self.lbl_player.setText("Tu flota {0}".format(username))
        self.lbl_player.setMinimumSize(190, 25)
        self.counter = 0
        self.map = {}

    def init_UI(self):
        # Add core elements for the window
        self.board_local = QGridLayout()
        self.board_remote = QGridLayout()
        self.lbl_battle = QLabel("Batalla ", self)
        self.lbl_battle.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 29px")
        self.lbl_battle.move(450, 50)
        self.img_logo = QLabel(self)
        self.pixmap = QPixmap("Clases/images/imgTitle.png")
        self.img_logo.setPixmap(self.pixmap)
        self.img_logo.move(550, 5)
        self.img_logo.setMinimumSize(100, 100)
        self.lbl_naval = QLabel("Naval ", self)
        self.lbl_naval.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 29px")
        self.lbl_naval.move(650, 50)

        # Add button to locate ships randomize
        self.btn_randomize = QPushButton('Reacomodar', self)
        self.btn_randomize.resize(102, 26)
        self.btn_randomize.move(240, 575)
        self.btn_randomize.setStyleSheet(
            "background-color: #08AE9E; font-weight: bold; color: White; font-family: century gothic; font-size: 12px")
        self.btn_randomize.clicked.connect(self.button_random)
        self.btn_randomize.setVisible(True)

        self.lbl_leave = QLabel("Abandonar partida", self)
        self.lbl_leave.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 17px")
        self.lbl_leave.move(1005, 92)
        self.lbl_leave.setMinimumSize(300, 35)

        # Code to initialize the grid
        self.cells_local = []
        self.cells_remote = []

        for i in range(10):
            self.cells_local.append([0] * 10)
            self.cells_remote.append([0] * 10)

        self.init_board_local()
        # self.initBoardVs()

        # Add button 'iniciar juego'
        self.btn_start = QPushButton('Iniciar juego', self)
        self.btn_start.resize(self.btn_start.sizeHint())
        self.btn_start.move(840, 480)
        self.btn_start.setStyleSheet(
            "background-color: #08AE9E; font-weight: bold; color: White; font-family: century gothic; font-size: 17px")
        self.setFixedSize(1200, 650)
        self.center()
        self.setWindowTitle('Batalla Naval')
        self.setWindowIcon(QtGui.QIcon('Clases/images/b6.ico'))
        self.locate_ships()
        self.btn_start.clicked.connect(self.start_clicked)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Clases/images/fondo.png")))
        self.setPalette(palette)
        self.init_board_remote()
        self.show()

    def reset_text(self):
        self.t = OPTIONS.get(self.selected_language)
        self.btn_randomize.setText(self.t["randomize"])
        self.lbl_leave.setText(self.t["leave"])
        self.btn_start.setText(self.t["start"])
        self.lbl_player.setText(self.t["player"])
        self.lbl_enemy.setText(self.t["enemy"])

    # Code to initialize the window centered
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Add the local board layout to the frame
    def init_board_local(self):
        self.lbl_player = QLabel("Tu flota", self)
        self.lbl_player.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lbl_player.move(100, 150)
        self.contenedor1 = QFrame(self)
        self.contenedor1.setGeometry(100, 170, 400, 400)
        self.contenedor1.setLayout(self.board_local)
        for x in range(10):
            for y in range(10):
                cell = Cell(x, y)
                # cell.setText("{},{}".format(x,y))
                # cell.setStyleSheet("background-color: #F3F3F3")
                cell.setMinimumSize(40, 40)
                self.board_local.addWidget(cell, x, y)
                # self.cellsLocal.append(cell)
                self.cells_local[x][y] = cell
                # print (self.cellsLocal[x][y].isShip,x)

    # Add the remote board layout to the frame
    def init_board_remote(self):
        self.lbl_enemy = QLabel("Enemigo", self)
        self.lbl_enemy.setStyleSheet("font-weight: bold; color: white; font-family: century gothic; font-size: 20px")
        self.lbl_enemy.move(700, 150)
        self.lbl_enemy.show()
        # self.contenedor3.setVisible(False)
        self.contenedor2 = QFrame(self)
        self.contenedor2.setGeometry(700, 170, 400, 400)
        for x in range(10):
            for y in range(10):
                cell = Cell(x, y)
                # cell.setText("{},{}".format(x, y))
                # cell.setStyleSheet("background-color: #F3F3F3")
                cell.setMinimumSize(40, 40)
                # cell.setText("{},{}".format(x, y))
                self.board_remote.addWidget(cell, x, y)
                # self.cellsRemote.append(cell)
                self.cells_remote[x][y] = cell
                # cell.clicked.connect(self.buttonClicked)
        self.contenedor2.setLayout(self.board_remote)
        self.contenedor2.setVisible(False)

    # Add vs image to the window
    def init_Board_Vs(self):
        self.contenedor3 = QFrame(self)
        self.contenedor3.setGeometry(800, 140, 400, 400)
        '''lbl_user = QLabel("Usuario1", self)
        lbl_user.setStyleSheet("font-weight: bold; color: orange; font-family: century gothic; font-size: 22px")
        lbl_user.move(830, 230)
        lbl_enemy = QLabel("Usuario2", self)
        lbl_enemy.setStyleSheet("font-weight: bold; color: orange; font-family: century gothic; font-size: 22px")
        lbl_enemy.move(830, 430)'''
        self.imgVS = QLabel(self)
        self.pixmap2 = QPixmap("Clases/images/b3.png")
        self.imgVS.setPixmap(self.pixmap2)
        self.board_remote.addWidget(self.imgVS)
        # self.imgVS.move(900,700)
        self.contenedor3.setLayout(self.board_remote)

    def start_clicked(self, e):
        # Start the game
        self.client.update_state_and_start_game(self.username, self.opponent)

    def button_random(self, e):
        self.delete_ships()
        self.locate_ships()

#Function to restart the board without ships
    def delete_ships(self):
        for x in range(10):
            for y in range(10):
                self.cells_local[x][y].setStyleSheet("background-color: ##F3F3F3")
                self.cells_local[x][y].isShip = False

    # Add ships to the frame without overlapping
    def locate_ships(self):
        Ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.map = {}
        for i in ships:
            vertical = randint(0, 1)
            # overlap variable helps to make ships non-overlapping
            overlap = True
            while overlap:
                overlap = False
                if vertical:
                    y = randint(0, 9 - i + 1)
                    x = randint(0, 9)
                    for j in range(i):
                        if self.cells_local[x][y + j].isShip == True:
                            overlap = True
                            self.map[(x, y + j)] = True
                    if not overlap:
                        # place ship in position
                        for j in range(i):
                            self.cells_local[x][y + j].isShip = True
                            self.map[(x, y + j)] = True
                            self.cells_local[x][y + j].setStyleSheet("background-color: #42A5F5")
                else:
                    # ship will lie horizontally
                    x = randint(0, 9 - i + 1)
                    y = randint(0, 9)
                    for j in range(i):
                        if self.cells_local[x + j][y].isShip == True:
                            overlap = True
                            self.map[(x, y + j)] = True
                    if not overlap:
                        for j in range(i):
                            self.cells_local[x + j][y].isShip = True
                            self.map[(x, y + j)] = True
                            self.cells_local[x + j][y].setStyleSheet("background-color: #42A5F5")
#Function to return every cell to the other client
    def get_map(self):
        map = []
        for row in self.cells_local:
            for cell in row:
                x = cell.x
                y = cell.y
                is_ship = cell.isShip
                obj = {"x": x, "y": y, "is_ship": is_ship}
                map.append(obj)
        return map
#Function to set the rival's board
    def set_map(self, map):
        # map = [{x:1, y:1, is_ship: True]}, {x:1, y:2, is_ship: False]}]
        map = json.loads(map)
        print(self.cells_remote)
        for cell in map:
            remote_cell = self.cells_remote[cell["x"]][cell["y"]]
            remote_cell.isShip = cell["is_ship"]
            remote_cell.clicked.connect(self.verify_cell)

        # for row in self.cells_remote:
        #     for cell in row:
        #         x = cell.x
        #         y = cell.y
        #         cell.isShip = map[str(x)][str(y)]
        self.active_board(False)
        self.contenedor2.show()
        self.btn_start.setVisible(False)
        self.btn_randomize.setVisible(False)

    #Function to verify if the cell hit is a ship or not and if the game is finished
    def verify_cell(self):
        cell = self.sender()
        if cell.isShip:
            cell.setStyleSheet("background-color: green")
            self.counter += 1
        else:
            cell.setStyleSheet("background-color: red")
        if self.counter == 20:
            # implement method to win
            QMessageBox.information(self, 'Battleship', 'Has Ganado!')
            # self.client.user_logout(self.username)
            # self.client.user_logout(self.opponent)
            return 0
        self.active_board(False)
        cell = {"x": cell.x, "y": cell.y, "is_ship": cell.isShip}
        self.client.send_info_to_opponent(self.opponent, cell)
        # implement method to send data to the opponent≤

    def active_board(self, boolean):
        for row in self.cells_remote:
            for cell in row:
                cell.setEnabled(boolean)

    # Recive a shoot and show in the board
    def received_shoot(self, cell):
        print(type(cell))
        x = cell["x"]
        y = cell["y"]
        is_ship = cell["is_ship"]
        if is_ship:
            self.cells_local[x][y].setStyleSheet("background-color: green")
        else:
            self.cells_local[x][y].setStyleSheet("background-color: red")
