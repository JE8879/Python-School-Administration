from . ServerConnection import Connection
import psycopg2

class ProfessionModel(Connection):

    def GetAll(self):
        try:
            sQuery = "SELECT ProfessionID, ProfessionName FROM Profession"
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = err
        return result


# if __name__ == '__main__':
#     profObject = ProfessionModel()
#     result = profObject.GetAll()
#     print(result)