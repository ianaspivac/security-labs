from PyQt6.QtWidgets import (QMainWindow, QTextEdit,
                             QFileDialog, QApplication, QLineEdit, QVBoxLayout, QWidget, QPushButton)
from PyQt6.QtGui import QIcon, QAction, QShortcut, QKeySequence
from pathlib import Path

from PyQt6.uic.properties import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QTextCursor

from parserFile import mainParse
from searchOption import search
import sys
import json



class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.textEdit = QTextEdit()


        self.searchInput = QLineEdit()
        self.btnSearch = QPushButton("Search")
        self.searchInput.setMaxLength(20)
        self.searchInput.setPlaceholderText("Search keyword...")


        self.layout.addWidget(self.searchInput)
        self.layout.addWidget(self.btnSearch)
        self.layout.addWidget(self.textEdit)



        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.statusBar()

        self.btnSearch.clicked.connect(self.find_word)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

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


    def find_word(self):
        words = self.searchInput.text()
        if not self.textEdit.find(words):
            cursor = self.textEdit.textCursor()
            cursor.setPosition(0)
            self.textEdit.setTextCursor(cursor)
            self.textEdit.find(words)
    def Find_word(self):
        self.findDialog = QtWidgets.QDialog(self)

        label = QtWidgets.QLabel("Find Word:")
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setText(self.lastSearchText)
        label.setBuddy(self.lineEdit)

        self.findButton = QtWidgets.QPushButton("Find Next")
        self.findButton.setDefault(True)
        self.findButton.clicked.connect(self.searchText)

        buttonBox = QtWidgets.QDialogButtonBox(QtCore.Qt.Vertical)
        buttonBox.addButton(self.findButton, QtWidgets.QDialogButtonBox.ActionRole)

        topLeftLayout = QtWidgets.QHBoxLayout()
        topLeftLayout.addWidget(label)
        topLeftLayout.addWidget(self.lineEdit)

        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.addLayout(topLeftLayout)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addWidget(buttonBox, 0, 1)
        mainLayout.setRowStretch(2, 1)
        self.findDialog.setLayout(mainLayout)

        self.findDialog.setWindowTitle("Find")
        self.findDialog.show()

    def searchText(self):
        cursor = self.textEdit.textCursor()
        findIndex = cursor.anchor()
        text = self.lineEdit.text()
        content = self.textEdit.toPlainText()
        length = len(text)

        self.lastSearchText = text
        index = content.find(text, findIndex)

        if -1 == index:
            errorDialog = QtWidgets.QMessageBox(self)
            errorDialog.addButton("Cancel", QtWidgets.QMessageBox.ActionRole)

            errorDialog.setWindowTitle("Find")
            errorDialog.setText("Not Found\"%s\"." % text)
            errorDialog.setIcon(QtWidgets.QMessageBox.Critical)
            errorDialog.exec_()
        else:
            start = index

            cursor = self.textEdit.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, start + length)
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor, length)
            cursor.selectedText()
            self.text.setTextCursor(cursor)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
