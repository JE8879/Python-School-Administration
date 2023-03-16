from . ServerConnection import Connection
import psycopg2

class UserModel(Connection):

    def Add(self,parameters):
        try:
            sQuery = "INSERT INTO UserData (firstname,lastname,address,gender,email,phone,birthday,positionid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"
        except (Exception, psycopg2.Error) as err:
            result = str(err)        
        return result

    def Update(self,parameters):
        try:
            sQuery = "UPDATE UserData SET firstname=%s, lastname=%s, address=%s, gender=%s, email=%s, phone=%s, birthday=%s, positionid=%s WHERE UserID=%s"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record updated succesfully"
        except (Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Delete(self,ID):
        try:
            sQuery = "DELETE FROM UserData WHERE UserID=%s"
            self.ExecuteQuery(sQuery,(ID,))
            result = "Record deleted succesfully"
        except (Exception, psycopg2.Error) as err:
            result = err
        return result

    def GetAll(self):
        try:           
            sQuery = "SELECT * FROM UserData ORDER BY userid ASC"
            result = self.ExecuteReader(sQuery)
        except (Exception, psycopg2.Error) as err:
            result = err
        return result

    def SearchLike(self, key, value):
        keys = ['ID', 'fname', 'lname', 'address', 'gender', 'email', 'phone', 'birthday', 'positionid']
        lstValues = []
        dictionaryList = []
        auxiliaryList = []

        if(len(lstValues)) > 0:
            print('Desde los valores')
            # Crea una lista de diccionarios
            dictionaryList = [dict(zip(keys, item)) for item in lstValues]

            try:
                auxiliaryList = [element for element in dictionaryList if element[key] == value]
            except:
                return
            return auxiliaryList
        else:
            lstValues = self.GetAll()
            print('Desde la Base de Datos')
            # Crea una lista de diccionarios
            dictionaryList = [dict(zip(keys, item)) for item in lstValues]

            try:
                auxiliaryList = [element for element in dictionaryList if element[key] == value]
            except:
                return
            return auxiliaryList
            


    def CustomSearch(self, key, value, update=None):
        keys = ['ID', 'fname', 'lname', 'address', 'gender', 'email', 'phone', 'birthday', 'positionid']

        lstValues = []

        if(lstValues):
            print(lstValues)
        else:
            lstValues = self.GetAll()


# if __name__ == '__main__':
#     testQuery = UserModel()
#     result = testQuery.SearchLike('ID',1)
#     for item in result:
#         print(item)
