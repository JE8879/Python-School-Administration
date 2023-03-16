import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.PositionModel import PostionModel
from Models.StudentModel import StudentModel
from Models.ProfessionModel import ProfessionModel
from . Utils.Format import FormatComponents

class GenericForm(QtWidgets.QWidget):
    # Constructor
    def __init__(self, searchParameter):
        #Properties
        self.searchParameter = searchParameter

        # Find components and assing properties
        super(GenericForm, self).__init__()

        # Load Template UI-File
        uic.loadUi('Views/Templates/GenericForm.ui',self)
        self.setMaximumSize(QtCore.QSize(400,300))
        self.setMinimumSize(QtCore.QSize(400,300))
        self.setStyleSheet('background-color: rgb(46, 64, 83);')
        
        # Load Styles CSS
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

        #--------------------- Search Buttons ---------------------#
        self.BtnAcept = self.findChild(QtWidgets.QPushButton, 'BtnAcept')
        self.BtnAcept.setStyleSheet(self.globalStyles)

        self.BtnCancel = self.findChild(QtWidgets.QPushButton, 'BtnCancel')
        self.BtnCancel.clicked.connect(self.close)
        self.BtnCancel.setStyleSheet(self.globalStyles)

        # -------------------- QTableWidget ------------------------#
        self.GenericTable = self.findChild(QtWidgets.QTableWidget, 'GenericTable')
        self.GenericTable.setStyleSheet(self.globalStyles)
        self.GenericTable.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.groupBox = self.findChild(QtWidgets.QGroupBox, 'groupBox')
        self.groupBox.setStyleSheet(self.globalStyles)
        self.result = ''

        #---------------------- QLineEdits ----------------------------#
        self.textSearch = self.findChild(QtWidgets.QLineEdit, 'textSearch')
        self.textSearch.setStyleSheet(self.globalStyles)
        self.textSearch.setFont(self.fontQLineEdit)

        self.instancePosition = PostionModel()
        self.instanceStudent = StudentModel()
        self.instaceFormat = FormatComponents()
        self.instanceProfession = ProfessionModel()

        self.UploadMatches()

    def UploadMatches(self):
        searchParameter = self.searchParameter

        match searchParameter:
            case "Positions":
                self.setWindowTitle("Positions")
                self.LoadPositions()
            case "Students":
                self.setWindowTitle("Students")
                self.textSearch.setPlaceholderText("Search By Student ID")
                # self.textSearch.textChanged.connect(self.LoadStudents)
                self.LoadStudents()

            case "Semesters":
                self.setWindowTitle("Semesters")
                self.LoadSemesters()

            case "Professions":
                self.setWindowTitle("Professions")
                self.LoadProfessions()
            
            case "Payments":
                self.textSearch.hide()
                self.setWindowTitle("Payments")
                self.LoadPaymentTable()

    def LoadPositions(self):
        lstHeaderLabels = ('Position ID', 'Position Name')
        self.instaceFormat.FormatQTableWidget(self.GenericTable, 2, self.instancePosition.GetPositions(), lstHeaderLabels, 1)

    def LoadStudents(self):
        lstHeaderLabels = ('ID', 'Full Name')
        # result = self.instanceStudent.GetOnlyOneStuent('ID',self.textSearch.text())
        self.instaceFormat.FormatQTableWidget(self.GenericTable, 2, self.instanceStudent.GetStudents(), lstHeaderLabels, 1)

    def LoadSemesters(self):
        lstHeaderLabels = ('ID', 'Semester Name', 'School Year')
        self.instaceFormat.FormatQTableWidget(self.GenericTable, 3, self.instanceStudent.GetSemesters(), lstHeaderLabels, 1)

    def LoadProfessions(self):
        lstHeaderLabels = ('ID', 'Profession Name')
        self.instaceFormat.FormatQTableWidget(self.GenericTable, 2, self.instanceProfession.GetAll(), lstHeaderLabels, 1)

    def LoadPaymentTable(self):
        lstHeaderLabels = ('Concept Name', 'Amount')
        lstPaymentData = [('Monthly Payment',1000),('Enrollment Payment',3000)]

        self.instaceFormat.FormatQTableWidget(self.GenericTable, 2, lstPaymentData, lstHeaderLabels, 1)

    def RetrieveData(self):
        row = self.GenericTable.currentRow()
        if(row >= 0):
            self.result = self.GenericTable.item(row,0).text()
            self.result+= ' ' + self.GenericTable.item(row,1).text()
        return self.result

    def LoadCheckStatus(self):
        
        for row in range(self.GenericTable.rowCount()):
             
            checkbox = QtWidgets.QCheckBox()
            checkbox.setCheckState(False)

            # set the checkbox widget as the cell widget for the first column of the row
            self.GenericTable.setCellWidget(row, 0, checkbox)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = GenericForm()

    app.exec_()