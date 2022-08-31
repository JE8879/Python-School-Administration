from . ServerConnection import Connection
from PyQt5.QtCore import QDate
import psycopg2

class SemesterModel(Connection):

    def Add(self, parameters):
        try:
            sQuery = "INSERT INTO Semester(semestername,schoolyear,timestart,timeend,professionid) VALUES(%s,%s,%s,%s,%s)"
            self.ExecuteQuery(sQuery,parameters)
            result = "Record inserted successfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def Update(self, parameters):
        try:
            sQuery = "UPDATE Semester SET semestername=%s, schoolyear=%s, timestart=%s, timeend=%s, professionid=% WHERE semesterid=%s"
            self.ExecuteReader(sQuery, parameters)
            result = "Record updated succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result
    
    def Delete(self, ID):
        try:
            sQuery = "DELETE FROM Semester WHERE semesterid=%s"
            self.ExecuteQuery(sQuery,(ID,))
            result = "Record deleted succesfully"
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def GetAll(self):
        try:
            sQuery = """
            SELECT  semesterid, semestername, schoolyear, timestart, timeend, profession.professionid || ' - ' || profession.professionname AS Profession
            FROM Semester
            INNER JOIN Profession ON Profession.professionid = semester.professionid;
            """
            result = self.ExecuteReader(sQuery)
        except(Exception, psycopg2.Error) as err:
            result = str(err)
        return result

    def GetMonths(self, dateOne, dateTwo):
        monthsPassed = (dateTwo.year() - dateOne.year()) * 12 + (dateTwo.month() - dateOne.month())
        return monthsPassed

    def GetFormattedData(self):
        inputData = self.GetAll()
        outputData = []

        for item in inputData:
            dateOne = QDate.currentDate()
            dateTwo = QDate(item[4])

            monthsRemaining = self.GetMonths(dateOne, dateTwo)
            if(monthsRemaining >= 1):
                lstElement = list(item)
                lstElement.insert(5,monthsRemaining)
                outputData.append(tuple(lstElement))
        return outputData

    def SearchLike(self, key, value):
        keys = ['ID', 'Name', 'Year', 'Time Start', 'Time End', 'Remaining', 'ProfID']
        lstValues = self.GetFormattedData()
        dictionaryList = []

        for item in lstValues:
            newDictionary = dict(zip(keys, item))
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
#     instanceSemester = SemesterModel()
#     result = instanceSemester.GetFormattedData()
#     print(result)

