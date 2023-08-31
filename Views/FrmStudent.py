import os
import re
import sys
import uuid
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.StudentModel import StudentModel
from . FrmGeneric import ViewGeneric
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

        self.groupBoxOne = self.findChild(QtWidgets.QGroupBox, 'groupBoxOne')
        self.groupBoxOne.setStyleSheet(self.globalStyles)

        self.BtnSelectStudent = self.findChild(QtWidgets.QPushButton, 'BtnSelectStudent')
        self.BtnSelectStudent.setStyleSheet(self.globalStyles)
        self.BtnSelectStudent.setFont(self.fontQLineEdit)
        self.BtnSelectStudent.clicked.connect(self.OpenGenericStudentForm)
        
        self.BtnGenerateEnrollment = self.findChild(QtWidgets.QPushButton, 'BtnGenerateEnrollment')
        self.BtnGenerateEnrollment.setFont(self.fontQLineEdit)
        self.BtnGenerateEnrollment.clicked.connect(self.GenerateUUID)

        self.BtnSelectSection = self.findChild(QtWidgets.QPushButton, 'BtnSelectSection')
        self.BtnSelectSection.setFont(self.fontQLineEdit)
        self.BtnSelectSection.clicked.connect(self.OpenGenericSectionForm)

        self.CboStudy = self.findChild(QtWidgets.QComboBox, 'CboStudy')
        self.CboStudy.setStyleSheet(self.globalStyles)
        self.CboStudy.setFont(self.fontQLineEdit)

        self.CboActive = self.findChild(QtWidgets.QComboBox, 'CboActive')
        self.CboActive.setStyleSheet(self.globalStyles)
        self.CboActive.setFont(self.fontQLineEdit)

        self.DateEnrollment = self.findChild(QtWidgets.QDateEdit, 'DateEnrollment')
        self.DateEnrollment.setStyleSheet(self.globalStyles)

        self.textSearch = self.findChild(QtWidgets.QLineEdit , 'textSearch')
        self.textSearch.setStyleSheet(self.globalStyles)
        self.textSearch.textChanged.connect(self.ApplyStudentFilters)

        self.TableStudents = self.findChild(QtWidgets.QTableWidget, 'TableStudents')
        self.TableStudents.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TableStudents.customContextMenuRequested.connect(self.GenerateMenu)
        self.TableStudents.viewport().installEventFilter(self)
        self.TableStudents.setFocusPolicy(QtCore.Qt.NoFocus)

        self.groupBoxTwo = self.findChild(QtWidgets.QGroupBox, 'groupBoxTwo')
        self.groupBoxTwo.setStyleSheet(self.globalStyles)

        self.BtnSave = self.findChild(QtWidgets.QPushButton, 'BtnSave')
        self.BtnSave.setStyleSheet(self.globalStyles)
        self.BtnSave.clicked.connect(self.SaveStudent)

        self.BtnUpdateStudent = self.findChild(QtWidgets.QPushButton, 'BtnUpdate')
        self.BtnUpdateStudent.setStyleSheet(self.globalStyles)
        self.BtnUpdateStudent.clicked.connect(self.UpdateStudent)

        self.BtnDelete = self.findChild(QtWidgets.QPushButton, 'BtnDelete')
        self.BtnDelete.setStyleSheet(self.globalStyles)
        self.BtnDelete.clicked.connect(self.RemoveStudent)

        self.BtnFilters = self.findChild(QtWidgets.QPushButton, 'BtnFilters')
        self.BtnFilters.setStyleSheet(self.globalStyles)
        self.BtnFilters.clicked.connect(self.OpenFiltersStudent)
        self.BtnFilters.setToolTip('Open Filters')
        self.BtnFilters.clicked.connect(self.ResetAll)

        self.BtnClearFilters = self.findChild(QtWidgets.QPushButton, 'BtnClearFilters')
        self.BtnClearFilters.setStyleSheet(self.globalStyles)
        self.BtnClearFilters.setToolTip('Clear Filters')
        self.BtnClearFilters.clicked.connect(self.ResetAll)

        self.LblStudent = self.findChild(QtWidgets.QLabel, 'LblStudent')
        
        self.LblEnrollment = self.findChild(QtWidgets.QLabel, 'LblEnrollment')

        self.LblSection = self.findChild(QtWidgets.QLabel, 'LblSection')
        
        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.hide()

        # Create instances
        self.instanceUtil = FormatComponents()
        self.instanceStudentModel = StudentModel()
        self.fieldValue = ''

        # Execute some methods
        self.LoadComboBox()
        self.LoadStudentData()

    #region ---------------- <Student Methods> ----------------
    def LoadStudentData(self):
        self.lstHeaderLabelsStudent = ('User Id', 'Full Name', 'SchoolEnrollment', 'StudyShift', 'Active')

        self.instanceUtil.FormatQTableWidget(self.TableStudents,5,
                                             self.instanceStudentModel.GetStudentData(),
                                             self.lstHeaderLabelsStudent, 1)

        # Init QDate 
        dateFromString = QtCore.QDate().currentDate().toString(QtCore.Qt.ISODate)
        currentDate = QtCore.QDate.fromString(dateFromString, 'yyyy-MM-dd')
        self.DateEnrollment.setDate(currentDate)

    def SaveStudent(self):
        
        self.objectList = [self.LblStudent.text(),
                            self.LblEnrollment.text(), 
                            self.DateEnrollment.dateTime().toString('yyyy-MM-dd'),
                            self.CboStudy.currentText(), 
                            self.CboActive.currentText(),
                            self.LblSection.text()]
        
        for x in range(len(self.objectList)):
            if(self.objectList[x] == ''):
                self.instanceUtil.ShowMessageLabel(self.LblMessage,'Please compleate all Fields','error')
                return

        
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
            # Get UserId and SectionID to Enroll
            studentId = int(re.search(r'\d+',self.LblStudent.text()).group())
            sectionId = int(re.search(r'\d+',self.LblSection.text()).group())

            # Update list with new values
            self.objectList[0] = studentId
            self.objectList[5] = sectionId

            # Save Student
            message = self.instanceStudentModel.Add(self.objectList)
            # Refresh Data
            self.LoadStudentData()
            # Clear Items
            self.Clear()
            # Show message
            if('error' in message):
                self.instanceUtil.ShowMessageLabel(self.LblMessage, str(message[0]), str(message[1]))
            else:
                self.instanceUtil.ShowMessageLabel(self.LblMessage, str(message), 'successful')
    
    def UpdateStudent(self):
        currentStudenRow = self.TableStudents.currentRow()        
        if(currentStudenRow >= 0):
            # Get Student Info
            studentInfo =  self.TableStudents.item(currentStudenRow,0).text()
            studentInfo += ' - '
            studentInfo += self.TableStudents.item(currentStudenRow,1).text()           
      
            self.isUpdateInfoStudent = True
            # Fill Items
            self.LblStudent.setText(studentInfo)
            self.LblEnrollment.setText(self.TableStudents.item(currentStudenRow, 2).text())    
            self.CboStudy.setEditText(self.TableStudents.item(currentStudenRow,3).text())
            self.CboActive.setEditText(self.TableStudents.item(currentStudenRow,4).text())
        else:
            self.instanceUtil.ShowMessageLabel(self.LblMessage, 'Select a Record to Update', 'error')

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
        self.studentWindow = ViewGeneric("Students-not-Enrollment")
        self.studentWindow.BtnAcept.clicked.connect(self.GetStudentField)
        self.studentWindow.show()

    def OpenGenericSectionForm(self):
        self.sectionWindow = ViewGeneric("Sections")
        self.sectionWindow.BtnAcept.clicked.connect(self.GetSectionField)
        self.sectionWindow.show()

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

    def GetStudentField(self):
        self.fieldValue = self.studentWindow.RetrieveData()
        if(self.fieldValue != ''):
            self.LblStudent.setText(self.fieldValue)
            self.studentWindow.close()

    def GetSectionField(self):
        self.fieldValue = self.sectionWindow.RetrieveData()
        if(self.fieldValue != ''):
            self.LblSection.setText(self.fieldValue)
            self.sectionWindow.close()
    
    def Clear(self):
        self.LblStudent.setText("")
        self.LblSection.setText("")
        self.LblEnrollment.setText("")

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
    
    def ResetAll(self):
        self.keyStudent = 'ID'
        self.fieldValue = ''
    
    #endregion
 

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    window = ViewStudent()

    app.exec_()