# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_picture.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddPic(object):
    def setupUi(self, AddPic):
        AddPic.setObjectName("AddPic")
        AddPic.resize(500, 300)
        font = QtGui.QFont()
        font.setPointSize(11)
        AddPic.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(AddPic)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(AddPic)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 2)
        self.label_8 = QtWidgets.QLabel(AddPic)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 2, 1, 2)
        self.label = QtWidgets.QLabel(AddPic)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(AddPic)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(AddPic)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(AddPic)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(AddPic)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.textEdit = QtWidgets.QTextEdit(AddPic)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.label_6 = QtWidgets.QLabel(AddPic)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.gridLayout.addLayout(self.verticalLayout, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(AddPic)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddPic)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.buttonBox.setFont(font)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(AddPic)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)

        self.retranslateUi(AddPic)
        QtCore.QMetaObject.connectSlotsByName(AddPic)

    def retranslateUi(self, AddPic):
        _translate = QtCore.QCoreApplication.translate
        AddPic.setWindowTitle(_translate("AddPic", "Дополнительная картинка"))
        self.label.setText(_translate("AddPic", "Id исходной картинки"))
        self.label_2.setText(_translate("AddPic", "Автор"))
        self.label_4.setText(_translate("AddPic", "Название"))
        self.textEdit.setHtml(_translate("AddPic", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Введите комментарий здесь</span></p></body></html>"))
        self.label_6.setText(_translate("AddPic", "Выберите файл дополнительной картинки"))
        self.pushButton.setText(_translate("AddPic", "Выберите файл"))

