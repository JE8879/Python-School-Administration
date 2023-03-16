from . ServerConnection import Connection
import psycopg2

class StudentModel(Connection):

    def Add(self,parameters):
        try:
            sQuery = "INSERT INTO Student(userid,schoolenrollment,studyshift,active) VALUES(%s,%s,%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"        
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Update(self,parameters):
        try:
            sQuery = "UPDATE Student SET studyshift=%s, active=%s WHERE userid=%s"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record updated succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Delete(self, ID):
        try:
            sQuery = "DELETE FROM Student WHERE studentid=%s"
            self.ExecuteQuery(sQuery,(ID,))
            result = "Record deleted succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def GetAll(self):
        try:
            sQuery = """SELECT Student.userid, UserData.firstname || ' ' || UserData.lastname as FullName, Student.Schoolenrollment, Student.studyshift, Student.active
                        FROM Student
                        INNER JOIN UserData ON Userdata.userid = Student.userid
                        WHERE Student.Active = 'Active'
                        ORDER BY Student.userid;"""    
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result
    
    def GetStudents(self):
        try:
            sQuery = """
                SELECT UserData.UserID, UserData.Firstname || ' ' || UserData.LastName as FullName
                FROM UserData
                LEFT JOIN Student ON Student.UserId = Userdata.UserId
                WHERE Student.UserId IS NULL AND UserData.PositionId=2;
                """
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result
    
    def GetSemesters(self):
        try:
            sQuery = """SELECT SemesterID, SemesterName || ' - ' || ProfessionName AS Semester, SchoolYear
                        FROM Semester
                        INNER JOIN Profession ON Semester.ProfessionID = Profession.ProfessionID;
                    """
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def SearchLikeStudent(self, key, value):
        # crate keys, the field null is the enrollment but i don´t use that field then i ignore
        # The field null is not inside of list of parameters to search
        keys = ['ID','fullname','null','studyShift','active']
        lstValues = self.GetAll()

        dictionaryList = []

        for item in lstValues:
            newDictionary = dict(zip(keys,item))
            dictionaryList.append(newDictionary)

        auxiliaryList = []
        try:
            for element in dictionaryList:
                if(element[key] == value):
                    auxiliaryList.append(element)
        except:
            return
        return auxiliaryList

# if __name__ == '__main__':
#     objectStudent = StudentModel()
#     result = objectStudent.GetSemesters()
#     print(result)

    
