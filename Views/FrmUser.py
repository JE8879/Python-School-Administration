import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.UserModel import UserModel
from . FrmGeneric import GenericForm
from . Utils.Format import FormatComponents
from . FrmFilter import ViewFilter

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir))
sys.path.append(PROJECT_ROOT)


class ManageUser(QtWidgets.QWidget):
    # Constructor
    def __init__(self):
        # Find components and assign properties
        super(ManageUser, self).__init__()

        # Load Template-UI-File
        uic.loadUi('Views/Templates/FrmUserLogs.ui',self)

        # Load Styles CSS
        with open('./Assets/App.css') as fileCSS:
            self.globalStyles = fileCSS.read()

        self.isUpdate = False
        self.key = 'ID'

        self.qTabWidget = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.qTabWidget.setStyleSheet(self.globalStyles)

        # Search gridLayout
        self.gridLayOut = self.findChild(QtWidgets.QGridLayout, 'gridLayout')

        # Create Fonts
        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        self.fontQLabel = QtGui.QFont()
        self.fontQLabel.setFamily("Century Gothic")
        self.fontQLabel.setPointSize(11)
        self.fontQLabel.setBold(True)
        self.fontQLabel.setWeight(75)

        self.OnlyInteger = QtGui.QIntValidator()

        #------------------ Search LineEdtis ------------------#
        self.textFirstName = self.findChild(QtWidgets.QLineEdit, 'textFirstName')
        self.textFirstName.setStyleSheet(self.globalStyles)
        self.textFirstName.setFont(self.fontQLineEdit)

        self.textLastName = self.findChild(QtWidgets.QLineEdit, 'textLastName')
        self.textLastName.setStyleSheet(self.globalStyles)
        self.textLastName.setFont(self.fontQLineEdit)

        self.CboGender = self.findChild(QtWidgets.QComboBox, 'CboGender')
        self.CboGender.setStyleSheet(self.globalStyles)
        self.CboGender.setFont(self.fontQLineEdit)

        self.textAge = self.findChild(QtWidgets.QLineEdit, 'textAge')
        self.textAge.setStyleSheet(self.globalStyles)
        self.textAge.setFont(self.fontQLineEdit)
        self.textAge.setValidator(self.OnlyInteger)

        self.textPhone = self.findChild(QtWidgets.QLineEdit, 'textPhone')
        self.textPhone.setStyleSheet(self.globalStyles)
        self.textPhone.setFont(self.fontQLineEdit)

        self.textEmail = self.findChild(QtWidgets.QLineEdit, 'textEmail')
        self.textEmail.setStyleSheet(self.globalStyles)
        self.textEmail.setFont(self.fontQLineEdit)

        self.textSearch = self.findChild(QtWidgets.QLineEdit, 'textSearch')
        self.textSearch.setStyleSheet(self.globalStyles)
        self.textSearch.textChanged.connect(self.ApplyFilters)
        self.textSearch.setFont(self.fontQLineEdit)

        self.LblPosition = self.findChild(QtWidgets.QLabel, 'LblPosition')
        self.LblPosition.setFont(self.fontQLineEdit)

        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.hide()

        #--------------------- Search Buttons ---------------------#
        self.BtnSave = self.findChild(QtWidgets.QPushButton, 'BtnSave')
        self.BtnSave.setStyleSheet(self.globalStyles)
        self.BtnSave.clicked.connect(self.SaveUser)

        self.BtnUpdate = self.findChild(QtWidgets.QPushButton, 'BtnUpdate')
        self.BtnUpdate.setStyleSheet(self.globalStyles)
        self.BtnUpdate.clicked.connect(self.UpdateUser)

        self.BtnDelete = self.findChild(QtWidgets.QPushButton, 'BtnDelete')
        self.BtnDelete.setStyleSheet(self.globalStyles)
        self.BtnDelete.clicked.connect(self.RemoveUser)

        self.BtnPosition = self.findChild(QtWidgets.QPushButton, 'BtnPosition')
        self.BtnPosition.setStyleSheet(self.globalStyles)
        self.BtnPosition.clicked.connect(self.OpenPositions)

        self.BtnFilter = self.findChild(QtWidgets.QPushButton, 'BtnFilters')
        self.BtnFilter.setStyleSheet(self.globalStyles)
        self.BtnFilter.clicked.connect(self.OpentFilters)

        self.BtnClearFilters = self.findChild(QtWidgets.QPushButton, 'BtnClearFilters')
        self.BtnClearFilters.clicked.connect(self.ClearFilters)
        self.BtnClearFilters.setStyleSheet(self.globalStyles)

        self.TableUserData = self.findChild(QtWidgets.QTableWidget, 'tableWidget')

        # Create new Menu
        self.qMenuBar = QtWidgets.QMenuBar(self)
        self.qMenuBar.setStyleSheet(self.globalStyles)
        self.fileMenu = self.qMenuBar.addMenu("File")

        # Create the instance 
        self.instanceFormat = FormatComponents()
        self.instanceUserModel = UserModel()

        self.lstHeaderLabels = ('User ID', 'First Name', 'Last Name', 'Gender', 'Age', 'Phone', 'Email', 'Position ID')

        self.fieldValue = ''

        self.LoadComboBox()

        self.Load()
        
    def Load(self):
        self.instanceFormat.FormatQTableWidget(self.TableUserData, 8, self.instanceUserModel.GetBasicInfoUser(), self.lstHeaderLabels, 1)

    def SaveUser(self):
        # Get Data from QLineEdtits
        self.DataUser = self.textFirstName.text(), self.textLastName.text(), self.CboGender.currentText(), self.textAge.text(), self.textPhone.text(), self.textEmail.text(), self.LblPosition.text()[0:2]

        # Create new list
        self.lstUser = list(self.DataUser)

        # Validate List
        for x in range(0,len(self.lstUser)):
            if(len(str(self.lstUser[x])) == 0):
                self.instanceFormat.ShowMessageLabel(self.LblMessage,'Please complete all fields', 'error')
                return
        
        if(self.isUpdate):
            # Get Selected Row
            row = self.TableUserData.currentRow()
            # Get User ID
            currentStudentID = int(self.TableUserData.item(row,0).text())
            # Added the id to the list to update
            self.lstUser.append(currentStudentID)
            # Execute Update
            message = self.instanceUserModel.Update(self.lstUser)            
            # Show Message
            self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Change Value State
            self.isUpdate = False
            # Reload Data
            self.Load()
            # Clear QLineEdits
            self.ClearQLineEdits()
            #Clear Selection
            self.TableUserData.clearSelection()
        else:                      
            # Save User
            message = self.instanceUserModel.Add(self.lstUser)
            # Show message
            self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Clear Information
            self.ClearQLineEdits()
            # Refresh data
            self.Load()

    def UpdateUser(self):
        row = self.TableUserData.currentRow()
        if(row >= 0):
            self.isUpdate = True
            self.textFirstName.setText(self.TableUserData.item(row,1).text())
            self.textLastName.setText(self.TableUserData.item(row,2).text())
            self.CboGender.setEditText(self.TableUserData.item(row,3).text())
            self.textAge.setText(self.TableUserData.item(row,4).text())
            self.textPhone.setText(self.TableUserData.item(row,5).text())
            self.textEmail.setText(self.TableUserData.item(row,6).text())
            self.LblPosition.setText(self.TableUserData.item(row,7).text())
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Select a record to update', 'error')

    def RemoveUser(self):
        row = self.TableUserData.currentRow()
        if(row >= 0):
            #Get ID of element
            currentUserID = int(self.TableUserData.item(row,0).text())
            #Execute funtion
            message = self.instanceUserModel.Delete(currentUserID)
            # Show message
            self.instanceFormat.ShowMessageLabel(self.LblMessage,str(message),'successful')
            #Refresh data
            self.Load()
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Select a record to delete', 'error')
  
    def ClearQLineEdits(self):
        self.textFirstName.clear()
        self.textLastName.clear()
        self.textAge.clear()
        self.textPhone.clear()
        self.textEmail.clear()
        self.LblPosition.setText('')

    def LoadComboBox(self):
        self.CboGender.addItems(['Male','Feminine'])

    def OpenPositions(self):
        self.positionWindow = GenericForm("Positions")
        self.positionWindow.BtnAcept.clicked.connect(self.GetSelectedPosition)
        self.positionWindow.show()        
    
    def GetSelectedPosition(self):
        self.fieldValue = self.positionWindow.RetrieveData()
        if(self.fieldValue != ''):
            self.LblPosition.setText(self.fieldValue)
            self.positionWindow.close()
    
    def OpentFilters(self):
        self.instanceFilter = ViewFilter()
        self.instanceFilter.BtnAcept.clicked.connect(self.GetElement)
        self.instanceFilter.show()

    def GetElement(self):
        self.key = self.instanceFilter.LoadEvents()
        self.instanceFilter.close()

    def ApplyFilters(self):
        # Get data from db
        result = self.instanceUserModel.GetCustomData(self.key, self.textSearch.text())

        self.instaceFormat.FormatQTableWidget(self.TableUsers, 8, result, self.lstHeaderLabels, 2)
        # Reset Data
        if(len(self.textSearch.text()) == 0):
            self.Load()

    def ClearFilters(self):
        self.key = 'ID'

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = ManageUser()

    app.exec_()