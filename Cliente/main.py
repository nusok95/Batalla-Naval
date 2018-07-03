from Clases.window_login import WindowLogin
from PyQt5.QtWidgets import QApplication
import sys

from Clases.common import ServerThread
from Clases.common import PORT
import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    server = ServerThread(host=host, port=PORT)
    server.start()
    app = QApplication(sys.argv)
    windowLogin = WindowLogin(server)
    sys.exit(app.exec_())
