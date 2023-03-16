
from PyQt5.QtCore import QValidator, QRegExp, QRegExpValidator

class Validator:
    def __init__(self) -> None:
        super(Validator, self).__init__()

    def QLineEditValidator(self, QLineEdit):
        self.__regEx = QRegExp("[a-zA-Z]+")
        self.__QLineValidator = QRegExpValidator(self.__regEx,QLineEdit)
        QLineEdit.setValidator(self.__QLineValidator)