import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.StudentModel import StudentModel
from . FrmGeneric import GenericForm
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

        self.isUpdate = False

        # Create Fonts
        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        #------------------ Search QPushButtons ------------------#
        self.BtnSelectStudent = self.findChild(QtWidgets.QPushButton, 'BtnSelectStudent')
        self.BtnSelectStudent.setStyleSheet(self.globalStyles)
        self.BtnSelectStudent.clicked.connect(self.OpenGenericStudentForm)
        
        self.BtnSelectSemester = self.findChild(QtWidgets.QPushButton, 'BtnSelectSemester')        
        self.BtnSelectSemester.setStyleSheet(self.globalStyles)
        self.BtnSelectSemester.clicked.connect(self.OpenGenericSemesterForm)

        self.BtnSave = self.findChild(QtWidgets.QPushButton, 'BtnSave')
        self.BtnSave.setStyleSheet(self.globalStyles)
        self.BtnSave.clicked.connect(self.SaveStudent)

        self.BtnUpdate = self.findChild(QtWidgets.QPushButton, 'BtnUpdate')
        self.BtnUpdate.clicked.connect(self.UpdateStudent)
        self.BtnUpdate.setStyleSheet(self.globalStyles)

        self.BtnDelete = self.findChild(QtWidgets.QPushButton, 'BtnDelete')
        self.BtnDelete.setStyleSheet(self.globalStyles)
        self.BtnDelete.clicked.connect(self.RemoveStudent)

        self.BtnFilters = self.findChild(QtWidgets.QPushButton, 'BtnFilters')
        self.BtnFilters.setStyleSheet(self.globalStyles)

        self.BtnClearFilters = self.findChild(QtWidgets.QPushButton, 'BtnClearFilters')
        self.BtnClearFilters.setStyleSheet(self.globalStyles)

        #------------------ Search QComboBoxes ------------------#
        self.CboStudy = self.findChild(QtWidgets.QComboBox, 'CboStudy')
        self.CboStudy.setStyleSheet(self.globalStyles)
        self.CboStudy.setFont(self.fontQLineEdit)

        #------------------QGroupBoxes------------------#
        self.groupBoxOne = self.findChild(QtWidgets.QGroupBox, 'groupBoxOne')
        self.groupBoxOne.setStyleSheet(self.globalStyles)

        self.groupBoxTwo = self.findChild(QtWidgets.QGroupBox, 'groupBoxTwo')
        self.groupBoxTwo.setStyleSheet(self.globalStyles)

        self.groupBoxThree = self.findChild(QtWidgets.QGroupBox, 'groupBoxThree')
        self.groupBoxThree.setStyleSheet(self.globalStyles)
        
        self.CboActive = self.findChild(QtWidgets.QComboBox, 'CboActive')
        self.CboActive.setStyleSheet(self.globalStyles)
        self.CboActive.setFont(self.fontQLineEdit)

        #------------------ Search QLineEdits ------------------#
        self.textSemester = self.findChild(QtWidgets.QLineEdit, 'textSemester')
        self.textSemester.setStyleSheet(self.globalStyles)

        self.textSearch = self.findChild(QtWidgets.QLineEdit , 'textSearch')
        self.textSearch.setStyleSheet(self.globalStyles)

        #------------------ Search QLabel ------------------#
        self.LblStudent = self.findChild(QtWidgets.QLabel, 'LblStudent')
        self.LblStudent.setStyleSheet(self.globalStyles)

        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.hide()

        #------------------ Search QTableWidget ------------------#
        self.TableStudents = self.findChild(QtWidgets.QTableWidget, 'TableStudents')
        self.TableStudents.setFocusPolicy(QtCore.Qt.NoFocus)

        self.instaceUtil = FormatComponents()
        self.instaceStudentModel = StudentModel()

        self.fieldValue = ''

        self.LoadComboBox()

        self.LoadData()

    
    def LoadData(self):
        lstHeaderLabels = ('Student ID', 'Full Name', 'Semester', 'StudyShift', 'Active')
        self.instaceUtil.FormatQTableWidget(self.TableStudents,5,self.instaceStudentModel.GetAll(),lstHeaderLabels, 1)

    def SaveStudent(self):
        # Get only IDs
        userID = self.LblStudent.text()[0:2]
        semesterID = self.textSemester.text()[0:2]

        self.DataStudent = userID, semesterID, self.CboStudy.currentText(), self.CboActive.currentText()

        # Create new List
        self.lstStudent = list(self.DataStudent)
        # Validate the list
        for x in range(0,len(self.lstStudent)):
            if(len(str(self.lstStudent[x])) == 0):
                self.instaceUtil.ShowMessageLabel(self.LblMessage, 'Please complete all fields', 'error')
                return
        
        if(self.isUpdate):
            # Get Selected row
            row = self.TableStudents.currentRow()
            # Get Student ID
            currentStudentID = int(self.TableStudents.item(row,0).text())
            # Create new tuple
            self.dataToUpdate = semesterID, self.CboStudy.currentText(), self.CboActive.currentText()
            # Convert tuple to list
            self.lstToUpdate = list(self.dataToUpdate)
            # Added the id to the list to update
            self.lstToUpdate.append(currentStudentID)
            # Execute Update
            self.instaceStudentModel.Update(self.lstToUpdate)
            # Change Value State
            self.isUpdate = False
            # Refesh Data
            self.LoadData()
            # Clear QlineEdits
            self.Clear()
            # Clear Selection
            self.TableStudents.clearSelection()
        else:
            # Save Student
            message = self.instaceStudentModel.Add(self.lstStudent)
            # Show message
            self.instaceUtil.ShowMessageLabel(self.LblMessage, message, 'successful')
            # Clear QlineEdits
            self.Clear()
            # Refresh data
            self.LoadData()

    def UpdateStudent(self):
        row = self.TableStudents.currentRow()
        if(row >= 0):
            self.isUpdate = True
            # Join id and fullname
            studentInfo = self.TableStudents.item(row,0).text() + ' - ' + self.TableStudents.item(row,1).text()

            self.LblStudent.setText(studentInfo)
            self.textSemester.setText(self.TableStudents.item(row,2).text())
            self.CboStudy.setEditText(self.TableStudents.item(row,3).text())
            self.CboStudy.setEditText(self.TableStudents.item(row,4).text())
        else:
            self.instaceUtil.ShowMessageLabel(self.LblMessage, 'Select a record to update', 'error') 
        
    def RemoveStudent(self):
        row = self.TableStudents.currentRow()
        if(row >= 0):
            # Get StudentID
            currentStudentID = int(self.TableStudents.item(row,0).text())
            # Execute Delete
            message = self.instaceStudentModel.Delete(currentStudentID)
            # Show message
            self.instaceUtil.ShowMessageLabel(self.LblMessage,str(message),'successful')
            # Refresh Data
            self.LoadData()
        else:
            self.instaceUtil.ShowMessageLabel(self.LblMessage, 'Select a record to delete', 'error')
    
    def LoadComboBox(self):
        self.CboStudy.addItems(['Morning','Evening'])
        self.CboActive.addItems(['Active', 'Not Active'])
    
    def OpenGenericStudentForm(self):
        self.studentWindow = GenericForm("Students")
        self.studentWindow.BtnAcept.clicked.connect(self.GetStudentField)
        self.studentWindow.show()
       
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
            self.textSemester.setText(self.fieldValue)
            self.semesterWindow.close()

    def Clear(self):
        self.LblStudent.setText("")
        self.textSemester.setText("")

   
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    window = ViewStudent()

    app.exec_()