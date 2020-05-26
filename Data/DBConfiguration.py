import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

host = 'localhost'
database = 'bods'
user = 'root'
password = 'Dmun10091992Luda'




def getDbConnection():
    # Get Database connection
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             auth_plugin='mysql_native_password')

        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to database {}".format(error))


def closeDbConnection(connection):
    # Close Database connection
    try:
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to close database connection {}".format(error))


