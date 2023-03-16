from . ServerConnection import Connection
import psycopg2

class ProfessionModel(Connection):

    def Add(self, parameters):
        try:
            sQuery = "INSERT INTO Profession(professionName,professionDescription,active) VALUES (%s, %s, %s)"
            self.ExecuteQuery(sQuery, parameters)
            result = "Record inserted successfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Update(self, parameters):
        try:
            sQuery = "UPDATE Profession SET professionName=%s, professiondescription=%s, active=%s WHERE ProfessionID = %s"
            self.ExecuteQuery(sQuery, parameters)
            result = "Record updated succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Delete(self, ID):
        try:
            sQuery = "DELETE FROM Profession WHERE ProfessionID = %s"
            self.ExecuteQuery(sQuery,(ID,))
            result = "Record deleted succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def GetAll(self):
        try:
            sQuery = "SELECT * FROM Profession"
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = err
        return result


# if __name__ == '__main__':
#     profObject = ProfessionModel()
#     result = profObject.GetAll()
#     print(result)