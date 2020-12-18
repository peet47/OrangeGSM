import sqlite3
from sqlite3 import Error

class db_ops(object):

    def create_connection(db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def create_entry(conn, sms):
        """
        Create a new entry into the sms's table
        :param conn:
        :param sms:
        :return: 
        """
        sql = ''' INSERT INTO sms(tele_number,received_date,received_time,message)
                VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, sms)
        conn.commit()
        return
    
    def read_entries(conn):
        cur = conn.cursor()
        query_string = "SELECT * FROM sms ORDER BY id DESC"
        cur.execute(query_string)
        data = cur.fetchall()
        return data

    def create_db_schema(conn):
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS sms (
                                            id integer PRIMARY KEY,
                                            tele_number text NOT NULL,
                                            received_date text,
                                            received_time text,
                                            message text
                                        ); """
        try:
            c = conn.cursor()
            c.execute(sql_create_projects_table)
            print("DB created")
        except Error as e:
            print(e)
