from . ServerConnection import Connection
import psycopg2

class PostionModel(Connection):

    def GetPositions(self):
        try:
            sQuery = "SELECT * FROM UserPosition"
            result = self.ExecuteReader(sQuery)
        except (Exception, psycopg2.Error) as err:
            result = err
        return result



# if __name__ == '__main__':
#     objectQuery = PostionModel()
#     arrObject = objectQuery.GetPositions()
#     print(arrObject)