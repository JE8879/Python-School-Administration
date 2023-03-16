import os
import sys
import uuid
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.StudentModel import StudentModel
from Models.SemesterStudentModel import SemesterStudentModel
from . ManageStudent import ManageStudent
from . ManageSemester import ManageSemester
from . FrmGeneric import GenericForm
from . FrmFilter import ViewFilter
from . Utils.Format import FormatComponents


PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir))
sys.path.append(PROJECT_ROOT)

class ViewStudent(QtWidgets.QWidget):
    # Contructor
    def __init__(self):
        # Find components and assign properties
        super(ViewStudent, self).__init__()

        # Load Template-UI-File
        uic.loadUi('Views/Templates/FrmStudent.ui',self)
        self.setStyleSheet('background-color: rgb(46, 64, 83);')

        # Load styles CSS
        with open('./Assets/App.css') as fileCSS:
            self.globalStyles = fileCSS.read()

        self.isUpdateInfoStudent = False
        self.isUpdateSemesterStudent = False

        # Create Fonts
        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        self.fontQLabel = QtGui.QFont()
        self.fontQLabel.setFamily("Century Gothic")
        self.fontQLabel.setPointSize(11)
        self.fontQLabel.setBold(True)
        self.fontQLabel.setWeight(75)

        self.keyStudent = 'ID'
        self.keySemester = 'ID'

        #------------------ Search QPushButtons ------------------#
        self.BtnSelectStudent = self.findChild(QtWidgets.QPushButton, 'BtnSelectStudent')
        self.BtnSelectStudent.setStyleSheet(self.globalStyles)
        self.BtnSelectStudent.setFont(self.fontQLineEdit)
        self.BtnSelectStudent.clicked.connect(self.OpenGenericStudentForm)

        self.BtnGenerateEnrollment = self.findChild(QtWidgets.QPushButton, 'BtnGenerateEnrollment')
        self.BtnGenerateEnrollment.setFont(self.fontQLineEdit)
        self.BtnGenerateEnrollment.clicked.connect(self.GenerateUUID)
        
        self.BtnSelectSemester = self.findChild(QtWidgets.QPushButton, 'BtnSelectSemester')        
        self.BtnSelectSemester.setStyleSheet(self.globalStyles)
        self.BtnSelectSemester.setFont(self.fontQLineEdit)
        self.BtnSelectSemester.clicked.connect(self.OpenGenericSemesterForm)

        self.BtnSave = self.findChild(QtWidgets.QPushButton, 'BtnSave')
        self.BtnSave.setStyleSheet(self.globalStyles)
        self.BtnSave.clicked.connect(self.SaveStudent)

        self.BtnUpdateStudent = self.findChild(QtWidgets.QPushButton, 'BtnUpdateStudent')
        self.BtnUpdateStudent.setStyleSheet(self.globalStyles)
        self.BtnUpdateStudent.clicked.connect(self.UpdateStudent)

        self.BtnDelete = self.findChild(QtWidgets.QPushButton, 'BtnDelete')
        self.BtnDelete.setStyleSheet(self.globalStyles)
        self.BtnDelete.clicked.connect(self.RemoveStudent)

        self.BtnPassStudent = self.findChild(QtWidgets.QPushButton, 'BtnPassStudent')
        self.BtnPassStudent.setStyleSheet(self.globalStyles)
        self.BtnPassStudent.clicked.connect(self.PassStudent)

        self.BtnFiltersStudent = self.findChild(QtWidgets.QPushButton, 'BtnFiltersStudent')
        self.BtnFiltersStudent.setStyleSheet(self.globalStyles)
        self.BtnFiltersStudent.clicked.connect(self.OpenFiltersStudent)
        self.BtnFiltersStudent.setToolTip('Open Filters')
        self.BtnFiltersStudent.clicked.connect(self.ResetAll)

        self.BtnClearFilters = self.findChild(QtWidgets.QPushButton, 'BtnClearFilters')
        self.BtnClearFilters.setStyleSheet(self.globalStyles)
        self.BtnClearFilters.setToolTip('Clear Filters')
        self.BtnClearFilters.clicked.connect(self.ResetAll)
        # self.BtnClearFilters.clicked.connect()

        #------------------ Search QComboBoxes ------------------#
        self.CboStudy = self.findChild(QtWidgets.QComboBox, 'CboStudy')
        self.CboStudy.setStyleSheet(self.globalStyles)
        self.CboStudy.setFont(self.fontQLineEdit)

        # -------------------------Componenets SemesterStuednt ------------------------------#
        self.BtnSaveSemesterStudent = self.findChild(QtWidgets.QPushButton, 'BtnSaveSemester')
        self.BtnSaveSemesterStudent.clicked.connect(self.SaveSemesterStudent)

        self.BtnUpdateSemester = self.findChild(QtWidgets.QPushButton, 'BtnUpdateSemester')
        self.BtnUpdateSemester.clicked.connect(self.UpdateSemesterStudent)

        self.BtnDeleteStudentSemester = self.findChild(QtWidgets.QPushButton, 'BtnDeleteStudentSemester')
        self.BtnDeleteStudentSemester.clicked.connect(self.RemoveStudentSemester)

        self.BtnFiltersSemester = self.findChild(QtWidgets.QPushButton, 'BtnFiltersSemester')
        self.BtnFiltersSemester.clicked.connect(self.OpenFiltersSememester)
        self.BtnFiltersSemester.setToolTip('Open Filters')

        self.BtnClearFiltersSemester = self.findChild(QtWidgets.QPushButton, 'BtnClearFiltersSemester')
        self.BtnClearFiltersSemester.setToolTip('Clear Filters')

        #------------------QGroupBoxes------------------#
        self.groupBoxOne = self.findChild(QtWidgets.QGroupBox, 'groupBoxOne')
        self.groupBoxOne.setStyleSheet(self.globalStyles)

        self.groupBoxTwo = self.findChild(QtWidgets.QGroupBox, 'groupBoxTwo')
        self.groupBoxTwo.setStyleSheet(self.globalStyles)

        self.groupBoxThree = self.findChild(QtWidgets.QGroupBox, 'groupBoxThree')
        self.groupBoxThree.setStyleSheet(self.globalStyles)

        self.groupBoxFour = self.findChild(QtWidgets.QGroupBox, 'groupBoxFour')
        self.groupBoxFour.setStyleSheet(self.globalStyles)
        
        self.CboActive = self.findChild(QtWidgets.QComboBox, 'CboActive')
        self.CboActive.setStyleSheet(self.globalStyles)
        self.CboActive.setFont(self.fontQLineEdit)

        #------------------ Search QLineEdits ------------------#
        self.textSearch = self.findChild(QtWidgets.QLineEdit , 'textSearch')
        self.textSearch.setStyleSheet(self.globalStyles)
        self.textSearch.textChanged.connect(self.ApplyStudentFilters)

        self.textSearchStuSemester = self.findChild(QtWidgets.QLineEdit, 'textSearchStuSemester')
        self.textSearchStuSemester.setStyleSheet(self.globalStyles)
        self.textSearchStuSemester.textChanged.connect(self.ApplyFiltersSemesterStudent)
        
        #------------------ Search QLabel ------------------#
        self.LblStudent = self.findChild(QtWidgets.QLabel, 'LblStudent')
        # self.LblStudent.setStyleSheet(self.globalStyles)

        self.LblEnrollment = self.findChild(QtWidgets.QLabel, 'LblEnrollment')

        self.LblSemesterStudent = self.findChild(QtWidgets.QLabel, 'LblStudentSemester')
        
        self.LblSemester = self.findChild(QtWidgets.QLabel, 'LblSemester')
        # self.LblSemester.setStyleSheet(self.globalStyles)

        # Create Actions
        self.actionEditStudent = QtWidgets.QAction('Edit InfoStudent...')
        self.actionEditStudent.triggered.connect(self.ExecuteActionInfoSemester)

        self.actionEditSemesterStudent = QtWidgets.QAction('Edit SemesterStudent...')
        self.actionEditSemesterStudent.triggered.connect(self.ExecuteActionsSemesterStuent)

        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.hide()

        #------------------ Search QTableWidget ------------------#
        self.TableStudents = self.findChild(QtWidgets.QTableWidget, 'TableStudents')
        self.TableStudents.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TableStudents.customContextMenuRequested.connect(self.GenerateMenu)
        self.TableStudents.viewport().installEventFilter(self)
        self.TableStudents.setFocusPolicy(QtCore.Qt.NoFocus)

        self.TableStudentSemester = self.findChild(QtWidgets.QTableWidget, 'TableStudentSemester')
        self.TableStudentSemester.setFocusPolicy(QtCore.Qt.NoFocus)

        self.instanceUtil = FormatComponents()
        self.instanceStudentModel = StudentModel()
        self.instanceManageStudent = ManageStudent()
        self.instanceManageSemester = ManageSemester()

        self.instanceSemesterStudentModel = SemesterStudentModel()

        self.fieldValue = ''

        self.LoadComboBox()

        self.LoadStudentData()
        self.LoadSemesterStudent()

        self.LoadOptions()
 
    def LoadStudentData(self):
        self.lstHeaderLabelsStudent = ('User Id', 'Full Name', 'SchoolEnrollment', 'StudyShift', 'Active')
        self.instanceUtil.FormatQTableWidget(self.TableStudents,5,self.instanceManageStudent.GetAll(),self.lstHeaderLabelsStudent, 1)

    def LoadSemesterStudent(self):
        self.lstHeaderLabelsSemesterStuedent = ('Semester Stud ID', 'Full Name', 'Semester')
        self.instanceUtil.FormatQTableWidget(self.TableStudentSemester,3,self.instanceManageSemester.GetSemesterStudent(), self.lstHeaderLabelsSemesterStuedent, 1)

    def SaveStudent(self):
        # Get only IDs
        userID = self.LblStudent.text()[0:2]
        # Create Array of items
        self.DataStudent = userID, self.LblEnrollment.text() ,self.CboStudy.currentText(), self.CboActive.currentText()
        
        if(self.isUpdateInfoStudent):
            # Get Selected row
            row = self.TableStudents.currentRow()
            # Get Student ID
            currentStudentID = self.TableStudents.item(row,0).text()
            # Create new tuple
            self.dataToUpdate = self.CboStudy.currentText(), self.CboActive.currentText()
            # Convert tuple to list
            self.lstToUpdate = list(self.dataToUpdate)
            # Added the id to the list to update
            self.lstToUpdate.append(currentStudentID)
            # Execute Update
            message = self.instanceStudentModel.Update(self.lstToUpdate)
            # Show Message
            self.instanceUtil.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Change Value State
            self.isUpdateInfoStudent = False
            # Refesh Data
            self.LoadStudentData()
            # Clear QlineEdits
            self.Clear()
            # Clear Selection
            self.TableStudents.clearSelection()
            # Enabled Buttons
            self.BtnGenerateEnrollment.setEnabled(True)
            self.BtnSelectSemester.setEnabled(True)
            self.BtnSelectStudent.setEnabled(True)
            return        
        else:
            # Save Student
            message = self.instanceManageStudent.AddStudent(self.DataStudent)
            # Refresh Data
            self.LoadStudentData()
            # Clear Items
            self.Clear()
            # Show message
            if('error' in message):
                self.instanceUtil.ShowMessageLabel(self.LblMessage, str(message[0]), str(message[1]))
            else:
                self.instanceUtil.ShowMessageLabel(self.LblMessage, str(message), 'successful')
    
    def SaveSemesterStudent(self):
        # Get only IDs
        userID = self.LblSemesterStudent.text()[0:1]
        semesterID = self.LblSemester.text()[0:1]

        arrItemsSemesStudent = userID, semesterID

        if(self.isUpdateSemesterStudent):
            # Get Selected row
            row = self.TableStudentSemester.currentRow()
            # Get SemesterStudent ID
            currentSemesStuid = self.TableStudentSemester.item(row,0).text()
            # Create new Tuple
            self.dataSemesterStudent = self.LblSemester.text()[0:2]
            # Convert tuple to list
            self.lstSemesterStudent = list(self.dataSemesterStudent)
            # Add SemesterStudentID
            self.lstSemesterStudent.append(currentSemesStuid)
            # Remove Empty items
            self.lstSemesterStudent = ' '.join(self.lstSemesterStudent).split()       
            # Execute Update
            message = self.instanceSemesterStudentModel.Update(self.lstSemesterStudent)
            # Show Message
            self.instanceUtil.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Change Value States
            self.isUpdateSemesterStudent = False
            # Refresh Data
            self.LoadSemesterStudent()
            # Clear Items
            self.Clear()
            # Clear Selection
            self.TableStudentSemester.clearSelection()
        else:
            # Add Record
            message = self.instanceManageSemester.AddSemesterStudent(arrItemsSemesStudent)
            # Refresh Data
            self.LoadSemesterStudent()
            # Clear Labels
            self.Clear()
             # Show message
            if('error' in message):
                self.instanceUtil.ShowMessageLabel(self.LblMessage, str(message[0]), str(message[1]))
            else:
                self.instanceUtil.ShowMessageLabel(self.LblMessage, str(message), 'successful')
    
    def RemoveStudentSemester(self):
        row = self.TableStudentSemester.currentRow()
        if(row >= 0):
            # Get StudentSemesterID
            currentStudentSemesterID = int(self.TableStudentSemester.item(row,0).text())
            # Execute Sentence
            message = self.instanceSemesterStudentModel.Delete(currentStudentSemesterID)
            # Show Message 
            self.instanceUtil.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Refresh Data
            self.LoadSemesterStudent()
        else:
            self.instanceUtil.ShowMessageLabel(self.LblMessage, 'Select a record to delete', 'error')

    def ExecuteActionInfoSemester(self):
        self.GlobalUpdate(1)

    def ExecuteActionsSemesterStuent(self):
        self.GlobalUpdate(2)

    def GlobalUpdate(self, opt = None):
        currentStudenRow = self.TableStudents.currentRow()
        currentSemesterRow = self.TableStudentSemester.currentRow()

        if(currentStudenRow >= 0):
            # Check opt1 to updateInfoStudent
            if(opt == 1):
                # Get Student Info
                studentInfo = self.TableStudents.item(currentStudenRow,0).text() + ' - ' + self.TableStudents.item(currentStudenRow,1).text()           
      
                self.isUpdateInfoStudent = True
                # Fill Items
                self.LblStudent.setText(studentInfo)
                self.LblEnrollment.setText(self.TableStudents.item(currentStudenRow, 2).text())    
                self.CboStudy.setEditText(self.TableStudents.item(currentStudenRow,3).text())
                self.CboActive.setEditText(self.TableStudents.item(currentStudenRow,4).text())
                # Disable Buttons
                self.BtnGenerateEnrollment.setEnabled(False)
                self.BtnSelectStudent.setEnabled(False)
        if(currentSemesterRow >= 0):
            if(opt == 2):
                # Get Student Info
                studentInfo = self.TableStudentSemester.item(currentSemesterRow,0).text() + ' - ' + self.TableStudentSemester.item(currentSemesterRow,1).text()
                self.isUpdateSemesterStudent = True

                self.LblSemesterStudent.setText(studentInfo)
                self.LblSemester.setText(self.TableStudentSemester.item(currentSemesterRow,2).text())                
        else:
            self.instanceUtil.ShowMessageLabel(self.LblMessage, 'Select a record to update', 'error')
    
    def UpdateStudent(self):
        self.GlobalUpdate(1)

    def UpdateSemesterStudent(self):
        self.GlobalUpdate(2)
    
    def RemoveStudent(self):
        row = self.TableStudents.currentRow()
        if(row >= 0):
            # Get StudentID
            currentStudentID = int(self.TableStudents.item(row,0).text())
            # Execute Delete
            message = self.instanceSemesterStudentModel.Delete(currentStudentID)
            # Show message
            self.instanceUtil.ShowMessageLabel(self.LblMessage,str(message),'successful')
            # Refresh Data
            self.LoadStudentData()
        else:
            self.instanceUtil.ShowMessageLabel(self.LblMessage, 'Select a record to delete', 'error')
    
    def LoadComboBox(self):
        self.CboStudy.addItems(['Morning','Evening'])
        self.CboActive.addItems(['Active', 'Not Active'])
    
    def OpenGenericStudentForm(self):
        self.studentWindow = GenericForm("Students")
        self.studentWindow.BtnAcept.clicked.connect(self.GetStudentField)
        self.studentWindow.show()

    def OpenFiltersStudent(self):
        # Create new dictionary with our choices
        dicHeaderStudent = {'fullname':'Full Name', 'studyShift':'StudyShift', 'active':'Active'}
        # Pass dictionary to contructor
        self.instanceFilter = ViewFilter(dicHeaderStudent)
        self.instanceFilter.BtnAcept.clicked.connect(self.GetFieldStudentSelected)
        self.instanceFilter.show()
    
    def GetFieldStudentSelected(self):
        self.keyStudent = self.instanceFilter.RetrieveSelectedChoices()
        self.instanceFilter.close()

    def ApplyStudentFilters(self):
        try:
            if(self.keyStudent == 'ID'):
                idFieldStudent = int(self.textSearch.text())
                result = self.instanceStudentModel.SearchLikeStudent(self.keyStudent, idFieldStudent)
                self.instanceUtil.FormatQTableWidget(self.TableStudents, 5, result, self.lstHeaderLabelsStudent, 2)
            else:
                result = self.instanceStudentModel.SearchLikeStudent(self.keyStudent, self.textSearch.text())
                self.instanceUtil.FormatQTableWidget(self.TableStudents, 5, result, self.lstHeaderLabelsStudent, 2)

                if(self.textSearch.text() == ''):
                    self.LoadStudentData()
        except:
            self.LoadStudentData()

    def OpenFiltersSememester(self):
        dicHeaderSemesterStudent = {'fullname':'Full Name', 'semester':'Semester'}
         # Pass dictionary to contructor
        self.instanceFilter = ViewFilter(dicHeaderSemesterStudent)
        self.instanceFilter.BtnAcept.clicked.connect(self.GetFieldSemesterStudenSelected)
        self.instanceFilter.show()

    def GetFieldSemesterStudenSelected(self):
        self.keySemester = self.instanceFilter.RetrieveSelectedChoices()
        self.instanceFilter.close()
    
    def ApplyFiltersSemesterStudent(self, text):
        try:
            if(self.keySemester == 'ID'):
                idFieldSemesterStudent = int(self.textSearchStuSemester.text())
                result = self.instanceSemesterStudentModel.SearchLikeSemesterStudent(self.keySemester, idFieldSemesterStudent)
                self.instanceUtil.FormatQTableWidget(self.TableStudentSemester, 3, result,  self.lstHeaderLabelsSemesterStuedent, 2)
            else:
                result = self.instanceSemesterStudentModel.SearchLikeSemesterStudent(self.keySemester, self.textSearchStuSemester.text())
                self.instanceUtil.FormatQTableWidget(self.TableStudentSemester, 3, result, self.lstHeaderLabelsSemesterStuedent, 2)

            if(len(text) == 0):
                    self.LoadSemesterStudent()
        except:
            self.LoadSemesterStudent()

    def OpenGenericSemesterForm(self):
        self.semesterWindow = GenericForm("Semesters")
        self.semesterWindow.BtnAcept.clicked.connect(self.GetSemesterField)
        self.semesterWindow.show()
       
    def GetStudentField(self):
        self.fieldValue = self.studentWindow.RetrieveData()
        if(self.fieldValue != ''):
            self.LblStudent.setText(self.fieldValue)
            self.studentWindow.close()

    def GetSemesterField(self):
        self.fieldValue = self.semesterWindow.RetrieveData()
        if(self.fieldValue != ''):
            self.LblSemester.setText(self.fieldValue)
            self.semesterWindow.close()

    def Clear(self):
        self.LblStudent.setText("")
        self.LblSemester.setText("")
        self.LblEnrollment.setText("")
        self.LblSemesterStudent.setText("")

    def GenerateUUID(self):
        enrollmentID = uuid.uuid4()        
        self.LblEnrollment.setText(str(enrollmentID))

    def eventFilter(self, source, event):
        if(event.type() == QtCore.QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.RightButton and source is self.TableStudents.viewport()):
            currentItem = self.TableStudents.itemAt(event.pos())
            
            if(currentItem is not None):
                self.menu = QtWidgets.QMenu(self)
                self.menu.setStyleSheet(self.globalStyles)
                self.menu.addAction('Editar Info Student...')
                self.menu.addAction('Editar Info SemesterStudent...')
        return super(ViewStudent, self).eventFilter(source,event)

    def GenerateMenu(self, pos):
        self.menu.exec_(self.TableStudents.mapToGlobal(pos))

    def LoadOptions(self):
        menuStudent = QtWidgets.QMenu()
        # Add Actions
        menuStudent.addAction(self.actionEditStudent)
        menuStudent.addAction(self.actionEditSemesterStudent)
    
    def PassStudent(self):
        currentRow = self.TableStudents.currentRow()
        if(currentRow >= 0):
            studentInfo = self.TableStudents.item(currentRow,0).text() + ' ' + self.TableStudents.item(currentRow,1).text()
            self.LblSemesterStudent.setText(str(studentInfo))
            self.TableStudents.clearSelection()
        else:
            self.instanceUtil.ShowMessageLabel(self.LblMessage, 'Select a record to pass', 'error')  
   
    def ResetAll(self):
        self.keyStudent = 'ID'
        self.keySemester = 'ID'
        self.fieldValue = ''

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    window = ViewStudent()

    app.exec_()