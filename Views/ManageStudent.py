import os 
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir))
sys.path.append(PROJECT_ROOT)

from Models.StudentModel import StudentModel

class ManageStudent:
    # Constructor
    def __init__(self) -> None:
        super(ManageStudent, self).__init__()

        # Start the instances
        self.objectStudent = StudentModel()

    def AddStudent(self,  arrItems = None):
        # Convert Array to list
        listItems = list(arrItems)

        # Validate items not empty
        for x in range(0,len(listItems)):
            if(len(str(listItems[x])) == 0):
                message = 'Please complete all fields', 'error'
                return message

        message = self.objectStudent.Add(listItems)
        return message
    
    def GetAll(self):
        return self.objectStudent.GetAll()