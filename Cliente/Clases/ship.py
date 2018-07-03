from PyQt5.QtWidgets import QPushButton


class Barco(object):
    def __init__(self, size, name, ubication, orientation, cells):
        self.size = size
        self.name = name
        self.ubication = cells
        self.orientation = orientation
        # self.sprite = None

    def hola(self):
        print("Soy una taza " + self.nombre)
