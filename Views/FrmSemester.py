import sys
from PyQt5.QtCore import QEvent
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.SemesterModel import SemesterModel
from . Utils.Format import FormatComponents
from . FrmGeneric import ViewGeneric


class ViewSemester(QtWidgets.QWidget):
    # Constructor
    def __init__(self):
        # Find components and assign properties
        super(ViewSemester, self).__init__()

        # Load Template UI-File
        uic.loadUi('Views/Templates/FrmSemester.ui', self)
        self.setStyleSheet('background-color: rgb(46, 64, 83);')
        
        # Load styles CSS
        with open('./Assets/App.css') as fileCSS:
            self.globalStyles = fileCSS.read()

        self.isUpdate = False
        self.fieldValue = ''

        # Create Objects
        self.instanceFormat = FormatComponents()
        self.instanceSemester = SemesterModel()

        # Create Fonts
        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        self.fontQLabel = QtGui.QFont()
        self.fontQLabel.setFamily("Century Gothic")
        self.fontQLabel.setPointSize(12)

        # region ---------------- <Semester Components> ------------------
        self.textSemesterName = self.findChild(QtWidgets.QLineEdit, 'textSemesterName')
        self.textSemesterName.setStyleSheet(self.globalStyles)
        self.textSemesterName.setFont(self.fontQLineEdit)

        self.textSchoolYear = self.findChild(QtWidgets.QLineEdit, 'textSchoolYear')
        self.textSchoolYear.setStyleSheet(self.globalStyles)
        self.textSchoolYear.setFont(self.fontQLineEdit)

        self.textSearch = self.findChild(QtWidgets.QLineEdit, 'textSearch')
        self.textSearch.setStyleSheet(self.globalStyles)
        self.textSearch.setFont(self.fontQLineEdit)

        self.DteStart = self.findChild(QtWidgets.QDateEdit, 'dateEdit')
        self.DteStart.setStyleSheet(self.globalStyles)
        self.DteStart.clearFocus()

        self.DteEnd = self.findChild(QtWidgets.QDateEdit, 'dateEdit_2')
        self.DteEnd.setStyleSheet(self.globalStyles)

        self.CboStatus = self.findChild(QtWidgets.QComboBox, 'CboStatus')
        self.CboStatus.setFont(self.fontQLineEdit)
        # self.CboStatus.setStyleSheet(self.globalStyles)

        self.LblProfession = self.findChild(QtWidgets.QLabel, 'LblProfession')
        self.LblProfession.setStyleSheet(self.globalStyles)
        self.LblProfession.setFont(self.fontQLabel)
        self.LblProfession.hide()

        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.setStyleSheet(self.globalStyles)
        self.LblMessage.hide()

        self.BtnSaveSemester = self.findChild(QtWidgets.QPushButton, 'BtnSaveSemester')
        self.BtnSaveSemester.setStyleSheet(self.globalStyles)
        self.BtnSaveSemester.clicked.connect(self.SaveSemester)

        self.BtnUpdateSemester = self.findChild(QtWidgets.QPushButton, 'BtnUpdateSemester')
        self.BtnUpdateSemester.setStyleSheet(self.globalStyles)
        self.BtnUpdateSemester.clicked.connect(self.UpdateSemester)

        self.BtnDeleteSemester = self.findChild(QtWidgets.QPushButton, 'BtnDeleteSemester')
        self.BtnDeleteSemester.setStyleSheet(self.globalStyles)
        self.BtnDeleteSemester.clicked.connect(self.DeleteSemester)

        self.BtnSelectProfession = self.findChild(QtWidgets.QPushButton, 'BtnProfession')
        self.BtnSelectProfession.setStyleSheet(self.globalStyles)
        self.BtnSelectProfession.clicked.connect(self.OpenProfessions)

        self.BtnFiltersSemester = self.findChild(QtWidgets.QPushButton, 'BtnFiltersSemester')
        self.BtnFiltersSemester.setStyleSheet(self.globalStyles)

        self.BtnClearFiltersSemester = self.findChild(QtWidgets.QPushButton, 'BtnClearFiltersSemester')
        self.BtnClearFiltersSemester.setStyleSheet(self.globalStyles)

        self.TableSemesters = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        
        # self.TableSemesters.leaveEvent = self.handle_leave_event

        self.groupBoxOne = self.findChild(QtWidgets.QGroupBox, 'groupBoxOne')
        self.groupBoxOne.setStyleSheet(self.globalStyles)

        self.groupBoxTwo = self.findChild(QtWidgets.QGroupBox, 'groupBoxTwo')
        self.groupBoxTwo.setStyleSheet(self.globalStyles)

        self.groupBoxFour = self.findChild(QtWidgets.QGroupBox, 'groupBoxFour')
        self.groupBoxFour.setStyleSheet(self.globalStyles)

        # endregion

        # Load QDates
        self.InitQDates()
        self.LoadSemesters()

    # region --------------<Student Methods> -----------
    def LoadSemesters(self):
        lstHeaders = ('ID', 'Name', 'Year', 'Time Start', 'Time End', 'Missing Months', 'ProfID')
        self.instanceFormat.FormatQTableWidget(self.TableSemesters,7,self.instanceSemester.GetFormattedData(),lstHeaders,1)

    def SaveSemester(self):
        # Get data from inputs
        self.semesterData = self.textSemesterName.text(), self.textSchoolYear.text(),self.DteStart.dateTime().toString('yyyy-MM-dd'),self.DteEnd.dateTime().toString('yyyy-MM-dd'), self.CboStatus.currentText(), self.LblProfession.text()[0:1]

        # Covert to list
        self.listSemesterData = list(self.semesterData)
       
        # Validate List
        for x in range(0,len(self.listSemesterData)):
            if(len(str(self.listSemesterData[x])) == 0):
                self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Please complete all fields', 'error')
                return             

        if(self.isUpdate):
            # Get Selected row
            row = self.TableSemesters.currentRow()
            # Get semester ID
            currentSemesterID = int(self.TableSemesters.item(row,0).text())
            # Add ID to List
            self.listSemesterData.append(currentSemesterID)
            # Execute Update
            message = self.instanceSemester.Update(self.listSemesterData)
            # Show message
            self.instanceFormat.ShowMessageLabel(self.LblMessage,message,'succesfull')
            # Change Value
            self.isUpdate = False
            # Refresh data
            self.LoadSemesters()
            # Clear
            self.ClearItems()
            # Clear Selection
            self.TableSemesters.clearSelection()
        else:
            # Execute Add
            message = self.instanceSemester.Add(self.listSemesterData)
            # Show Message
            self.instanceFormat.ShowMessageLabel(self.LblMessage,message,'succesful')
            # Refresh Data
            self.LoadSemesters()
            # Clear
            self.ClearItems()       

    def UpdateSemester(self):
        row = self.TableSemesters.currentRow()
        if(row >= 0):
            self.textSemesterName.setText(self.TableSemesters.item(row,1).text())
            self.textSchoolYear.setText(self.TableSemesters.item(row,2).text())
            # Get Dates from String
            startDate = QtCore.QDate.fromString(self.TableSemesters.item(row,3).text(),'yyyy-MM-dd')
            endDate = QtCore.QDate.fromString(self.TableSemesters.item(row,4).text(),'yyyy-MM-dd')
            # Set Dates
            self.DteStart.setDate(startDate)
            self.DteEnd.setDate(endDate)

            self.LblProfession.setText(self.TableSemesters.item(row,6).text())
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage,'Select a record to update','error')

    def DeleteSemester(self):
        row = self.TableSemesters.currentRow()
        if(row >= 0):
            # Get ID
            currentSemesterID = int(self.TableSemesters.item(row,0).text())
            # Catch message
            message = self.instanceSemester.Delete(currentSemesterID)
            # Show message
            self.instanceFormat.ShowMessageLabel(self.LblMessage,message,'succesfull')
            # Refresh Data
            self.LoadSemesters()
            # Clear selection
            self.TableSemesters.clearSelection()
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Select a record to delete', 'error')
    
    def OpenProfessions(self):
        self.semesterWindow = ViewGeneric("Professions")
        self.semesterWindow.BtnAcept.clicked.connect(self.GetSelectedProfession)
        self.semesterWindow.show()
    
    def GetSelectedProfession(self):
        self.fieldValue = self.semesterWindow.RetrieveData()
        if(self.fieldValue !=''):
            self.LblProfession.setText(self.fieldValue)
            self.LblProfession.show()
            self.semesterWindow.close()

    def InitQDates(self):

        dateFromString = QtCore.QDate().currentDate().toString(QtCore.Qt.ISODate)
        currentDate = QtCore.QDate.fromString(dateFromString,'yyyy-MM-dd')

        self.DteStart.setDate(currentDate)
        self.DteEnd.setDate(currentDate)
    
    def ClearItems(self):
        self.textSemesterName.setText('')
        self.textSchoolYear.setText('')
        self.LblProfession.setText('')
        self.LblProfession.hide()


    # def handle_leave_event(self, event):
    #    if(event.type() == QEvent.Leave):
    #        self.TableSemesters.clearSelection()
    #        self.TableSemesters.clearFocus()

    # endregion

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    window = ViewSemester()

    app.exec_()