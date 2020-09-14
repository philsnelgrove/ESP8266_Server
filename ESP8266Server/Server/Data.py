'''
Created on Sep. 14, 2020

@author: Phil
'''
import mysql.connector as mysql


class DataSource(object):
    '''
    classdocs
    '''
    db = mysql.connect(
        host="localhost",
        user="phil",
        passwd="manchu"
    )
    cursor = db.cursor()

    def __init__(self):
        '''
        Constructor
        '''
        self.cursor.execute("SHOW DATABASES")
        databases = self.cursor.fetchall()
        print(databases)
