#! ./venv/bin/python
import sys, os
from lib.rust_wrap import encode, decode
from PySide6 import QtCore, QtWidgets


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        mainlayout = QtWidgets.QVBoxLayout()
        self.filepath = QtWidgets.QLineEdit()
        self.keypath = QtWidgets.QLineEdit()
        self.outputpath = QtWidgets.QLineEdit()
        self.fileButton = QtWidgets.QPushButton("Browse File")
        self.keyButton = QtWidgets.QPushButton("Browse Key")
        self.outputButton = QtWidgets.QPushButton("Create File")
        self.encodeButton = QtWidgets.QPushButton("Encode")
        self.decodeButton = QtWidgets.QPushButton("Decode")

        self.fileButton.clicked.connect(self.openFile)
        self.keyButton.clicked.connect(self.openKey)
        self.outputButton.clicked.connect(self.createFile)
        self.encodeButton.clicked.connect(self.run_encode)
        self.decodeButton.clicked.connect(self.run_decode)

        self.statusBox = QtWidgets.QTextEdit()
        self.statusBox.setEnabled(False)

        self.createGroup([[self.filepath, self.fileButton], 
                          [self.keypath, self.keyButton], 
                          [self.outputpath, self.outputButton]])

        self.createButtonBox([self.encodeButton, self.decodeButton])

        mainlayout.addWidget(self._box)
        mainlayout.addWidget(self._bbox)
        mainlayout.addWidget(self.statusBox)


        self.setLayout(mainlayout)

    def createButtonBox(self, order: list):
        self._bbox = QtWidgets.QGroupBox()
        main = QtWidgets.QHBoxLayout()
        for b in order:
            main.addWidget(b)
        self._bbox.setLayout(main)
        
    def createGroup(self, order : list):
        self._box = QtWidgets.QGroupBox("File Locations")
        main = QtWidgets.QFormLayout()
        for row in order:
            main.addRow(*row)

        self._box.setLayout(main)
            
    def clear_input(self):
        self.filepath.setText("")
        self.keypath.setText("")
        self.outputpath.setText("")
    
    @QtCore.Slot()
    def run_decode(self):
        fp = self.filepath.text()
        kp = self.keypath.text()
        op = self.outputpath.text()
        if os.path.isfile(fp) and os.path.isfile(kp):
            status = decode(fp, op, kp)
            info = f"STDOUT\n{status.stdout.decode('utf-8')}\n\nSTDERR\n{status.stderr.decode('utf-8')}"
            self.statusBox.setText(info)
            self.clear_input()

    @QtCore.Slot()
    def run_encode(self):
        fp = self.filepath.text()
        kp = self.keypath.text()
        op = self.outputpath.text()
        if os.path.isfile(fp):
            status = encode(fp, op, kp)
            info = f"STDOUT\n{status.stdout.decode('utf-8')}\n\nSTDERR\n{status.stderr.decode('utf-8')}"
            self.statusBox.setText(info)
            self.clear_input()


    @QtCore.Slot()
    def createFile(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        if dlg.exec():
            self.outputpath.setText(dlg.selectedFiles()[0])

    @QtCore.Slot()
    def openFile(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)

        if dlg.exec():
            self.filepath.setText(dlg.selectedFiles()[0])

    @QtCore.Slot()
    def openKey(self):
        dlg = QtWidgets.QFileDialog() 
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        
        
        if dlg.exec():
            self.keypath.setText(dlg.selectedFiles()[0])



if __name__ == "__main__":
    DEFAULT_LOC = os.path.dirname(os.path.abspath(__file__))
    
    app = QtWidgets.QApplication([])
    with open(DEFAULT_LOC + "/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    _version = open(DEFAULT_LOC + "/version.txt", "r").readlines()[0]
    
    widget = MainWidget()
    widget.setWindowTitle("OTP TOOL V-" + _version)
 
    widget.show()

    sys.exit(app.exec())
