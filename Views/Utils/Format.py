from PyQt5 import QtCore
from PyQt5 import QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QStyledItemDelegate, QApplication, QStyleOptionButton, QStyle

class FormatComponents:
    # Constructor
    def __init__(self):
        super(FormatComponents, self).__init__()

        # Load Styles CSS
        with open('./Assets/App.css') as fileCSS:
            self.globalStyles = fileCSS.read()

        # Create Fonts
        self.fontQLabel = QtGui.QFont()
        self.fontQLabel.setFamily("Century Gothic")
        self.fontQLabel.setPointSize(11)
        self.fontQLabel.setBold(True)
        self.fontQLabel.setWeight(75)

        self.fontQLineEdit =  QtGui.QFont()
        self.fontQLineEdit.setFamily("Century Gothic")
        self.fontQLineEdit.setPointSize(10)

        self.styleError = """
            .QLabel#LblMessage {
                color: white;
                font-weight: bold;
                border-radius: 10px;
                background-color: rgb(205, 97, 85);
            }
        """

        self.styleSuccesfull = """
            .QLabel#LblMessage {
                color: black;
                font-weight: bold;
                border-radius: 10px;
                background-color: rgb(46, 204, 113);
            }
        """

    def FormatQTableWidget(self, QTableWidget, numCols, lstData, headerLabels, typeData = None):
       
        numRows = len(lstData)

        QTableWidget.setColumnCount(numCols)
        QTableWidget.setRowCount(numRows)

        QTableWidget.setHorizontalHeaderLabels(headerLabels)
        QTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        QTableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        QTableWidget.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        QTableWidget.setStyleSheet(self.globalStyles)
        
        QTableWidget.horizontalHeader().setStyleSheet(self.globalStyles)
        QTableWidget.horizontalHeader().setFont(self.fontQLabel)
        QTableWidget.verticalHeader().hide()
        QTableWidget.setShowGrid(False)


        if(typeData == 1):
            for row in range(numRows):
                for column in range(numCols):
                    QTableWidget.setItem(row,column,QtWidgets.QTableWidgetItem(str(lstData[row][column])))
                    QTableWidget.item(row,column).setFont(self.fontQLineEdit)
                    QTableWidget.horizontalHeader().setSectionResizeMode(column,QtWidgets.QHeaderView.ResizeToContents)

                    if(row %2 == 0):
                            QTableWidget.item(row,column).setBackground(QtGui.QColor(33, 47, 61))
                    else:
                            QTableWidget.item(row,column).setBackground(QtGui.QColor(44, 62, 80))

        if(typeData == 2):
            for row, item_list in enumerate(lstData):
                for col, key in enumerate(item_list):
                    newItem = QtWidgets.QTableWidgetItem(str(item_list[key]))
                    QTableWidget.setItem(row, col, newItem)
                    QTableWidget.item(row,col).setFont(self.fontQLineEdit)
                    QTableWidget.horizontalHeader().setSectionResizeMode(col,QtWidgets.QHeaderView.ResizeToContents)

    def ShowMessage(self, title, message):
        self.messageBox = QtWidgets.QMessageBox()
        self.messageBox.setIcon(QtWidgets.QMessageBox.Information)
        self.messageBox.setText(message)
        self.messageBox.setWindowTitle(title)
        self.messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.messageBox.show()
    
    def ShowMessageLabel(self, QLabel, message, typeMessage):
        if(typeMessage == 'error'):
            QLabel.show()
            QLabel.setText(message)
            QLabel.setStyleSheet(self.styleError)
            QtCore.QTimer.singleShot(2000, QLabel.hide)

        if(typeMessage == 'successful'):
            QLabel.show()
            QLabel.setText(message)
            QLabel.setStyleSheet(self.styleSuccesfull)
            QtCore.QTimer.singleShot(3000, QLabel.hide)



class Delegate(QStyledItemDelegate):
    #Constructor
    def __init__(self):
        super(Delegate, self).__init__()
        
    def paint(self, painter, option, index):
        if not index.parent().isValid():
            QStyledItemDelegate.paint(self, painter, option, index)
        else:
            widget = option.widget
            style = widget.style() if widget else QApplication.style()
            opt = QStyleOptionButton()
            opt.rect = option.rect
            opt.text = index.data()
            opt.state |= QStyle.State_On if index.data(Qt.CheckStateRole) else QStyle.State_Off
            style.drawControl(QStyle.CE_RadioButton, opt, painter, widget)

    def editorEvent(self, event, model, option, index):
        value = QStyledItemDelegate.editorEvent(self, event, model, option, index)
        if value:
            if event.type() == QEvent.MouseButtonRelease:
                if index.data(Qt.CheckStateRole) == Qt.Checked:
                    parent = index.parent()
                    for i in range(model.rowCount(parent)):
                        if i != index.row():
                            ix = parent.child(i, 0)
                            model.setData(ix, Qt.Unchecked, Qt.CheckStateRole)
        return value
    