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
        print(env.toStringList())
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
        # if sys.platform.startswith("linux"):
        #     cmd += [
        #         "--no-warn-script-location",
        #         "--prefix",
        #         user_plugin_dir(),
        #     ]
        self.process.setArguments(cmd + pkg_list)
        if self._output_widget:
            self._output_widget.clear()
        self.process.start()

    def uninstall(self, pkg_list):
        args = ["-m", "pip", "uninstall", "-y"]
        self.process.setArguments(args + pkg_list)
        if self._output_widget:
            self._output_widget.clear()
        self.process.start()


class BootStrap(QWidget):
    def __init__(self):
        app = QApplication.instance()
        if not app:
            app = QApplication([])
        super().__init__()
        self.install = QPushButton("install", self)
        self.install.clicked.connect(self._install)
        self.uninstall = QPushButton("uninstall", self)
        self.uninstall.clicked.connect(self._uninstall)
        self.stdout_text = QTextEdit(self)
        self.stdout_text.setReadOnly(True)
        self.stdout_text.setObjectName("pip_install_status")
        # self.stdout_text.hide()
        layout = QVBoxLayout(self)
        layout.addWidget(self.install)
        layout.addWidget(self.uninstall)
        layout.addWidget(self.stdout_text)
        self.setLayout(layout)
        self.installer = Installer(self.stdout_text)

    def run(self):
        self.show()
        QApplication.instance().exec_()

    def _install(self):
        self.installer.install(["napari"])

    def _uninstall(self):
        self.installer.uninstall(["napari"])
