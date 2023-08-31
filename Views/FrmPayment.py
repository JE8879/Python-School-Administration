import re
import sys
import uuid
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from Models.PaymentModel import PaymentModel
from PyQt5.QtGui import QIntValidator
from . FrmGeneric import ViewGeneric
from . Utils.Format import FormatComponents


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

        self.groupBox = self.findChild(QtWidgets.QGroupBox, 'groupBox')
        self.groupBox.setStyleSheet(self.globalStyles)

        self.groupBoxThree = self.findChild(QtWidgets.QGroupBox, 'groupBoxThree')
        self.groupBoxThree.setStyleSheet(self.globalStyles)

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
        
        self.LblPayConcept = self.findChild(QtWidgets.QLabel, 'LblPayConcept')

        self.LBlCambio = self.findChild(QtWidgets.QLabel, 'LBlCambio')

        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.hide()

        self.BtnPay = self.findChild(QtWidgets.QPushButton, 'BtnPay')
        self.BtnPay.setStyleSheet(self.globalStyles)
        self.BtnPay.clicked.connect(self.ProcesPayment)

        self.BtnDetails = self.findChild(QtWidgets.QPushButton, 'BtnDetails')
        self.BtnDetails.setStyleSheet(self.globalStyles)

        self.BtnHistory = self.findChild(QtWidgets.QPushButton, 'BtnHistory')
        self.BtnHistory.setStyleSheet(self.globalStyles)

        self.BtnDelete = self.findChild(QtWidgets.QPushButton, 'BtnDelete')
        self.BtnDelete.setStyleSheet(self.globalStyles)

        self.TabletPayment = self.findChild(QtWidgets.QTableWidget, 'TabletPayment')
        self.TabletPayment.setFocusPolicy(QtCore.Qt.NoFocus)

        self.instanceFormat = FormatComponents()
        self.instancePayment = PaymentModel()
        self.Load()

    def LoadStudents(self):
        self.instanceStudentWindow = ViewGeneric('Students')
        self.instanceStudentWindow.BtnAcept.clicked.connect(self.GetStudent)
        self.instanceStudentWindow.show()

    def GetStudent(self):
        currentStudent = self.instanceStudentWindow.RetrieveData()
        if(currentStudent != ''):
            self.LblStudent.setText(currentStudent)
            self.instanceStudentWindow.close()
             
    def LoadPaymentTypes(self):
        self.instanceStudentWindow = ViewGeneric('Payments')
        self.instanceStudentWindow.BtnAcept.clicked.connect(self.GetPayConcept)
        self.instanceStudentWindow.show()

    def GetPayConcept(self):
        payConceptDetails = self.instanceStudentWindow.RetrievePayConcept()
        if(len(payConceptDetails) > 0):
            self.LblTotal.setText(str(payConceptDetails[0]))
            self.LblPayConcept.setText(str(payConceptDetails[1]))
            self.instanceStudentWindow.close()

    def on_text_changed(self,text):

        if(len(text) == 0):
            self.LBlCambio.setText('')
            return

        if(not text.isdigit()):
            self.textAmount.setText(text[:-1])
        else:
            result = int(text) - int(self.LblTotal.text())
            
            if(result < 0):
                return
            else:
                self.LBlCambio.setText(str(result))

    def ProcesPayment(self):
        currentDate = QtCore.QDate.currentDate().toString('yyyy-MM-dd')
        folioNumber = self.GetFolioNumber()

        objectList = [self.LblStudent.text(),
                      folioNumber,
                      self.LblPayConcept.text(),
                      currentDate,
                      self.LblTotal.text()]
        
        # Validate list
        for x in range(0,len(objectList)):
            if(len(objectList[x]) == 0):
                self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Please complete all fields', 'error')
                print(len(objectList))
                return
        
        # Delete elements of the list
        del objectList[0]
        del objectList[3]
        # Get and convert studentid to int
        studentID = int(re.search(r'\d+',self.LblStudent.text()).group())
        total = int(re.search(r'\d+',self.LblTotal.text()).group())        
        # Insert objects into the list
        objectList.insert(0,studentID)
        objectList.insert(4,total)

        # Execute Query
        message = self.instancePayment.Add(objectList)
        # Show Message
        self.instanceFormat.ShowMessageLabel(self.LblMessage,message,'successful')
        # Clean
        self.CleanContents()
        # Refresh data
        self.Load()
    
    def Load(self):
        lstHeaderLabels = ('Payment ID', 'User ID', 'Folio Number', 'Payment Concept', 'Payment Date', 'Amount')
        self.instanceFormat.FormatQTableWidget(self.TabletPayment,6,self.instancePayment.GetAll(),lstHeaderLabels,1)
        self.textAmount.setFocus()
    
    def GetFolioNumber(self):
        uuidFolio = uuid.uuid4()
        return str(uuidFolio)

    def CleanContents(self):
        self.LblStudent.setText('')
        self.LblPayConcept.setText('')
        self.LblTotal.setText('')
        self.LBlCambio.setText('')


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    window = ViewPayment()

    app.exec_()

        