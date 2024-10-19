import sys

from utils.logger import logger, qMessageHandler
from app import App
from PySide6 import QtCore
from window import Window

if __name__ == "__main__":
    with logger.catch():
        QtCore.qInstallMessageHandler(qMessageHandler)

        app = App(sys.argv)

        window = Window()
        window.show()

        sys.exit(app.exec())
