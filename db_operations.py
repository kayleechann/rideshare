import sqlite3
import datetime

class db_operations():

    #constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

    #creates table rider in our database
    def create_rider_table(self):
        query = '''
        CREATE TABLE rider(
            riderID INT NOT NULL PRIMARY KEY,
            fullName VARCHAR(40),
            creationDate DATE
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print('Rider Table Created')
        
    #creates table driver in our database
    def create_driver_table(self):
        query = '''
        CREATE TABLE driver(
            driverID INT NOT NULL PRIMARY KEY,
            fullName VARCHAR(40),
            rating DECIMAL,
            driverMode VARCHAR(20),
            licensePlate VARCHAR(7)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print('Driver Table Created')
        
    #creates table rides in our database
    def create_rides_table(self):
        query = '''
        CREATE TABLE rides(
            rideID INT NOT NULL PRIMARY KEY,
            pickupLocation VARCHAR(40),
            dropoffLocation VARCHAR(40),
            dateAndTime DATETIME,
            FOREIGN KEY (riderID) REFERENCES rider(riderID),
            FOREIGN KEY (driverID) REFERENCES driver(driverID)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print('Rides Table Created')

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