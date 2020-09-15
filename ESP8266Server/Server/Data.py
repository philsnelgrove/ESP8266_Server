'''
Created on Sep. 14, 2020

@author: Phil
'''
import mysql.connector as mysql
import time


class DataSource(object):
    '''
    classdocs
    '''
    db = mysql.connect(
        host="localhost",
        user="phil",
        passwd="manchu",
        database="esp8266"
    )
    cursor = db.cursor()

    def __init__(self):
        '''
        Constructor
        '''
        self.cursor.execute("SHOW DATABASES")
        databases = self.cursor.fetchall()
        print(databases)

    def register_node(self, name, mac_address):
        # perform an SQL insert with a new device
        prior_count = self.cursor.rowcount
        query = "INSERT INTO device (name, mac_address, last_connection) VALUES (%s, %s, %s)"
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        values = (name, mac_address, now)
        self.cursor.execute(query, values)
        self.db.commit()
        result_of_insert = self.cursor.rowcount - prior_count
        if result_of_insert:
            return(result_of_insert)
        else:
            return(-1)

    def node_lookup_id_by_mac(self, mac_address):
        # perform an SQL request that checks for
        # the existence of a given MAC address
        query = "SELECT id FROM device WHERE mac_address = '%s'"
        value = mac_address
        self.cursor.execute(query, value)
        result_of_query = self.cursor.fetchall()
        if result_of_query:
            return(result_of_query)
        else:
            return(-1)

    def node_lookup_by_id(self, device_id):
        # perform an SQl query to return the complete
        # record for a device, by ID
        query = "SELECT * FROM device WHERE id = %s"
        value = device_id
        self.cursor.execute(query, value)
        result_of_query = self.cursor.fetchall()
        if result_of_query:
            return(result_of_query)
        else:
            return(-1)

    def fetch_all_nodes(self):
        query = "SELECT * FROM `device`"
        self.cursor.execute(query)
        result_of_query = self.cursor.fetchall()
        if result_of_query:
            return(result_of_query)
        else:
            return(-1)
