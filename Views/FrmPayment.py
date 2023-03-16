import sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtGui import QIntValidator
from . FrmGeneric import GenericForm

class ViewPayment(QtWidgets.QWidget):
    # Constructor
    def __init__(self):
        super(ViewPayment, self).__init__()

        # Load Template-UI-File
        uic.loadUi('Views/Templates/FrmPayment.ui', self)

        # Create a validator to textamout
        self.textAmountValidator = QIntValidator()

        # Load CSS File 
        with open('./Assets/App.css') as fileCSS:
            self.globalStyles = fileCSS.read()

        # Create Fonts
        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        self.fontQLabel = QtGui.QFont()
        self.fontQLabel.setFamily("Century Gothic")
        self.fontQLabel.setPointSize(12)

        self.BtnSelectStudent = self.findChild(QtWidgets.QPushButton, 'BtnSelectStudent')
        self.BtnSelectStudent.setStyleSheet(self.globalStyles)
        self.BtnSelectStudent.clicked.connect(self.LoadStudents)

        self.LblStudent = self.findChild(QtWidgets.QLabel, 'LblStudent')
        self.LblStudent.setStyleSheet(self.globalStyles)

        self.BtnSelectPayment = self.findChild(QtWidgets.QPushButton, 'BtnSelectPayment')
        self.BtnSelectPayment.setStyleSheet(self.globalStyles)
        self.BtnSelectPayment.clicked.connect(self.LoadPaymentTypes)

        self.textAmount = self.findChild(QtWidgets.QLineEdit, 'textAmount')
        self.textAmount.setStyleSheet(self.globalStyles)
        self.textAmount.setFont(self.fontQLineEdit)
        self.textAmount.setValidator(self.textAmountValidator)
        self.textAmount.textChanged.connect(self.on_text_changed)

        self.LblTotal = self.findChild(QtWidgets.QLabel, 'LblTotal')

        self.LBlCambio = self.findChild(QtWidgets.QLabel, 'LBlCambio')

        self.BtnPay = self.findChild(QtWidgets.QPushButton, 'BtnPay')
        self.BtnPay.setStyleSheet(self.globalStyles)

        self.BtnDetails = self.findChild(QtWidgets.QPushButton, 'BtnDetails')
        self.BtnDetails.setStyleSheet(self.globalStyles)

        self.BtnHistory = self.findChild(QtWidgets.QPushButton, 'BtnHistory')
        self.BtnHistory.setStyleSheet(self.globalStyles)

        self.BtnDelete = self.findChild(QtWidgets.QPushButton, 'BtnDelete')
        self.BtnDelete.setStyleSheet(self.globalStyles)

    def LoadStudents(self):
        self.instanceStudentWindow = GenericForm('Students')
        self.instanceStudentWindow.BtnAcept.clicked.connect(self.GetStudent)
        self.instanceStudentWindow.show()

    def GetStudent(self):
        currentStudent = self.instanceStudentWindow.RetrieveData()
        if(currentStudent != ''):
            self.LblStudent.setText(currentStudent)
            self.instanceStudentWindow.close()
             
    def LoadPaymentTypes(self):
        self.instanceStudentWindow = GenericForm('Payments')
        self.instanceStudentWindow.show()

    def on_text_changed(self,text):
        if(len(text) == 0):
            self.LBlCambio.setText('')

        if(not text.isdigit()):
            self.textAmount.setText(text[:-1])
        else:
            result = int(text) - int(self.LblTotal.text())
            self.LBlCambio.setText(str(result))

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    window = ViewPayment()

    app.exec_()

        