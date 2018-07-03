from PyQt5.QtWidgets import QPushButton


class Cell(QPushButton):
    def __init__(self, x, y):
        super(QPushButton, self).__init__()
        self.x = x
        self.y = y
        self.isShip = False

    def __str__(self):
        return "x: {0} y: {1} isShip: {2}".format(self.x, self.y, self.isShip)

    def __unicode__(self):
        return "x: {0} y: {1} isShip: {2}".format(self.x, self.y, self.isShip)
