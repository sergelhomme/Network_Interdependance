from PyQt4 import QtCore, QtGui

class Ui_Bar(object):
    def setupUi(self, Bar):
        Bar.setObjectName("Bar")
        Bar.resize(400, 189)
        self.progressBar = QtGui.QProgressBar(Bar)
        self.progressBar.setGeometry(QtCore.QRect(30, 80, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtGui.QLabel(Bar)
        self.label.setGeometry(QtCore.QRect(30, 50, 201, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Bar)
        QtCore.QMetaObject.connectSlotsByName(Bar)

    def retranslateUi(self, Bar):
        Bar.setWindowTitle(QtGui.QApplication.translate("Bar", "Progression du calcul", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Bar", "Progression du calcul", None, QtGui.QApplication.UnicodeUTF8))

