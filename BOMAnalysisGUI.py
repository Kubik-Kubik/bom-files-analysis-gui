from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon


class Ui_Dialog(object):
    def __init__(self, dialog):
        self.lineEdit = QtWidgets.QLineEdit(dialog)
        self.lineEdit_2 = QtWidgets.QLineEdit(dialog)
        self.label = QtWidgets.QLabel(dialog)
        self.label_2 = QtWidgets.QLabel(dialog)
        self.pushButton = QtWidgets.QPushButton(dialog)
        self.pushButton_2 = QtWidgets.QPushButton(dialog)
        self.btn_open = QtWidgets.QPushButton(dialog)
        self.pushButton_5 = QtWidgets.QPushButton(dialog)
        self.btn_dir = QtWidgets.QPushButton(dialog)

    def setupUi(self, dialog):
        dialog.setObjectName("Dialog")
        dialog.resize(725, 350)
        dialog.setStyleSheet("QDialog {\n"
                             "background-color: #343a40;\n"
                             "}")

        self.lineEdit.setGeometry(QtCore.QRect(70, 100, 471, 31))
        self.lineEdit.setAcceptDrops(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 180, 471, 31))
        self.lineEdit_2.setAcceptDrops(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label.setGeometry(QtCore.QRect(70, 70, 581, 41))
        self.label.setStyleSheet("QLabel {\n"
                                 "color : white;\n"
                                 " }")
        self.label.setObjectName("label")
        self.label_2.setGeometry(QtCore.QRect(70, 161, 371, 20))
        self.label_2.setStyleSheet("QLabel {\n"
                                   "color : white;\n"
                                   " }")
        self.label_2.setObjectName("label_2")
        self.pushButton.setGeometry(QtCore.QRect(550, 100, 100, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2.setGeometry(QtCore.QRect(550, 180, 100, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        # self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        # self.pushButton_3.setGeometry(QtCore.QRect(580, 100, 71, 31))
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        # self.pushButton_4.setGeometry(QtCore.QRect(580, 180, 71, 31))
        # self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5.setGeometry(QtCore.QRect(70, 240, 581, 31))
        self.pushButton_5.setObjectName("pushButton_5")

        self.btn_dir.setGeometry(QtCore.QRect(68, 240, 290, 31))
        self.btn_open.setGeometry(QtCore.QRect(358, 240, 290, 31))
        self.btn_dir.setText('Открыть расположение файла')
        self.btn_open.setText('Открыть отчет в формате .CSV')

        self.btn_dir.hide()
        self.btn_open.hide()

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Сравнение BOM-файлов по RefDes"))
        dialog.setWindowIcon(QIcon('logo.png'))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p><span style=\" font-size:12pt;\">Выберите исходный BOM файл</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:12pt;\">Выберите измененный BOM файл</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Выбрать файл"))
        self.pushButton_2.setText(_translate("Dialog", "Выбрать файл"))
        self.pushButton_5.setText(_translate("Dialog", "Сформировать отчет"))
