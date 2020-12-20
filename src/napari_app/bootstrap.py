import os
import site
import sys

from PySide2.QtCore import QProcess, QProcessEnvironment
from PySide2.QtWidgets import QApplication, QPushButton, QTextEdit, QWidget, QVBoxLayout


class Installer:
    def __init__(self, output_widget: QTextEdit = None):

        # create install process
        self._output_widget = None
        self.process = QProcess()
        self.process.setProgram(sys.executable)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self._on_stdout_ready)
        # setup process path
        env = QProcessEnvironment()
        combined_paths = os.pathsep.join(
            [site.getsitepackages()[0], env.systemEnvironment().value("PYTHONPATH")]
        )
        env.insert("PATH", QProcessEnvironment.systemEnvironment().value("PATH"))
        env.insert("PYTHONPATH", combined_paths)
        self.process.setProcessEnvironment(env)
        self.set_output_widget(output_widget)

    def set_output_widget(self, output_widget: QTextEdit):
        if output_widget:
            self._output_widget = output_widget
            self.process.setParent(output_widget)

    def _on_stdout_ready(self):
        if self._output_widget:
            text = self.process.readAllStandardOutput().data().decode()
            self._output_widget.append(text)

    def install(self, pkg_list):
        cmd = ["-m", "pip", "install", "--upgrade"]
        self.process.setArguments(cmd + pkg_list)
        if self._output_widget:
            self._output_widget.clear()
        self.process.start()


class BootStrap(QWidget):
    def __init__(self):
        app = QApplication.instance()
        if not app:
            app = QApplication([])
        super().__init__()
        self.install = QPushButton("install napari", self)
        self.install.clicked.connect(self._install)
        self.stdout_text = QTextEdit(self)
        self.stdout_text.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.install)
        layout.addWidget(self.stdout_text)
        self.setLayout(layout)
        self.installer = Installer(self.stdout_text)

    def run(self):
        self.show()
        QApplication.instance().exec_()

    def _install(self):

        def restart():
            self.stdout_text.append("rebooting...")
            QApplication.instance().quit()
            os.execl(sys.executable, 'python', *sys.argv)

        self.installer.process.finished.connect(restart)
        self.installer.install(["napari"])
