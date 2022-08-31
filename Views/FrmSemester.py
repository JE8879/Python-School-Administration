import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.SemesterModel import SemesterModel
from . Utils.Format import FormatComponents
from . FrmGeneric import GenericForm


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

        # Create Fonts
        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        self.fontQLabel = QtGui.QFont()
        self.fontQLabel.setFamily("Century Gothic")
        self.fontQLabel.setPointSize(12)

        # ------------------------------QLineEdits------------------------------ #
        self.textSemesterName = self.findChild(QtWidgets.QLineEdit, 'textSemesterName')
        self.textSemesterName.setStyleSheet(self.globalStyles)
        self.textSemesterName.setFont(self.fontQLineEdit)

        self.textSchoolYear = self.findChild(QtWidgets.QLineEdit, 'textSchoolYear')
        self.textSchoolYear.setStyleSheet(self.globalStyles)
        self.textSchoolYear.setFont(self.fontQLineEdit)

        self.textSearch = self.findChild(QtWidgets.QLineEdit, 'textSearch')
        self.textSearch.setStyleSheet(self.globalStyles)
        self.textSearch.setFont(self.fontQLineEdit)

        # ------------------------------QDateEdits------------------------------ #
        self.DteStart = self.findChild(QtWidgets.QDateEdit, 'DteStart')
        self.DteStart.setStyleSheet(self.globalStyles)

        self.DteEnd = self.findChild(QtWidgets.QDateEdit, 'DteEnd')
        self.DteEnd.setStyleSheet(self.globalStyles)

        # ------------------------------QLabels------------------------------ #
        self.LblProfession = self.findChild(QtWidgets.QLabel, 'LblProfession')
        self.LblProfession.setStyleSheet(self.globalStyles)
        self.LblProfession.setFont(self.fontQLabel)

        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.setStyleSheet(self.globalStyles)
        self.LblMessage.hide()

        # ------------------------------QPushButtons------------------------------ #
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

        # ------------------------------QGroupBoxes------------------------------ #
        self.groupBoxOne = self.findChild(QtWidgets.QGroupBox, 'groupBoxOne')
        self.groupBoxOne.setStyleSheet(self.globalStyles)

        self.groupBoxTwo = self.findChild(QtWidgets.QGroupBox, 'groupBoxTwo')
        self.groupBoxTwo.setStyleSheet(self.globalStyles)

        self.groupBoxThree = self.findChild(QtWidgets.QGroupBox, 'groupBoxThree')
        self.groupBoxThree.setStyleSheet(self.globalStyles)

        # ------------------------------QTableWidget------------------------------ #
        self.TableSemesters = self.findChild(QtWidgets.QTableWidget, 'TableSemesters')

        # Create Objects
        self.instanceFormat = FormatComponents()
        self.instanceSemester = SemesterModel()

        # Load QDates
        self.InitQDates()

        self.LoadSemesters()
       
    def LoadSemesters(self):
        lstHeaders = ('ID', 'Name', 'Year', 'Time Start', 'Time End', 'Missing Months', 'ProfID')
        self.instanceFormat.FormatQTableWidget(self.TableSemesters,7,self.instanceSemester.GetFormattedData(),lstHeaders,1)

    def SaveSemester(self):
        # Get data from inputs
        self.semesterData = self.textSemesterName.text(), self.textSchoolYear.text(),self.DteStart.dateTime().toString('yyyy-MM-dd'),self.DteEnd.dateTime().toString('yyyy-MM-dd'),self.LblProfession.text()[0:1]

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
            self.instanceFormat.ShowMessageLabel(self.LblMessage,message,'succesfull')
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
        self.semesterWindow = GenericForm("Professions")
        self.semesterWindow.BtnAcept.clicked.connect(self.GetSelectedProfession)
        self.semesterWindow.show()
    
    def GetSelectedProfession(self):
        self.fieldValue = self.semesterWindow.RetrieveData()
        if(self.fieldValue !=''):
            self.LblProfession.setText(self.fieldValue)
            self.semesterWindow.close()

    def InitQDates(self):

        dateFromString = QtCore.QDate().currentDate().toString(QtCore.Qt.ISODate)
        currentDate = QtCore.QDate.fromString(dateFromString,'yyyy-MM-dd')

        self.DteStart.setDate(currentDate)
        self.DteEnd.setDate(currentDate)
    
    def ClearItems(self):
        self.textSemesterName.setText('')
        self.textSchoolYear.setText('')

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    window = ViewSemester()

    app.exec_()