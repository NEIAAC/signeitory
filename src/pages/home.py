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
    SmoothMode,
    TextBrowser,
    InfoBar,
    InfoBarPosition,
    ColorSettingCard,
    FlowLayout,
    DoubleSpinBox,
    SpinBox,
    ComboBox,
)

from app import App
from services.write import WriterThread
from utils import file_loader
from utils.data_saver import config


class HomePage(QWidget):
    worker: WriterThread | None = None

    def __init__(self):
        super().__init__()
        self.setObjectName("Home")

        self.finishSound = QSoundEffect()
        self.finishSound.setSource(
            QUrl.fromLocalFile(file_loader.loadResource("sounds/success.wav"))
        )
        self.finishSound.setVolume(0.1)

        self.xCoordinateLabel = BodyLabel("<b>X COORDINATE</b>")
        self.xCoordinateInput = DoubleSpinBox()
        self.xCoordinateInput.setValue(50.0)
        self.xCoordinateInput.setFixedWidth(200)
        self.xCoordinateInput.setMaximum(9999)
        self.xCoordinateLayout = QVBoxLayout()
        self.xCoordinateLayout.setSpacing(10)
        self.xCoordinateLayout.addWidget(self.xCoordinateLabel)
        self.xCoordinateLayout.addWidget(self.xCoordinateInput)

        self.yCoordinateLabel = BodyLabel("<b>Y COORDINATE</b>")
        self.yCoordinateInput = DoubleSpinBox()
        self.yCoordinateInput.setValue(50.0)
        self.yCoordinateInput.setFixedWidth(200)
        self.yCoordinateInput.setMaximum(9999)
        self.yCoordinateLayout = QVBoxLayout()
        self.yCoordinateLayout.setSpacing(10)
        self.yCoordinateLayout.addWidget(self.yCoordinateLabel)
        self.yCoordinateLayout.addWidget(self.yCoordinateInput)

        self.rotationLabel = BodyLabel("<b>ROTATION</b>")
        self.rotationInput = ComboBox()
        for rotation in ["0", "90", "180", "270"]:
            self.rotationInput.addItem(rotation, userData=int(rotation))
        self.rotationInput.setCurrentIndex(0)
        self.rotationInput.setFixedWidth(200)
        self.rotationLayout = QVBoxLayout()
        self.rotationLayout.setSpacing(10)
        self.rotationLayout.addWidget(self.rotationLabel)
        self.rotationLayout.addWidget(self.rotationInput)

        self.sizeLabel = BodyLabel("<b>SIZE</b>")
        self.sizeInput = DoubleSpinBox()
        self.sizeInput.setFixedWidth(200)
        self.sizeInput.setMinimum(1)
        self.sizeInput.setMaximum(9999)
        self.sizeInput.setValue(config.textSize.get())  # type: ignore
        self.sizeInput.setStepType(SpinBox.StepType.AdaptiveDecimalStepType)
        self.sizeInput.textChanged.connect(
            lambda text: config.textSize.set(float(text))  # type: ignore
        )
        self.sizeLayout = QVBoxLayout()
        self.sizeLayout.setSpacing(10)
        self.sizeLayout.addWidget(self.sizeLabel)
        self.sizeLayout.addWidget(self.sizeInput)

        self.pageNumberLabel = BodyLabel("<b>PAGE NUMBER</b>")
        self.pageNumberInput = SpinBox()
        self.pageNumberInput.setFixedWidth(200)
        self.pageNumberInput.setMinimum(0)
        self.pageNumberInput.setValue(0)
        self.pageNumberLayout = QVBoxLayout()
        self.pageNumberLayout.setSpacing(10)
        self.pageNumberLayout.addWidget(self.pageNumberLabel)
        self.pageNumberLayout.addWidget(self.pageNumberInput)

        self.inputsLayout = FlowLayout()
        self.inputsLayout.setVerticalSpacing(20)
        self.inputsLayout.setHorizontalSpacing(20)
        self.inputsLayout.addItem(self.xCoordinateLayout)
        self.inputsLayout.addItem(self.yCoordinateLayout)
        self.inputsLayout.addItem(self.rotationLayout)
        self.inputsLayout.addItem(self.sizeLayout)
        self.inputsLayout.addItem(self.pageNumberLayout)

        self.colorLabel = BodyLabel("<b>COLOR</b>")
        self.colorInput = ColorSettingCard(
            config.textColor,  # type: ignore
            FluentIcon.PENCIL_INK,
            "Use the box on the right to pick a color!",
        )
        self.colorInput.setFixedWidth(425)
        self.colorLayout = QVBoxLayout()
        self.colorLayout.setSpacing(10)
        self.colorLayout.addWidget(self.colorLabel)
        self.colorLayout.addWidget(self.colorInput)

        self.fontLabel = BodyLabel("<b>FONT FILE</b>")
        self.fontFileInput = LineEdit()
        self.fontFileInput.setMaximumWidth(500)
        self.fontFileInput.setReadOnly(True)
        self.fontFileInput.setPlaceholderText("No font file selected.")
        self.fontFileDialog = QFileDialog()
        self.fontFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.fontFilePickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.fontFilePickButton.clicked.connect(
            lambda: self.fontFileInput.setText(
                self.fontFileDialog.getOpenFileName(
                    self, "Select a font file!"
                )[0]
            )
        )
        self.fontContentLayout = QHBoxLayout()
        self.fontContentLayout.setSpacing(10)
        self.fontContentLayout.addWidget(self.fontFilePickButton)
        self.fontContentLayout.addWidget(self.fontFileInput)
        self.fontLayout = QVBoxLayout()
        self.fontLayout.setSpacing(10)
        self.fontLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.fontLayout.addWidget(self.fontLabel)
        self.fontLayout.addLayout(self.fontContentLayout)

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
                self.runLogsBox.clear(),  # type: ignore
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
        self.contentLayout.addLayout(self.inputsLayout)
        self.contentLayout.addLayout(self.colorLayout)
        self.contentLayout.addLayout(self.fontLayout)
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
        self.scrollArea.setSmoothMode(SmoothMode.NO_SMOOTH)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)

    def runWriter(self):
        """Runs the document text writer logic for this page."""

        if self.worker is not None and self.worker.isRunning():
            return

        schema = {
            "X Coordinate": self.xCoordinateInput.value(),
            "Y Coordinate": self.yCoordinateInput.value(),
            "Rotation": self.rotationInput.itemData(
                self.rotationInput.currentIndex()
            ),
            "Size": self.sizeInput.value(),
            "Page number": self.pageNumberInput.value(),
            "Color": self.colorInput.colorPicker.color,
            "Font path": self.fontFileInput.text(),
            "Document path": self.documentFileInput.text(),
            "Table path": self.tableFileInput.text(),
            "Output folder": self.outputFolderInput.text(),
        }
        for input in schema:
            if schema[input] is None or schema[input] == "":
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

        self.worker = WriterThread(
            self.xCoordinateInput.value(),
            self.yCoordinateInput.value(),
            self.sizeInput.value(),
            self.rotationInput.itemData(self.rotationInput.currentIndex()) or 0,
            self.pageNumberInput.value(),
            (
                self.colorInput.colorPicker.color.redF(),
                self.colorInput.colorPicker.color.greenF(),
                self.colorInput.colorPicker.color.blueF(),
            ),
            self.fontFileInput.text(),
            self.documentFileInput.text(),
            self.tableFileInput.text(),
            self.outputFolderInput.text(),
        )

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
            # if (
            #     App.applicationState()
            #     == Qt.ApplicationState.ApplicationInactive
            # ):
            #     SystemTray().send(
            #         "Text written!",
            #         "Go to the output folder to see the results.",
            #     )
            self.finishSound.play()

        self.worker.finished.connect(finished)
        self.worker.start()
