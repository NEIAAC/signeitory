import sys

from PySide6 import QtCore

from src.utils.logger import logger, qMessageHandler
from src.app import App
from src.window import Window

if __name__ == "__main__":
    with logger.catch():
        QtCore.qInstallMessageHandler(qMessageHandler)

        app = App(sys.argv)

        window = Window()
        window.show()

        sys.exit(app.exec())
