from . ServerConnection import Connection
import psycopg2

class SectionModel(Connection):

    def Add(self, parameters):
        try:
            sQuery = "INSERT INTO SchoolSection(SectionName,SemesterID) VALUES(%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result
    
    def Update(self, parameters):
        try:
            sQuery = "UPDATE SchoolSection SET SectionName=%s, SemesterID=%s WHERE SectionID=%s"
            self.ExecuteQuery(sQuery, parameters)
            result = "Record updated succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result
    
    def Delete(self, ID):
        try:
            sQuery = "DELETE FROM SchoolSection WHERE SectionID=%s"
            self.ExecuteQuery(sQuery,(ID,))
            result = "Record deleted succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result
    
    def GetAll(self):
        try:
            sQuery = """
            SELECT SchoolSection.SectionID, SchoolSection.SectionName, SchoolSection.SemesterID || ' - ' || Semester.SemesterName as SemesterSection,
            Profession.ProfessionName
            FROM SchoolSection
            INNER JOIN Semester ON Semester.SemesterID = SchoolSection.SemesterID
            INNER JOIN Profession ON profession.professionid = Semester.ProfessionID;
            """
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result