import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Views.FrmUser import ManageUser
from Views.FrmStudent import ViewStudent
from Views.FrmSemester import ViewSemester
from Views.FrmProfession import ViewProfession
from Views.FrmPayment import ViewPayment

class MainForm(QtWidgets.QWidget):
    # Constructor
    def __init__(self):
        # Find components and assign properties
        super(MainForm, self).__init__()

        # Load Template-UI-File
        uic.loadUi('Views/Templates/MainForm.ui',self)
        self.setStyleSheet("background-color: rgb(46, 64, 83);")
        # self.setStyleSheet("background-color: white;")

        # Load Styles CSS
        with open('./Assets/MainFormStyles.css') as fileCss:
            self.mainFormStyles = fileCss.read()
            
        self.CenterWindow()

        self.menuLateral = self.findChild(QtWidgets.QFrame, 'menuLateral')
        self.menuLateral.setStyleSheet(self.mainFormStyles)

        self.BtnMenu = self.findChild(QtWidgets.QPushButton, 'BtnMenu')
        self.BtnMenu.clicked.connect(self.OpenAdminSubMenu)
        self.BtnMenu.setToolTip('Menu')

        self.isShow = True

        self.BtnProfessor = self.findChild(QtWidgets.QPushButton, 'BtnProfessor')
        self.BtnProfessor.setStyleSheet(self.mainFormStyles)
        self.BtnProfessor.clicked.connect(self.OpenProfessorSubMenu)

        self.panelAdmin = self.findChild(QtWidgets.QFrame, 'adminSubMenu')
        self.panelProfessor = self.findChild(QtWidgets.QFrame, 'panelProfessor')

        self.BtnUser = self.findChild(QtWidgets.QPushButton, 'BtnUserLogs')
        self.BtnUser.clicked.connect(self.OpenMageUser)
        self.BtnUser.setToolTip('Edit Users')
        
        self.BtnStudent = self.findChild(QtWidgets.QPushButton, 'BtnStudents')
        self.BtnStudent.clicked.connect(self.OpenStudent)
        self.BtnStudent.setToolTip('Edit Students and Semester Students')

        self.BtnSemesters = self.findChild(QtWidgets.QPushButton, 'BtnSemesters')
        self.BtnSemesters.clicked.connect(self.OpenSemester)
        self.BtnSemesters.setToolTip('Edit Semesters')

        self.BtnProfession = self.findChild(QtWidgets.QPushButton, 'BtnProfessions')
        self.BtnProfession.clicked.connect(self.OpenProfessionSubject)
        self.BtnProfession.setToolTip('Edit Professions')

        self.BtnPay = self.findChild(QtWidgets.QPushButton, 'BtnPayMents')
        self.BtnPay.clicked.connect(self.OpenPayment)
        self.BtnPay.setToolTip('Register PayMents')

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
        self.BtnProfessor.setGeometry(QtCore.QRect(0, 140, 64, 50))

    def OpenAdminSubMenu(self):
        if(self.panelAdmin.isVisible() == False):
            self.panelAdmin.show()
            self.panelProfessor.hide()
            self.BtnProfessor.setGeometry(QtCore.QRect(0, 390, 64, 50))            
        else:
            self.mdiArea.closeAllSubWindows()
            self.panelAdmin.hide()
            self.BtnProfessor.setGeometry(QtCore.QRect(0, 140, 64, 50))
         
    def OpenProfessorSubMenu(self):
        if(self.panelProfessor.isVisible() == False):
            self.panelProfessor.show()
            self.panelAdmin.hide()
            self.mdiArea.closeAllSubWindows()
            self.BtnProfessor.setGeometry(QtCore.QRect(0, 140, 64, 50))
            self.panelProfessor.setGeometry(QtCore.QRect(0, 190, 241, 155))                                  
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

    def OpenProfessionSubject(self):
        self.instanceProfession = ViewProfession()
        self.frmProfessionSubWindow = QtWidgets.QMdiSubWindow()
        self.OpenChildForm(self.instanceProfession, self.frmProfessionSubWindow)
        
    def OpenPayment(self):
        self.instancePaymeent = ViewPayment()
        self.frmPaymentSubWindow = QtWidgets.QMdiSubWindow()
        self.OpenChildForm(self.instancePaymeent, self.frmPaymentSubWindow)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = MainForm()

    app.exec_()
