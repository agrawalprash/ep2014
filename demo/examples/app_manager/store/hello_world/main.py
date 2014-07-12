from pyface.qt import QtGui

app = QtGui.QApplication([])

w = QtGui.QLabel('Hello world')
w.resize(300, 200)
w.show()

app.exec_()
