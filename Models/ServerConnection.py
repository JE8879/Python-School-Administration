from sqlite3 import Cursor
import psycopg2

class Connection:

    def ExecuteQuery(self,sQuery,param=[]):
        connection = psycopg2.connect(database='SchoolDatabase', 
                                    user='postgres',
                                    password='hacker122')
    
        cursor = connection.cursor()
        with connection:
            cursor = connection.cursor()
            cursor.execute(sQuery,(param))

    def ExecuteReader(self,sQuery,param=[]):
        connection = psycopg2.connect(database='SchoolDatabase', 
                                    user='postgres',
                                    password='hacker122')
        
        cursor = connection.cursor()
        with connection:
            cursor = connection.cursor()
            cursor.execute(sQuery,(param))
            result = cursor.fetchall()
            return result
   