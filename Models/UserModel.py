from . ServerConnection import Connection
import psycopg2

class UserModel(Connection):

    def Add(self,parameters):
        try:
            sQuery = "INSERT INTO UserData (firstname,lastname,gender,age,phone,email,positionid) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"
        except (Exception, psycopg2.Error) as err:
            result = str(err)        
        return result

    def Update(self,parameters):
        try:
            sQuery = "UPDATE UserData SET firstname=%s, lastname=%s, gender=%s, age=%s, phone=%s, email=%s, positionid=%s WHERE UserID=%s"
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

    def GetBasicInfoUser(self):
        try:           
            sQuery = "SELECT * FROM UserData ORDER BY userid ASC"
            result = self.ExecuteReader(sQuery)
        except (Exception, psycopg2.Error) as err:
            result = err
        return result

    def GetCustomData(self, key, value):
        lstValues = self.GetBasicInfoUser()

        dictionaryList = []
        for item in lstValues:
            # Create new Dictionary
            newDictionary = {'ID':str(item[0]),'fname':item[1],
                    'lname':item[2],'gender':item[3],
                    'age':item[4],'phone':item[5],
                    'email':item[6], 'positionId':str(item[7])}
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
#     testQuery = UserModel()
#     result = testQuery.GetCustomData('ID','1')
#     for item in result:
#         print(item)
