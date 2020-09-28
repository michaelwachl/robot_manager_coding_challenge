import sqlite3
from sqlite3 import Error

"""
Data: 27.09.2020  
Author: Michael Wachl  
Contact:  wachlm@web.de  
Project: Fleet Manager Coding Challenge
"""


class FleetDatabase(object):
    """A simple class for SQLite manipulation
    """
    def __init__(self):
        self.db_name = 'Fleet_SQLite_Database.db'
        self.table_sql = "CREATE TABLE robot_fleet(x integer, y integer, vehicle_id text, " \
                         "driving integer, battery real, abort integer, order_id null)"
    def get_db_name(self):
        return self.db_name

    def set_db_name(self, name):
        self.db_name = name

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: Connection object
        :return: Connection object or None
        """
        self.db_name = db_file
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self, conn, table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param table_sql: a CREATE TABLE statement
        """
        try:
            cursor_obj = conn.cursor()
            cursor_obj.execute(table_sql)
        except Error as e:
            print("Create table: ", e)

    def insert_to_table(self, entities):
        """ adds a line to database
        :param entities: line to add
        """
        try:
            with sqlite3.connect(self.db_name) as con:
                cursor_obj = con.cursor()
                cursor_obj.execute('INSERT INTO robot_fleet(x, y, vehicle_id, driving, battery, abort, order_id) '
                                   'VALUES(?, ?, ?, ?, ?, ?, ?)', entities)
                con.commit()
                print("Elements inserted to ", self.db_name)
        except Error as e:
            print("Error Insert : ", e)


    def fetch_sql(self, conn):
        """ fetches all entities from the database
        :param conn: Connection object
        :return all rows or None
        """
        db_entities = None
        try:
            cursor_obj = conn.cursor()
            cursor_obj.execute('SELECT * FROM robot_fleet')
            db_entities = cursor_obj.fetchall()
            return db_entities
        except Error as e:
            print("Error Fetch table: ", e)
        return db_entities

    def fetch_columns(self, conn):
        """ fetches all columns from the database
        :param conn: Connection object
        :return all columns or None
        """
        db_entities = None
        try:
            cursor_obj = conn.cursor()
            cursor_obj.execute('SELECT x,y,vehicle_id,driving,battery,abort,order_id FROM robot_fleet')
            db_entities = cursor_obj.fetchall()
            return db_entities
        except Error as e:
            print("Error Fetch table: ", e)
        return db_entities
