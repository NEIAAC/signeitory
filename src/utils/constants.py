import os

from PySide6.QtCore import QStandardPaths

EXECUTABLE_NAME = "Signeitory"
AUTHOR_NAME = "NEIAAC"
AUTHOR_DOMAIN = "neiaac.com"
LOGO_PATH = "icons/logo.png"
DATA_PATH = os.path.join(
    QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.GenericConfigLocation
    ),
    AUTHOR_NAME,
    EXECUTABLE_NAME,
)
