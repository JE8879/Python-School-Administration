import sys
from Views.FrmMain import MainForm
from PyQt5 import QtCore, QtWidgets, QtGui, uic

class FrmLogin(QtWidgets.QWidget):
    # Constructor
    def __init__(self):
        # Find components and assing properties
        super(FrmLogin, self).__init__()

        uic.loadUi('Views/Templates/FrmLogin.ui', self)
        self.setStyleSheet("background-color: rgb(46, 64, 83);")
        self.setMaximumSize(QtCore.QSize(300,240))
        self.setMinimumSize(QtCore.QSize(300,240))

        # Load Styles CSS
        with open('Assets/app.css') as fileCss:
            self.globalStyles = fileCss.read()
        
        # Create Fonts
        self.fontQLineEdit = QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        # Find components and set properties
        self.BtnLogin = self.findChild(QtWidgets.QPushButton, 'BtnLogin')
        self.BtnLogin.setStyleSheet(self.globalStyles)
        self.BtnLogin.clicked.connect(self.CheckLogin)

        self.BtnCancel = self.findChild(QtWidgets.QPushButton, 'BtnCancel')
        self.BtnCancel.setStyleSheet(self.globalStyles)
        self.BtnCancel.clicked.connect(self.close)

        self.textUserName = self.findChild(QtWidgets.QLineEdit, 'textUserName')
        self.textUserName.setStyleSheet(self.globalStyles)
        self.textUserName.setFont(self.fontQLineEdit)

        self.textPassWord = self.findChild(QtWidgets.QLineEdit, 'textPassWord')
        self.textPassWord.setStyleSheet(self.globalStyles)
        self.textPassWord.setFont(self.fontQLineEdit)

        self.groupBox = self.findChild(QtWidgets.QGroupBox, 'groupBox')
        self.groupBox.setStyleSheet(self.globalStyles)

        self.show()
    
    def CheckLogin(self):        
        self.OpenDashBoard()
        self.close()
        # if(self.textUserName.text() == 'JE1041' and self.textPassWord.text() == 'Hacker122'):

    def OpenDashBoard(self):
        self.uiWindow = QtWidgets.QWidget()
        self.instanceWindow = MainForm()
        

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = FrmLogin() 

    app.exec_()



