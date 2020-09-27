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
    #===========================================================================
    # db = mysql.connect(
    #    host="localhost",
    #    user="wireless",
    #    passwd="fast1",
    #    database="esp8266"
    # )
    #===========================================================================
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

    def register_node(self, name, mac_address, ip_address):
        # perform an SQL insert with a new device
        prior_count = self.cursor.rowcount
        query = "INSERT INTO esp8266_control_device (name, mac_address, last_connected, ip_address, connected, status, led_status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        values = (name, mac_address, now, ip_address, 'true', '001', 'off')
        self.cursor.execute(query, values)
        self.db.commit()
        result_of_insert = self.cursor.rowcount - prior_count
        if result_of_insert:
            return(result_of_insert)
        else:
            return(0)

    def node_lookup_id_by_mac(self, mac_address):
        # perform an SQL request that checks for
        # the existence of a given MAC address
        query = "SELECT id FROM esp8266_control_device WHERE mac_address = %s"
        self.cursor.execute(query, (mac_address,))
        result_of_query = self.cursor.fetchall()
        if result_of_query:
            return(result_of_query)
        else:
            return(0)

    def node_lookup_by_id(self, device_id):
        # perform an SQl query to return the complete
        # record for a device, by ID
        query = "SELECT * FROM esp8266_control_device WHERE id = %s"
        self.cursor.execute(query, (device_id,))
        result_of_query = self.cursor.fetchall()
        if result_of_query:
            return(result_of_query)
        else:
            return(0)

    def fetch_all_nodes(self):
        query = "SELECT * FROM esp8266_control_device"
        self.cursor.execute(query)
        result_of_query = self.cursor.fetchall()
        if result_of_query:
            return(result_of_query)
        else:
            return(0)
