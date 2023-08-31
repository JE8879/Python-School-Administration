from . ServerConnection import Connection
import psycopg2
# from PyQt5 import QtCore
# import uuid


class PaymentModel(Connection):

    def Add(self, parameters):
        try:
            sQuery = "INSERT INTO Payment(UserID,folionumber,paymentconcept,paymentdate,amount) VALUES(%s,%s,%s,%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Delete(self, ID):
        pass

    def GetAll(self):
        try:
            sQuery = "SELECT * FROM Payment"
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result


# if __name__ == '__main__':

#     objectPayment = PaymentModel()
#     currentDate = QtCore.QDate.currentDate().toString('yyyy-MM-dd')
#     objectList = [1,str(uuid.uuid4()),'Enrollment Payment',currentDate,1000]

#     dataSet = objectPayment.GetAll()
#     print(type(dataSet))
#     print(dataSet)
    