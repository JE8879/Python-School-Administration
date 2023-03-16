import os
import sys
from . Utils.Format import Delegate
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.Qt import Qt


PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir))
sys.path.append(PROJECT_ROOT)

class ViewFilter(QtWidgets.QWidget):
    #Constructor
    def __init__(self, dicParameters):
        # Find components and set properties
        self.dicParameters = dicParameters
        super(ViewFilter, self).__init__()

        #Load UI-File
        uic.loadUi('Views/Templates/FrmFilter.ui',self)
        self.setMaximumSize(QtCore.QSize(400,300))
        self.setMinimumSize(QtCore.QSize(400,300))
        self.setStyleSheet('background-color: rgb(46, 64, 83);')

        #Load Styles CSS
        with open('./Assets/App.css') as fileCSS:
            self.globalStyles = fileCSS.read()
      
        #-------------Search treeview
        self.treeWidgetParent = self.findChild(QtWidgets.QTreeWidget, 'treeWidget')
        self.treeWidgetParent.setItemDelegate(Delegate())
        # self.treeWidgetParent.itemSelectionChanged.connect(self.LoadEvents)
        self.treeWidgetParent.setStyleSheet(self.globalStyles)

        #-------------Search buttons
        self.BtnAcept = self.findChild(QtWidgets.QPushButton, 'BtnAcept')
        self.BtnAcept.setStyleSheet(self.globalStyles)
        # self.BtnAcept.clicked.connect(self.LoadEvents)

        self.BtnCancel = self.findChild(QtWidgets.QPushButton, 'BtnCancel')
        self.BtnCancel.clicked.connect(self.close)
        self.BtnCancel.setStyleSheet(self.globalStyles)

        self.groupBox = self.findChild(QtWidgets.QGroupBox, 'groupBox')
        self.groupBox.setStyleSheet(self.globalStyles)

        # Create new Dictionary
        self.dictHeaderUser = {'fname':'First Name', 'lname':'Last Name','positionId':'Position'}

        self.LoadTreeWidget()

        self.show()
    
    def LoadTreeWidget(self):
        
        self.columnParen = QtWidgets.QTreeWidgetItem(self.treeWidgetParent)
        self.columnParen.setText(0,"Select")

        for key, value in self.dicParameters.items():
            childItem = QtWidgets.QTreeWidgetItem(self.columnParen)
            childItem.setFlags(childItem.flags() | Qt.ItemIsUserCheckable)
            childItem.setText(0, value)
            childItem.setCheckState(0, Qt.Unchecked)

    def RetrieveSelectedChoices(self):
        for item in range(self.columnParen.childCount()):
            if(self.columnParen.child(item).checkState(0)):
                # Get the element text
                textElement = self.columnParen.child(item).text(0)
                # Search value and get key
                for key, value in self.dicParameters.items():
                    if(value == textElement):
                        result = key
        return result


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = ViewFilter()

    app.exec_()