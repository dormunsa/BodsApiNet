import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from Data.DBConfiguration import *


def readCameraById(cameraId):

    try:

        connection = getDbConnection()
        cursor = connection.cursor()
        sql_select_query = """select * from camera where CameraId = %s"""
        cursor.execute(sql_select_query, (cameraId,))
        records = cursor.fetchall()
        # Close db connection
        closeDbConnection(connection)

        if(len(records) > 0):
            return records
        return None

    except mysql.connector.Error as error:
        print("Failed to read hospital table {}".format(error))


def insertCamera(camera):
    try:
        connection = getDbConnection()
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO camera (LocationName, Longitude, Latitude, IsWorking,DateAdded) 
                                   VALUES (%s, %s, %s, %s , %s) """

        recordTuple = ( camera.LocationName,  camera.Longitude, camera.Latitude , camera.IsWorking , camera.DateAdded)
        cursor.execute(mySql_insert_query, recordTuple)
        connection.commit()
        if(cursor.rowcount > 0):
            return True
        return False


    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            closeDbConnection(connection)
            print("MySQL connection is closed")
