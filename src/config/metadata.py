import os

from PySide6.QtCore import QStandardPaths

# Beware of changing these variable names as they are used in the deployment workflows to get required information
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
"""Path to store app data on the system, usually this should not need to be changed."""
