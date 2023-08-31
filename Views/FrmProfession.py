import sys
import re
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from Models.ProfessionModel import ProfessionModel
from Models.SubjectModel import SubjectModel
from . Utils.Format import FormatComponents
from . FrmGeneric import ViewGeneric


class ViewProfession(QtWidgets.QWidget):
    # Constructor
    def __init__(self):
        super(ViewProfession, self).__init__()

        # Load Template-UI-File
        uic.loadUi('Views/Templates/FrmProfession.ui', self)

        # Load CSS File 
        with open('./Assets/App.css') as fileCSS:
            self.globalStyles = fileCSS.read()

        # Glabal Controls and Vars
        self.SubContainerOne = self.findChild(QtWidgets.QGroupBox, 'SubContainerOne')
        self.SubContainerOne.setStyleSheet(self.globalStyles)

        self.field = ''

        self.SubContainerThree = self.findChild(QtWidgets.QGroupBox, 'SubContainerThree')
        self.SubContainerThree.setStyleSheet(self.globalStyles)

        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.hide()

        self.professionIsUpdate = False
        self.subjectIsUpdate = False

        # Create Fonts
        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        # region <Load Profession Controls UI>
        self.textProfessionName = self.findChild(QtWidgets.QLineEdit, 'textProfessionName')
        self.textProfessionName.setStyleSheet(self.globalStyles)

        self.textDescription = self.findChild(QtWidgets.QTextEdit, 'textDescription')
        self.textDescription.setStyleSheet(self.globalStyles)

        self.textSearchProfession = self.findChild(QtWidgets.QLineEdit, 'textSearchProfession')
        self.textSearchProfession.setStyleSheet(self.globalStyles)

        self.tableProfessions = self.findChild(QtWidgets.QTableWidget, 'tableProfessions')

        self.BtnSaveProfession = self.findChild(QtWidgets.QPushButton, 'BtnSaveProfession')
        self.BtnSaveProfession.setStyleSheet(self.globalStyles)
        self.BtnSaveProfession.clicked.connect(self.SaveProfession)

        self.BtnUpdateProfession = self.findChild(QtWidgets.QPushButton, 'BtnUpdateProfession')
        self.BtnUpdateProfession.setStyleSheet(self.globalStyles)
        self.BtnUpdateProfession.clicked.connect(self.UpdateProfession)

        self.BtnDeleteProfession = self.findChild(QtWidgets.QPushButton, 'BtnDeleteProfession')
        self.BtnDeleteProfession.setStyleSheet(self.globalStyles)
        self.BtnDeleteProfession.clicked.connect(self.DeleteProfession)

        self.BtnFiltersProfession = self.findChild(QtWidgets.QPushButton, 'BtnFiltersProfession')
        self.BtnFiltersProfession.setStyleSheet(self.globalStyles)

        self.BtnClearFiltersProfession = self.findChild(QtWidgets.QPushButton, 'BtnClearFiltersProfession')
        self.BtnClearFiltersProfession.setStyleSheet(self.globalStyles)

        self.CboActive = self.findChild(QtWidgets.QComboBox, 'CboActive')
        self.CboActive.setStyleSheet(self.globalStyles)
        self.CboActive.setFont(self.fontQLineEdit)
        #endregion

        # region <Load Subject Controls UI>
        self.textSubjectName = self.findChild(QtWidgets.QLineEdit, 'textSubjectName')
        self.textSubjectName.setStyleSheet(self.globalStyles)

        self.textSearchSubject = self.findChild(QtWidgets.QLineEdit, 'textSearchSubject')
        self.textSearchSubject.setStyleSheet(self.globalStyles)

        self.BtnSelectSemester = self.findChild(QtWidgets.QPushButton, 'BtnSelectSemester')
        self.BtnSelectSemester.setStyleSheet(self.globalStyles)
        self.BtnSelectSemester.setFont(self.fontQLineEdit)
        self.BtnSelectSemester.clicked.connect(self.OpenGenericSemesterWindow)

        self.LblSemester = self.findChild(QtWidgets.QLabel, 'LblSemester')
        self.LblSemester.setStyleSheet(self.globalStyles)

        self.BtnSaveSubject = self.findChild(QtWidgets.QPushButton, 'BtnSaveSubject')
        self.BtnSaveSubject.setStyleSheet(self.globalStyles)
        self.BtnSaveSubject.clicked.connect(self.SaveSubject)

        self.BtnUpdateSubject = self.findChild(QtWidgets.QPushButton, 'BtnUpdateSubject')
        self.BtnUpdateSubject.setStyleSheet(self.globalStyles)
        self.BtnUpdateSubject.clicked.connect(self.UpdateSubject)

        self.BtnDeleteSubject = self.findChild(QtWidgets.QPushButton, 'BtnDeleteSubject')
        self.BtnDeleteSubject.setStyleSheet(self.globalStyles)
        self.BtnDeleteSubject.clicked.connect(self.DeleteSubject)

        self.BtnFiltersSubject = self.findChild(QtWidgets.QPushButton, 'BtnFiltersSubject')
        self.BtnFiltersSubject.setStyleSheet(self.globalStyles)

        self.BtnClearFiltersSubject = self.findChild(QtWidgets.QPushButton, 'BtnClearFiltersSubject')
        self.BtnClearFiltersSubject.setStyleSheet(self.globalStyles)

        self.tableSubjects = self.findChild(QtWidgets.QTableWidget, 'tableSubjects')
        self.tableSubjects.setStyleSheet(self.globalStyles)
        # endregion

        # Create instances
        self.instanceProfessionModel = ProfessionModel()
        self.instanceSubjectModel = SubjectModel()
        self.instanceFormat = FormatComponents()

        self.LoadProfessions()
        self.LoadSubjects()
        self.LoadComboBox()

    # region <Create All Methods of Profession
    def LoadComboBox(self):
        lstItems = ['Active', 'Not Active']
        self.CboActive.addItems(lstItems)
    
    def LoadProfessions(self):
        lstHeaderLabels = ('Profession ID', 'Profession Name', 'Description', 'Active')
        self.instanceFormat.FormatQTableWidget(self.tableProfessions, 4, self.instanceProfessionModel.GetAll(), lstHeaderLabels, 1)

    def SaveProfession(self):
        # Get data from QlineEdits
        self.professionData = self.textProfessionName.text(), self.textDescription.toPlainText(), self.CboActive.currentText()

        # Convert to list
        self.lstDataProfession = list(self.professionData)

        # Validate list
        for x in range(0, len(self.lstDataProfession)):
            if(len(str(self.lstDataProfession[x])) == 0):
                self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Please complete all fields', 'error')
                return

        if(self.professionIsUpdate):
            currentRow = self.tableProfessions.currentRow()
            # Get ProfessionID
            currentProfessionID = int(self.tableProfessions.item(currentRow, 0).text())
            # Add ID to List
            self.lstDataProfession.append(currentProfessionID)
            # Execute update
            message = self.instanceProfessionModel.Update(self.lstDataProfession)
            # Show message 
            self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Change value state
            self.professionIsUpdate = False
            # Refresh Data
            self.LoadProfessions()
            # Clear
            self.ClearProfessionContent()
        else:
            # Save record
            message = self.instanceProfessionModel.Add(self.lstDataProfession)
            # Show message 
            self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Clear
            self.ClearProfessionContent()
            # Refresh Data
            self.LoadProfessions()

    def UpdateProfession(self):
        currentRow = self.tableProfessions.currentRow()
        if(currentRow >= 0):
            self.professionIsUpdate = True
            self.textProfessionName.setText(self.tableProfessions.item(currentRow,1).text())
            self.textDescription.setPlainText(self.tableProfessions.item(currentRow,2).text())
            self.CboActive.setEditText(self.tableProfessions.item(currentRow,3).text())
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Select a record to update', 'error')
    
    def DeleteProfession(self):
        currentRow = self.tableProfessions.currentRow()
        if(currentRow >= 0):
            # Get Id
            professionID = int(self.tableProfessions.item(currentRow, 0).text())
            # Execute query
            message = self.instanceProfessionModel.Delete(professionID)
            # Show message
            self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Refresh Data
            self.LoadProfessions()
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Select Record to Delete', 'error')

    def ClearProfessionContent(self):
        self.textProfessionName.setText('')
        self.textDescription.clear()
    #endregion
    
    # region <Create All Methods of Subject
    def OpenGenericSemesterWindow(self):
        self.semesterWindow = ViewGeneric('Semesters')
        self.semesterWindow.BtnAcept.clicked.connect(self.GetSemesterField)
        self.semesterWindow.show()

    def LoadSubjects(self):
        lstHeaderLabels = ('Subject ID', 'Subject Name', 'Semester ID', 'Semester Profession')
        self.instanceFormat.FormatQTableWidget(self.tableSubjects, 4, self.instanceSubjectModel.GetAll(), lstHeaderLabels, 1)

    def GetSemesterField(self):
        self.field = self.semesterWindow.RetrieveData()
        if(self.field != ''):
            self.LblSemester.setText(str(self.field))
            self.semesterWindow.close()

    def SaveSubject(self):
        # Create a empty list to storage data
        self.subjecData = []
        # GetString  ID of label
        stringSemesterID = self.LblSemester.text()
        # Search an integer in a string
        match = re.search(r'\d+', stringSemesterID)

        # Validate
        if match:
            # Convert string to int
            currentSemesterID = int(match.group())

            if(self.subjectIsUpdate):
                # Get Current Row
                currentSubject = self.tableSubjects.currentRow()
                # Get subjectID
                currentSubjectID = int(self.tableSubjects.item(currentSubject, 0).text())
                # Add data to list
                self.subjecData.append(self.textSubjectName.text())
                self.subjecData.append(currentSemesterID)
                self.subjecData.append(currentSubjectID)                
                # Execute Query
                message = self.instanceSubjectModel.Update(self.subjecData)
                # Show message
                self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
                # Refresh data
                self.LoadSubjects()
                # Clear Data
                self.ClearSubjectContent()
            else:
                # Add data to list
                self.subjecData.append(self.textSubjectName.text())
                self.subjecData.append(currentSemesterID)
                # Execute Query 
                message = self.instanceSubjectModel.Add(self.subjecData)
                # Show message
                self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
                # Refresh data
                self.LoadSubjects()
                # Clear Data
                self.ClearSubjectContent()
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Plese Complete all Fields', 'error')

    def UpdateSubject(self):
        currentRow = self.tableSubjects.currentRow()
        if(currentRow >= 0):
            self.subjectIsUpdate = True
            self.textSubjectName.setText(self.tableSubjects.item(currentRow,1).text())

            subjectInfo = self.tableSubjects.item(currentRow, 2).text()
            subjectInfo+= ' '
            subjectInfo+= self.tableSubjects.item(currentRow, 3).text()

            self.LblSemester.setText(subjectInfo)
            self.tableSubjects.clearSelection()
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Select a record to update', 'error')

    def DeleteSubject(self):
        currentRow = self.tableSubjects.currentRow()
        if(currentRow >= 0):
            # Get SubjectID
            currentSubjectID = int(self.tableSubjects.item(currentRow, 0).text())
            # Catch Message
            message = self.instanceSubjectModel.Delete(currentSubjectID)
            # Show Message
            self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Refresh Data
            self.LoadSubjects()
            # Clear Selection
            self.tableSubjects.clearSelection()
        else:
            self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Select a record to delete', 'error')

    def ClearSubjectContent(self):
        self.textSubjectName.setText('')
        self.LblSemester.setText('')

    #endregion

    
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = ViewProfession()

    app.exec_()