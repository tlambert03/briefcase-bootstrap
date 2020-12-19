from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
import traceback
import sys


class ErrorDialog(QWidget):
    def __init__(self, exception: Exception):
        app = QApplication.instance()
        if not app:
            app = QApplication([])
        super().__init__()
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text)
        self.setLayout(layout)
        self.text.append("Sorry an error occured:\n\n")
        self.text.append(
            "Please report at https://github.com/napari/napari/issues/new/choose\n\n"
        )
        self.text.append(traceback.format_exc())
        self.resize(600, 500)

    def run(self):
        self.show()
        QApplication.instance().exec_()
