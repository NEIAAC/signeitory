from src.window import Window

from pytestqt.qt_compat import qt_api as qtapi


def testWindow(qtbot):
    """
    Simple test to ensure we are setting up the Window correctly.
    """
    assert qtapi.QtWidgets.QApplication.instance() is not None
    window = Window()
    qtbot.addWidget(window)
    window.setWindowTitle("W1")
    window.show()

    assert window.isVisible()
    assert window.windowTitle() == "W1"
