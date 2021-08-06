# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spiceWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(406, 120)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 120))
        font = QtGui.QFont()
        font.setKerning(True)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(-1, 4, -1, 2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalWidget = QtWidgets.QWidget(Dialog)
        self.verticalWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nombreL = QtWidgets.QLabel(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nombreL.sizePolicy().hasHeightForWidth())
        self.nombreL.setSizePolicy(sizePolicy)
        self.nombreL.setObjectName("nombreL")
        self.horizontalLayout.addWidget(self.nombreL)
        self.nombreT = QtWidgets.QLineEdit(self.verticalWidget)
        self.nombreT.setObjectName("nombreT")
        self.horizontalLayout.addWidget(self.nombreT)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.archivoL = QtWidgets.QLabel(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.archivoL.sizePolicy().hasHeightForWidth())
        self.archivoL.setSizePolicy(sizePolicy)
        self.archivoL.setObjectName("archivoL")
        self.horizontalLayout_2.addWidget(self.archivoL)
        self.pathBtn = QtWidgets.QPushButton(self.verticalWidget)
        self.pathBtn.setMaximumSize(QtCore.QSize(23, 23))
        self.pathBtn.setAutoFillBackground(True)
        self.pathBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("fileBtn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pathBtn.setIcon(icon)
        self.pathBtn.setIconSize(QtCore.QSize(40, 40))
        self.pathBtn.setAutoExclusive(False)
        self.pathBtn.setObjectName("pathBtn")
        self.horizontalLayout_2.addWidget(self.pathBtn)
        self.pathT = QtWidgets.QLineEdit(self.verticalWidget)
        self.pathT.setObjectName("pathT")
        self.horizontalLayout_2.addWidget(self.pathT)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.okBtn = QtWidgets.QPushButton(self.verticalWidget)
        self.okBtn.setMinimumSize(QtCore.QSize(60, 30))
        self.okBtn.setMaximumSize(QtCore.QSize(60, 30))
        self.okBtn.setStyleSheet("background-color: rgb(14, 51, 90);\n"
"color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-radius:10px;\n"
"border-color:black;\n"
"")
        self.okBtn.setObjectName("okBtn")
        self.verticalLayout.addWidget(self.okBtn, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.verticalWidget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Gestor"))
        self.nombreL.setText(_translate("Dialog", "Nombre: "))
        self.nombreT.setPlaceholderText(_translate("Dialog", "Ingrese el nombre de la curva"))
        self.archivoL.setText(_translate("Dialog", "Seleccione el archivo: "))
        self.pathT.setPlaceholderText(_translate("Dialog", "Ingrese el path"))
        self.okBtn.setText(_translate("Dialog", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
