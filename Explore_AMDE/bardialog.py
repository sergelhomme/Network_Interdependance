from PyQt4 import QtCore, QtGui
from ui_bar import Ui_Bar
class UiBar(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_Bar()
    self.ui.setupUi(self)




