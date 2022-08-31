import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Views.FrmUser import ManageUser
from Views.FrmStudent import ViewStudent
from Views.FrmSemester import ViewSemester

class MainForm(QtWidgets.QWidget):
    # Constructor
    def __init__(self):
        # Find components and assign properties
        super(MainForm, self).__init__()

        # Load Template-UI-File
        uic.loadUi('Views/Templates/MainForm.ui',self)
        # self.setStyleSheet("background-color: white;")

        # Load Styles CSS
        with open('./Assets/MainFormStyles.css') as fileCss:
            self.mainFormStyles = fileCss.read()

        self.CenterWindow()

        self.menuPanel = self.findChild(QtWidgets.QFrame, 'MenuPanel')
        self.menuPanel.setStyleSheet(self.mainFormStyles)

        # ToolButtons
        self.BtnProfile = self.findChild(QtWidgets.QToolButton, 'BtnProfile')
        self.BtnProfile.setStyleSheet(self.mainFormStyles)

        # Buttons
        self.BtnAdministration = self.findChild(QtWidgets.QPushButton, 'BtnAdmin')
        self.BtnAdministration.setStyleSheet(self.mainFormStyles)
        self.BtnAdministration.clicked.connect(self.OpenAdminSubMenu)

        self.BtnProfessor = self.findChild(QtWidgets.QPushButton, 'BtnProfessor')
        self.BtnProfessor.setStyleSheet(self.mainFormStyles)
        self.BtnProfessor.clicked.connect(self.OpenProfessorSubMenu)

        self.panelAdmin = self.findChild(QtWidgets.QFrame, 'adminSubMenu')
        self.panelProfessor = self.findChild(QtWidgets.QFrame, 'panelProfessor')

        self.BtnUser = self.findChild(QtWidgets.QPushButton, 'BtnUserLogs')
        self.BtnUser.clicked.connect(self.OpenMageUser)
        
        self.BtnStudent = self.findChild(QtWidgets.QPushButton, 'BtnStudents')
        self.BtnStudent.clicked.connect(self.OpenStudent)

        self.BtnSubject = self.findChild(QtWidgets.QPushButton, 'BtnSubjects')
        self.BtnSubject.clicked.connect(self.OpenSemester)

        self.Profession = self.findChild(QtWidgets.QPushButton, 'BtnProfessions')

        self.BtnPay = self.findChild(QtWidgets.QPushButton, 'BtnPayMents')

        self.mdiArea = self.findChild(QtWidgets.QMdiArea, 'mdiArea')

        self.CustomDesign(self.panelAdmin)
        self.CustomDesign(self.panelProfessor)

        self.show()

    def OpenChildForm(self, objectInstance, mdiSubWindow):
        self.mdiArea.closeAllSubWindows()

        if(mdiSubWindow not in self.mdiArea.subWindowList()):
            instace = objectInstance
            mdiSubWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            mdiSubWindow.setWidget(instace)
            mdiSubWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.mdiArea.addSubWindow(mdiSubWindow)
            mdiSubWindow.showMaximized()

    def CenterWindow(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def CustomDesign(self,panelSubMenu):
        panelSubMenu.hide()
        self.BtnProfessor.setGeometry(QtCore.QRect(0, 200, 231, 31))

    def OpenAdminSubMenu(self):
        if(self.panelAdmin.isVisible() == False):
            self.panelAdmin.show()
            self.panelProfessor.hide()
            self.BtnProfessor.setGeometry(QtCore.QRect(0, 390, 231, 31))            
        else:
            self.panelAdmin.hide()
            self.BtnProfessor.setGeometry(QtCore.QRect(0, 200, 231, 31))
         
    def OpenProfessorSubMenu(self):
        if(self.panelProfessor.isVisible() == False):
            self.panelProfessor.show()
            self.panelAdmin.hide()  
            self.BtnProfessor.setGeometry(QtCore.QRect(0, 200, 231, 31))
            self.panelProfessor.setGeometry(QtCore.QRect(-10, 240, 241, 121))                                  
        else:
            self.panelProfessor.hide()

    def OpenMageUser(self):
        self.instanceMageUser = ManageUser()        
        self.frmManageUserSubWindow = QtWidgets.QMdiSubWindow()
        self.OpenChildForm(self.instanceMageUser,self.frmManageUserSubWindow)

    def OpenStudent(self):
        self.instaceStudent = ViewStudent()
        self.frmStudentSubWindow = QtWidgets.QMdiSubWindow()
        self.OpenChildForm(self.instaceStudent, self.frmStudentSubWindow)
    
    def OpenSemester(self):
        self.instanceSemester = ViewSemester()
        self.frmSemesterSubWindow = QtWidgets.QMdiSubWindow()
        self.OpenChildForm(self.instanceSemester, self.frmSemesterSubWindow)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = MainForm()

    app.exec_()
