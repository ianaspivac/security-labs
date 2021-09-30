from PyQt6.QtWidgets import (QMainWindow, QTextEdit,
                             QFileDialog, QApplication, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QPushButton,
                             QCheckBox, QGridLayout, QLabel, QScrollArea)
from PyQt6.QtGui import QIcon, QAction, QShortcut, QKeySequence
from pathlib import Path

from PyQt6.uic.properties import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QTextCursor


from parserFile import mainParse, identifyOptionKeywords
from searchOption import saveOptions
import sys
import json



class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
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
        self.widgetOptionsBox= QWidget()
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

        saveFile = QAction(QIcon('open.png'), 'Save As', self)
        saveFile.setStatusTip('Save current selection json')
        saveFile.triggered.connect(self.saveAsDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

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
        name = QFileDialog.getSaveFileName(self, 'Save File', home_dir,"*.json")
        if name[0]:
            file = open(name[0], 'w')
            text = self.textEdit.toPlainText()
            file.write(text)
            file.close()

    def saveAsDialog(self):
        self.listSelectedOptions = []
        for i, v in enumerate(self.listCheckBox):
            if v.isChecked():
                self.listSelectedOptions.append(v.text())
        fileSave = saveOptions(self.listSelectedOptions,self.textEdit.toPlainText())
        home_dir = str(Path.home())
        name = QFileDialog.getSaveFileName(self, 'Save File', home_dir,"*.json")
        if name[0]:
            file = open(name[0], 'w')
            file.write(fileSave)
            file.close()

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
