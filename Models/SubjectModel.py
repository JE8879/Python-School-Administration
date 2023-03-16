from . ServerConnection import Connection
import psycopg2

class SubjectModel(Connection):
    
    def Add(self, parameters):
        try:
            sQuery = "INSERT INTO Subject(SubjectName,SemesterID) VALUES(%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Update(self, parameters):
        try:
            sQuery = "UPDATE Subject Set SubjectName=%s, SemesterID=%s WHERE SubjectID = %s"
            self.ExecuteQuery(sQuery, parameters)
            result = "Record updated succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Delete(self, ID):
        try:
            sQuery = "DELETE FROM Subject WHERE SubjectID=%s"
            self.ExecuteQuery(sQuery,(ID,))
            result = "Record deleted succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def GetAll(self):
        try:
            sQuery = """SELECT Subject.subjectid, Subject.subjectname, Subject.semesterid, Semester.semestername || ' - ' || Profession.ProfessionName as SemesterProfession
                    FROM Subject
                    INNER JOIN Semester ON Semester.SemesterId = Subject.SemesterID
                    INNER JOIN Profession ON Profession.ProfessionID = Semester.ProfessionID;"""
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = err
        return result

# if __name__ == '__main__':
#     objectSubjectMolde = SubjectModel()
#     arrResult = objectSubjectMolde.GetAll()

#     print(arrResult)
