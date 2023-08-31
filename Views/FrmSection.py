import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.SectionModel import SectionModel
from . Utils.Format import FormatComponents
from . FrmGeneric import ViewGeneric

class ViewSection(QtWidgets.QWidget):
    # Constructor
    def __init__(self):
        # Find components and assign properties
        super(ViewSection, self).__init__()

        # Load Template-UI-File
        uic.loadUi('Views/Templates/FrmSection.ui',self)

        # Load styles CSS
        with open('./Assets/App.css') as fileCSS:
            self.globalStyles = fileCSS.read()

        # Create Fonts
        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        self.fontQLabel = QtGui.QFont()
        self.fontQLabel.setFamily("Century Gothic")
        self.fontQLabel.setPointSize(11)
        self.fontQLabel.setBold(True)
        self.fontQLabel.setWeight(75)

        self.groupBoxOne = self.findChild(QtWidgets.QGroupBox, 'groupBoxOne')        
        self.groupBoxOne.setStyleSheet(self.globalStyles)

        self.textSectionName = self.findChild(QtWidgets.QLineEdit, 'textSectionName')
        self.textSectionName.setStyleSheet(self.globalStyles)

        self.BtnSemester = self.findChild(QtWidgets.QPushButton, 'BtnSelectSemester')
        self.BtnSemester.setStyleSheet(self.globalStyles)
        self.BtnSemester.clicked.connect(self.OpenGenericSemesterForm)

        self.LblSection = self.findChild(QtWidgets.QLabel, 'LblSection')

        self.groupBoxTwo = self.findChild(QtWidgets.QGroupBox, 'groupBoxTwo')
        self.groupBoxTwo.setStyleSheet(self.globalStyles)

        self.BtnSave = self.findChild(QtWidgets.QPushButton, 'BtnSave')
        self.BtnSave.setStyleSheet(self.globalStyles)
        self.BtnSave.clicked.connect(self.SaveSection)

        self.BtnUpdate = self.findChild(QtWidgets.QPushButton, 'BtnUpdate')
        self.BtnUpdate.setStyleSheet(self.globalStyles)

        self.BtnDelete = self.findChild(QtWidgets.QPushButton, 'BtnDelete')
        self.BtnDelete.setStyleSheet(self.globalStyles)

        self.groupBoxThree = self.findChild(QtWidgets.QGroupBox, 'groupBoxThree')
        self.groupBoxThree.setStyleSheet(self.globalStyles)

        self.textSearch = self.findChild(QtWidgets.QLineEdit, 'textSearch')
        self.textSearch.setStyleSheet(self.globalStyles)

        self.BtnFilters = self.findChild(QtWidgets.QPushButton, 'BtnFilters')
        self.BtnFilters.setStyleSheet(self.globalStyles)

        self.BtnClearFilters = self.findChild(QtWidgets.QPushButton, 'BtnClearFilters')
        self.BtnClearFilters.setStyleSheet(self.globalStyles)

        self.tableSection = self.findChild(QtWidgets.QTableWidget, 'tableSection')
        
        self.LblMessage = self.findChild(QtWidgets.QLabel, 'LblMessage')
        self.LblMessage.hide()

        # Create Instances
        self.instanceSection = SectionModel()
        self.instanceFormat = FormatComponents()

        self.Load()
        self.fieldValue = ''

    def Load(self):
        lstHeaderLabelsSections = ('Section ID', 'Section Name', 'Semester Name','Profession Name')
        self.instanceFormat.FormatQTableWidget(self.tableSection, 4, self.instanceSection.GetAll(), lstHeaderLabelsSections, 1)

    def SaveSection(self):
        # Create objectList 
        self.objectList = [self.textSectionName.text(),self.LblSection.text()]

        # Validate list
        for x in range(0,len(self.objectList)):
            if(len(str(self.objectList[x])) == 0):
                self.instanceFormat.ShowMessageLabel(self.LblMessage, 'Please complete all fields', 'error')
                return
        
        # Delete element to convert to int
        del self.objectList[1]
        # Get Semester id as Integer
        SemesterID  = int(re.search(r'\d+',self.LblSection.text()).group())
        # Add ID to list again
        self.objectList.insert(1,SemesterID)

        # Save Section
        message = self.instanceSection.Add(self.objectList)
        # Show Message
        self.instanceFormat.ShowMessageLabel(self.LblMessage, message, 'successful')
        # Refresh Data
        self.Load()
        # Clear
        self.ClearContents()

    def OpenGenericSemesterForm(self):
        self.semesterWindow = ViewGeneric('Semesters')
        self.semesterWindow.BtnAcept.clicked.connect(self.GetFieldValueSemester)
        self.semesterWindow.show()

    def GetFieldValueSemester(self):
        self.fieldValue = self.semesterWindow.RetrieveData()
        if(self.fieldValue != ''):
            self.LblSection.setText(self.fieldValue)
            self.semesterWindow.close()

    def ClearContents(self):
        self.textSectionName.clear()
        self.LblSection.clear()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = ViewSection()

    app.exec_()