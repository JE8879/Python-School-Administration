from . ServerConnection import Connection
import psycopg2

class StudentModel(Connection):

    def Add(self,parameters):
        try:
            sQuery = "INSERT INTO Student(userid,semesterid,studyshift,active) VALUES(%s,%s,%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"        
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Update(self,parameters):
        try:
            sQuery = "UPDATE Student SET semesterid=%s, studyshift=%s, active=%s WHERE studentid=%s"
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
            result = str(result)
        return result

    def GetAll(self):
        try:
            sQuery = """SELECT StudentID, FirstName || ' ' || LastName  as FullName, Semester.SemesterID || ' - ' ||  SemesterName || ' - ' || ProfessionName  AS SemesterProfession, StudyShift, Active
            FROM Student
            INNER JOIN UserData ON Student.UserID = UserData.UserID
            INNER JOIN Semester ON Student.SemesterId = Semester.SemesterID
            INNER JOIN Profession ON Semester.ProfessionID = Profession.ProfessionID
            WHERE Active='Active'
            ORDER BY StudentID ASC;
            """
            
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result
    
    def GetStudents(self):
        try:
            sQuery = "SELECT UserID, Firstname || ' ' || LastName AS FullName From UserData WHERE PositionID = 3;"
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result
    
    def GetSemesters(self):
        try:
            sQuery = """SELECT SemesterID, SemesterName || ' - ' || ProfessionName AS Semester, SchoolYear
                        FROM Semester
                        INNER JOIN Profession ON Semester.ProfessionID = Profession.ProfessionID
                        WHERE SchoolYear = DATE_PART('YEAR',CURRENT_DATE);
                    """
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def GetOnlyOneStuent(self, key, value):
        lstValues = self.GetStudents()

        dictionaryList = []
        for item in lstValues:
            newDictionary = {'ID':str(item[0]), 'fullname':item[1]}
            # Add the dictionary to the list
            dictionaryList.append(newDictionary)
        # Create new list auxiliar
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
#     message = objectStudent.GetOnlyOneStuent('ID','1')
#     print(message)
