import sqlite3
import datetime

class db_operations():

    #constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

    #creates table songs in our database
    def create_songs_table(self):
        query = '''
        CREATE TABLE songs(
            songID VARCHAR(22) NOT NULL PRIMARY KEY,
            Name VARCHAR(20),
            Artist VARCHAR(20),
            Album VARCHAR(20),
            releaseDate DATETIME,
            Genre VARCHAR(20),
            Explicit BOOLEAN,
            Duration DOUBLE,
            Energy DOUBLE,
            Danceability DOUBLE,
            Acousticness DOUBLE,
            Liveness DOUBLE,
            Loudness DOUBLE
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print('Table Created')

    # function to return a single value from table
    def single_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function for bulk inserting records
    def bulk_insert(self,query,records):
        self.cursor.executemany(query,records)
        self.connection.commit()
        print("query executed..")

    # function to return a single attribute values from table
    def single_attribute(self,query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        #results.remove(None)
        return results

    # SELECT with named placeholders
    def name_placeholder_query(self,query,dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    #destructor that closes connection with DB
    def destructor(self):
        self.connection.close()