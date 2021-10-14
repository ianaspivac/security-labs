import math

from PyQt6.QtWidgets import (QMainWindow, QTextEdit,
                             QFileDialog, QApplication, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QPushButton,
                             QCheckBox, QScrollArea, QDialogButtonBox, QLabel, QDialog, QMessageBox)
from PyQt6.QtGui import QIcon, QAction
from pathlib import Path

from parserFile import mainParse, identifyOptionKeywords
from searchOption import saveOptions, exportOptions
from verifyAudit import verifyAudit
import sys
import json


class Second(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Audit verification')

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.dialog = Second()
        self.layoutV = QVBoxLayout()

        self.searchInput = QLineEdit()
        self.btnSearch = QPushButton("Search")
        self.searchInput.setMaxLength(20)
        self.searchInput.setPlaceholderText("Search keyword...")

        self.layoutV.addWidget(self.searchInput)
        self.layoutV.addWidget(self.btnSearch)

        self.layoutH = QHBoxLayout()
        self.layoutV.addLayout(self.layoutH)

        self.textEdit = QTextEdit()

        self.layoutH.addWidget(self.textEdit)

        self.optionsBox = QVBoxLayout()
        self.widgetOptionsBox = QWidget()
        self.widgetOptionsBox.setLayout(self.optionsBox)
        self.scroll = QScrollArea()
        self.layoutH.addWidget(self.scroll)
        self.scroll.setWidget(self.widgetOptionsBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)

        self.widget = QWidget()
        self.widget.setLayout(self.layoutV)
        self.setCentralWidget(self.widget)
        self.statusBar()

        self.btnSearch.clicked.connect(self.find_word)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        saveFile = QAction(QIcon('open.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save current policy json')
        saveFile.triggered.connect(self.saveDialog)

        saveAsFile = QAction(QIcon('open.png'), 'Save As', self)
        saveAsFile.setStatusTip('Save current selection json')
        saveAsFile.triggered.connect(self.saveAsDialog)

        exportFile = QAction(QIcon('open.png'), 'Export', self)
        exportFile.setStatusTip('Export selection as audit')
        exportFile.triggered.connect(self.exportDialog)

        verifyFile = QAction(QIcon('open.png'), 'Verify audit', self)
        verifyFile.setStatusTip('Verify audit')
        verifyFile.triggered.connect(self.verifyAuditPolicy)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(saveAsFile)
        fileMenu.addAction(exportFile)
        fileMenu.addAction(verifyFile)

        self.setGeometry(200, 100, 1000, 500)
        self.setWindowTitle('File dialog')
        self.show()

    def showDialog(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            mainParse(fname[0])
            parsedFile = open(fname[0].split(".audit")[0] + ".json", 'r')
            parsed = json.loads(parsedFile.read())
            readParsedFile = json.dumps(parsed, indent=4, sort_keys=True)
            self.textEdit.setText(readParsedFile)
            self.addOptionsSelect()

    def saveDialog(self):
        home_dir = str(Path.home())
        name = QFileDialog.getSaveFileName(self, 'Save File', home_dir, "*.json")
        if name[0]:
            file = open(name[0], 'w')
            text = self.textEdit.toPlainText()
            file.write(text)
            file.close()

    def exportDialog(self):
        self.saveCheckbox()
        fileSave = exportOptions(self.listSelectedOptions, self.textEdit.toPlainText())
        home_dir = str(Path.home())
        name = QFileDialog.getSaveFileName(self, 'Export File', home_dir, "*.audit")
        if name[0]:
            file = open(name[0], 'w')
            file.write(fileSave)
            file.close()

    def saveAsDialog(self):
        self.saveCheckbox()
        fileSave = saveOptions(self.listSelectedOptions, self.textEdit.toPlainText())
        home_dir = str(Path.home())
        name = QFileDialog.getSaveFileName(self, 'Save File', home_dir, "*.json")
        if name[0]:
            file = open(name[0], 'w')
            file.write(fileSave)
            file.close()

    def verifyAuditPolicy(self):
        self.saveCheckbox()
        success, fail, countSuccess, countFail = verifyAudit(self.listSelectedOptions, self.textEdit.toPlainText())
        rate=countSuccess*100/(countSuccess+countFail)
        layout = QVBoxLayout()
        self.dialog.labelFail = QLabel(fail)
        self.dialog.labelSuccess = QLabel(success)
        self.dialog.labelRate = QLabel("Succesful rate: "+str(math.trunc(rate))+"%")
        self.dialog.labelFail.setStyleSheet("color: red")
        self.dialog.labelSuccess.setStyleSheet("color: green")
        layout.addWidget(self.dialog.labelSuccess)
        layout.addWidget(self.dialog.labelFail)
        layout.addWidget(self.dialog.labelRate)
        self.dialog.setLayout(layout)
        self.dialog.show()




    def saveCheckbox(self):
        self.listSelectedOptions = []
        for i, v in enumerate(self.listCheckBox):
            if v.isChecked():
                self.listSelectedOptions.append(v.text())

    def addOptionsSelect(self):

        self.listCheckBox = identifyOptionKeywords(self.textEdit.toPlainText())

        self.selectBtn = QPushButton("Select all")
        self.selectBtn.clicked.connect(self.selectOptions)
        self.deselectBtn = QPushButton("Deselect all")
        self.deselectBtn.clicked.connect(self.deselectOptions)
        self.optionsBox.addWidget(self.selectBtn)
        self.optionsBox.addWidget(self.deselectBtn)

        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i] = QCheckBox(v)
            self.optionsBox.addWidget(self.listCheckBox[i])

        # self.saveOptionsBtn = QPushButton("Save options")
        # self.saveOptionsBtn.clicked.connect(self.checkboxState)

        # self.optionsBox.addWidget(self.saveOptionsBtn)

    def deselectOptions(self):
        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i].setChecked(False)

    def selectOptions(self):
        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i].setChecked(True)

    def find_word(self):
        words = self.searchInput.text()
        if not self.textEdit.find(words):
            cursor = self.textEdit.textCursor()
            cursor.setPosition(0)
            self.textEdit.setTextCursor(cursor)
            self.textEdit.find(words)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
