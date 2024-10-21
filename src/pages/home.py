from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QSoundEffect
from qfluentwidgets import (
    BodyLabel,
    LineEdit,
    PrimaryToolButton,
    FluentIcon,
    SingleDirectionScrollArea,
    PlainTextEdit,
    InfoBar,
    InfoBarPosition,
)

from src.app import App
from src.logic.write import WriterThread
from src.utils.config import config
from src.utils.system_tray import SystemTray
from src.utils import loader


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Home")

        self.finishSound = QSoundEffect()
        self.finishSound.setSource(
            QUrl.fromLocalFile(loader.resources("sounds/success.wav"))
        )
        self.finishSound.setVolume(0.2)

        self.inputLabel = BodyLabel("INPUT")
        self.inputField = LineEdit()
        self.inputField.setMaximumWidth(500)
        self.inputField.setPlaceholderText("This is a placeholder!")
        self.inputField.textChanged.connect(lambda text: config.input.set(text))
        self.inputField.setText(config.input.get())

        self.inputLayout = QVBoxLayout()
        self.inputLayout.setSpacing(10)
        self.inputLayout.addWidget(self.inputLabel)
        self.inputLayout.addWidget(self.inputField)

        self.outputBox = PlainTextEdit()
        self.outputBox.setMinimumHeight(150)
        self.outputBox.setReadOnly(True)
        self.outputBox.setPlaceholderText("Progress will be shown here.")

        self.outputClearButton = PrimaryToolButton(FluentIcon.DELETE)
        self.outputClearButton.setDisabled(True)
        self.outputClearButton.clicked.connect(self.outputBox.clear)

        self.outputButtonLayout = QVBoxLayout()
        self.outputButtonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.outputButtonLayout.setSpacing(10)
        self.outputButtonLayout.addWidget(self.outputClearButton)

        self.outputLayout = QHBoxLayout()
        self.outputLayout.setSpacing(10)
        self.outputLayout.addLayout(self.outputButtonLayout)
        self.outputLayout.addWidget(self.outputBox)

        self.startButton = PrimaryToolButton(FluentIcon.PLAY)
        self.startButton.setFixedWidth(100)

        self.worker = None
        self.startButtonLayout = QHBoxLayout()
        self.startButtonLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.startButtonLayout.addWidget(self.startButton)
        self.startButton.clicked.connect(self.runWriter)

        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(40, 40, 50, 40)
        self.contentLayout.setSpacing(40)
        self.contentLayout.addLayout(self.inputLayout)
        self.contentLayout.addLayout(self.outputLayout)
        self.contentLayout.addLayout(self.startButtonLayout)

        self.scrollArea = SingleDirectionScrollArea(
            orient=Qt.Orientation.Vertical
        )
        self.scrollArea.setWidget(self.contentWidget)
        self.scrollArea.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        self.scrollArea.horizontalScrollBar().setVisible(False)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.enableTransparentBackground()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)

    def runWriter(self):
        """Runs the example logic for this page."""
        if self.worker is not None and self.worker.isRunning():
            return
        if not self.inputField.text():
            InfoBar.error(
                title="Input field is empty!",
                content="",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=4000,
                parent=self,
            )
            return
        self.startButton.setDisabled(True)
        self.worker = WriterThread(self.inputField.text())
        self.worker.outputSignal.connect(
            lambda text: (
                self.outputBox.appendPlainText(text),
                self.outputClearButton.setDisabled(False),
            )
        )

        def finished():
            self.startButton.setDisabled(False)
            App.alert(self, 0)
            if (
                App.applicationState()
                == Qt.ApplicationState.ApplicationInactive
            ):
                SystemTray().send("Example finished!", "Go back to the app.")
            self.finishSound.play()

        self.worker.finished.connect(finished)
        self.worker.start()
