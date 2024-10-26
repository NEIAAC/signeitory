from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QSizePolicy,
)
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import Qt, QUrl
from qfluentwidgets import (
    LineEdit,
    BodyLabel,
    PrimaryToolButton,
    FluentIcon,
    SingleDirectionScrollArea,
    TextBrowser,
    InfoBar,
    InfoBarPosition,
)

from app import App
from logic.write import WriterThread
from utils import loader
from utils.system_tray import SystemTray


class HomePage(QWidget):
    worker: WriterThread | None = None

    def __init__(self):
        super().__init__()
        self.setObjectName("Home")

        self.finishSound = QSoundEffect()
        self.finishSound.setSource(
            QUrl.fromLocalFile(loader.resources("sounds/success.wav"))
        )
        self.finishSound.setVolume(0.1)

        self.documentLabel = BodyLabel("<b>DOCUMENT FILE</b>")
        self.documentPicker = QFileDialog()
        self.documentPicker.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.documentFileInput = LineEdit()
        self.documentFileInput.setMaximumWidth(500)
        self.documentFileInput.setReadOnly(True)
        self.documentFileInput.setPlaceholderText("No document file selected.")
        self.documentFileDialog = QFileDialog()
        self.documentFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.documentFilePickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.documentFilePickButton.clicked.connect(
            lambda: self.documentFileInput.setText(
                self.documentFileDialog.getOpenFileName(
                    self, "Select a document file!"
                )[0]
            )
        )
        self.documentContentLayout = QHBoxLayout()
        self.documentContentLayout.setSpacing(10)
        self.documentContentLayout.addWidget(self.documentFilePickButton)
        self.documentContentLayout.addWidget(self.documentFileInput)
        self.documentLayout = QVBoxLayout()
        self.documentLayout.setSpacing(10)
        self.documentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.documentLayout.addWidget(self.documentLabel)
        self.documentLayout.addLayout(self.documentContentLayout)

        self.tableLabel = BodyLabel("<b>VARIABLE TABLE FILE</b>")
        self.tableFileInput = LineEdit()
        self.tableFileInput.setReadOnly(True)
        self.tableFileInput.setMaximumWidth(500)
        self.tableFileInput.setPlaceholderText("No table file selected.")
        self.tableFileDialog = QFileDialog()
        self.tableFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.tableFilePickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.tableFilePickButton.clicked.connect(
            lambda: self.tableFileInput.setText(
                self.tableFileDialog.getOpenFileName(
                    self, "Select a table file!"
                )[0]
            )
        )
        self.tableContentLayout = QHBoxLayout()
        self.tableContentLayout.setSpacing(10)
        self.tableContentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tableContentLayout.addWidget(self.tableFilePickButton)
        self.tableContentLayout.addWidget(self.tableFileInput)
        self.tableLayout = QVBoxLayout()
        self.tableLayout.setSpacing(10)
        self.tableLayout.addWidget(self.tableLabel)
        self.tableLayout.addLayout(self.tableContentLayout)

        self.outputLabel = BodyLabel("<b>OUTPUT DIRECTORY</b>")
        self.outputFolderInput = LineEdit()
        self.outputFolderInput.setReadOnly(True)
        self.outputFolderInput.setMaximumWidth(500)
        self.outputFolderInput.setPlaceholderText("No output folder selected.")
        self.outputFileDialog = QFileDialog()
        self.outputFileDialog.setFileMode(QFileDialog.FileMode.Directory)
        self.outputFolderPickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.outputFolderPickButton.clicked.connect(
            lambda: self.outputFolderInput.setText(
                self.outputFileDialog.getExistingDirectory(
                    self, "Select a directory to store the output files!"
                )
            )
        )
        self.outputContentLayout = QHBoxLayout()
        self.outputContentLayout.setSpacing(10)
        self.outputContentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.outputContentLayout.addWidget(self.outputFolderPickButton)
        self.outputContentLayout.addWidget(self.outputFolderInput)
        self.outputLayout = QVBoxLayout()
        self.outputLayout.setSpacing(10)
        self.outputLayout.addWidget(self.outputLabel)
        self.outputLayout.addLayout(self.outputContentLayout)

        self.runLogsBox = TextBrowser()
        self.runLogsBox.setHtml("")
        self.runLogsBox.setMinimumHeight(150)
        self.runLogsBox.setMaximumHeight(300)
        self.runLogsBox.setReadOnly(True)
        self.runLogsBox.setPlaceholderText(
            "Press the start button on the left to begin. \
            \nLog output from the run will be shown here. \
            \nThe trash can button will clear this box."
        )
        self.runButton = PrimaryToolButton(FluentIcon.PLAY)
        self.runButton.setFixedWidth(100)
        self.runButton.clicked.connect(self.runWriter)
        self.runLogsClearButton = PrimaryToolButton(FluentIcon.DELETE)
        self.runLogsClearButton.setDisabled(True)
        self.runLogsClearButton.setFixedWidth(100)
        self.runLogsClearButton.clicked.connect(
            lambda: (
                self.runLogsBox.clear(),
                self.runLogsClearButton.setDisabled(True),
            )
        )
        self.runButtonLayout = QVBoxLayout()
        self.runButtonLayout.setSpacing(10)
        self.runButtonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.runButtonLayout.addWidget(self.runButton)
        self.runButtonLayout.addWidget(self.runLogsClearButton)
        self.runContentLayout = QHBoxLayout()
        self.runContentLayout.setSpacing(10)
        self.runContentLayout.addLayout(self.runButtonLayout)
        self.runContentLayout.addWidget(self.runLogsBox)

        self.contentLayout = QVBoxLayout()
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(40, 40, 50, 40)
        self.contentLayout.setSpacing(40)
        # self.contentLayout.addLayout(self.smtpLayout)
        # self.contentLayout.addLayout(self.headLayout)
        self.contentLayout.addLayout(self.documentLayout)
        self.contentLayout.addLayout(self.tableLayout)
        self.contentLayout.addLayout(self.outputLayout)
        self.contentLayout.addLayout(self.runContentLayout)
        self.contentWidget = QWidget()
        self.contentWidget.setLayout(self.contentLayout)

        self.scrollArea = SingleDirectionScrollArea(
            orient=Qt.Orientation.Vertical
        )
        self.scrollArea.setWidget(self.contentWidget)
        self.scrollArea.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.enableTransparentBackground()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)

    def runWriter(self):
        """Runs the document text writer logic for this page."""

        if self.worker is not None and self.worker.isRunning():
            return

        schema = {
            "Font path": self.fontFileInput.text(),
            "Document path": self.documentFileInput.text(),
            "Table path": self.tableFileInput.text(),
            "Output folder": self.outputFolderInput.text(),
        }
        for input in schema:
            if not schema[input]:
                InfoBar.error(
                    title=f"{input} field cannot be empty!",
                    content="",
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=4000,
                    parent=self,
                )
                return

        self.runButton.setDisabled(True)

        self.worker = WriterThread("Hello World!")

        def output(text, level):
            if level == "ERROR":
                self.runLogsBox.append(f'<font color="red">{text}</font>')
            else:
                self.runLogsBox.append(f'<font color="green">{text}</font>')
            self.runLogsClearButton.setDisabled(False)

        self.worker.outputSignal.connect(output)

        def finished():
            self.runButton.setDisabled(False)
            App.alert(self, 0)
            if (
                App.applicationState()
                == Qt.ApplicationState.ApplicationInactive
            ):
                SystemTray().send(
                    "Text written!",
                    "Go to the output folder to see the results.",
                )
            self.finishSound.play()

        self.worker.finished.connect(finished)
        self.worker.start()
