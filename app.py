from helper import helper
from db_operations import db_operations
from datetime import date

# import MySQL
import mysql.connector

# Make connection
conn = mysql.connector.connect(host="localhost",
    user = "root",
    password = "cpsc408!",
    auth_plugin = 'mysql_native_password',
    database="RideShare")

# create cursor object
cur_obj = conn.cursor()

"""  
# create rider table
query = '''
    CREATE TABLE rider(
        riderID INT NOT NULL PRIMARY KEY,
        fullName VARCHAR(40)
        creationDate DATETIME
    );
'''
cur_obj.execute(query)
conn.commit()
print('Rider Table Created')

# create driver table
query = '''
    CREATE TABLE driver(
        driverID INT NOT NULL PRIMARY KEY,
        fullName VARCHAR(40),
        rating DECIMAL,
        licensePlate VARCHAR(7),
        driverMode BOOLEAN
    );
'''
cur_obj.execute(query)
conn.commit()
print('Driver Table Created')

# create rides table
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
cur_obj.execute(query)
conn.commit()
print('Rides Table Created')
"""

#start screen of code
def startScreen():
    print("Welcome to your ride share app!")
    
# add a new user
def add_user():
    user_type = print("Do you want to create a rider (1) or driver (2) account?")
    choice = helper.get_choice([1,2])
    new_user_id = highest_id()
    
    # create a new rider
    if choice == 1:
        name = input("Enter your full name: ")
        
        insertQuery = '''
        INSERT INTO rider
        VALUES(%s,%s,%s)
        '''
        cur_obj.execute(insertQuery, (new_user_id, name, date.today()))
        conn.commit()
    # create a new driver
    else:
        name = input("Enter your full name: ")
        license_plate = input("Enter your license plate #: ")
        
        insertQuery = '''
        INSERT INTO driver
        VALUES(%s,%s,%s,%s,%s)
        '''
        cur_obj.execute(insertQuery, (new_user_id, name, 5.0, license_plate, False))
        conn.commit()
        
# find the highest id number in rider and driver table, add 1, and return the new_id
def highest_id():
    # find the highest id number in the rider table
    query1 = '''
    SELECT MAX(riderID)
    FROM rider
    '''
    cur_obj.execute(query1)
    max_riderID = cur_obj.fetchone()[0]
    
    # find the highest id number in the driver table
    query2 = '''
    SELECT MAX(driverID)
    FROM driver
    '''
    cur_obj.execute(query2)
    max_driverID = cur_obj.fetchone()[0]
    
    if int(max_riderID) > int(max_driverID):
        new_id = max_riderID + 1
    else:
        new_id = max_driverID + 1
        
    return new_id

# check if the user is a rider or driver
def check_user():
    while True:
        userID = input("What is your riderID or driverID?\n")
        
        # check if userID is a rider
        query = '''
        SELECT COUNT(*)
        FROM rider
        WHERE riderID = %s
        '''
        cur_obj.execute(query, (userID,))
        isRider = cur_obj.fetchone()[0]
        
        # check if userID is a driver
        query = '''
        SELECT COUNT(*)
        FROM driver
        WHERE driverID = %s
        '''
        cur_obj.execute(query, (userID,))
        isDriver = cur_obj.fetchone()[0]
        
        if isRider == 1:
            return 1
        elif isDriver == 1:
            return 0
        else:
            print("Incorrect userID. Try Again.")

#main program
startScreen()

# ask user if they are a new or returning user
user_type = print("Are you a new (1) or returning user (2)?")
num = helper.get_choice([1,2])
# if new, ask if rider or driver
if num == 1:
    add_user()
    # make an account for respective user
# else, ask the user for their userID
else:
    # determine if they are a rider or driver
    # if user_type = 1, user is a rider
    # if user_type = 0, user is a driver
    user_type = check_user()
    if user_type == 1:
        print("rider")
    else:
        print("driver")

# if user is a driver, show the following options:
    # 1. view their current rating
    # 2. view all rides they have driven for
    # 3. driver mode (activate/deactivate)
    
# if user is a rider, show the following options:
    # 1. view all rides they have taken
    # 2. find a driver
        # match rider with a driver that is activated
        # rider will be prompted for pick up & drop off location
        # create a ride
        # provide user with riderID
        # send rider back to the options menu
    # 3. rate driver
        # get user's last ride and get driver's ID
        # print information to user and ask if it's correct
        # if it's incorrect, have user enter the rideID
        # print information and ask user if it's correct
        # ask user for new rating 
        # calculate driver's new rating (current rating + new rating)/2

#db_ops.destructor()