import os 
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir))
sys.path.append(PROJECT_ROOT)

from Models.SemesterStudentModel import SemesterStudentModel

class ManageSemester:
    # Constrductor
    def __init__(self) -> None:
        super(ManageSemester, self).__init__()

        # Start Instances
        self.objectSemester = SemesterStudentModel()
    
    def AddSemesterStudent(self, arrItems = None):
         # Convert Array to list
        listItems = list(arrItems)

        # Validate items not empty
        for x in range(0,len(listItems)):
            if(len(str(listItems[x])) == 0):
                message = 'Please complete all fields', 'error'
                return message
        
        message = self.objectSemester.Add(listItems)
        return message
    
    def GetSemesterStudent(self):
        return self.objectSemester.GetSemesterStudent()

