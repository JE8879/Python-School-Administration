from . ServerConnection import Connection
import psycopg2

class SemesterStudentModel(Connection):
    # Methods
    def Add(self, parameters):
        try:
            sQuery = "INSERT INTO SemesterStudent(userid,semesterid) VALUES(%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Update(self, parameters):
        try:
            sQuery = "UPDATE SemesterStudent SET semesterid=%s WHERE semsstudid=%s"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record updated succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
            return
        return result
    
    def Delete(self, ID):
        try:
            sQuery = "DELETE FROM SemesterStudent WHERE semsstudid=%s"
            self.ExecuteQuery(sQuery,(ID,))
            result = "Record deleted succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def GetSemesterStudent(self):
        try:
            sQuery = """SELECT SemsStudId, Userdata.FirstName || ' ' || UserData.LastName as FullName, 
                        Semester.SemesterId || ' - ' || Semester.SemesterName || ' - ' || Profession.ProfessionName as Semester
                        FROM SemesterStudent
                        INNER JOIN UserData ON SemesterStudent.UserId = UserData.UserId
                        INNER JOIN Semester ON SemesterStudent.SemesterId = Semester.SemesterId
                        INNER JOIN Profession ON Semester.ProfessionId = Profession.ProfessionId;"""
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def SearchLikeSemesterStudent(self, key, value):
        keys = ['ID', 'fullname', 'semester']
        lstValues = self.GetSemesterStudent()

        dictionaryList = []
        for item in lstValues:
            newDictionary = dict(zip(keys, item))
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

#     objectSemesterStudentModel = SemesterStudentModel()
#     result = objectSemesterStudentModel.SearchLikeSemesterStudent('fullname','John B. Erdman')
#     print(result[0])
