from helper import helper
from db_operations import db_operations

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

# confirm execution worked by printing result
cur_obj.execute("SHOW DATABASES;")
for row in cur_obj:
    print(row)
    
# create rider table
cur_obj.execute('''
    CREATE TABLE rider(
        riderID INT NOT NULL PRIMARY KEY,
        fullName VARCHAR(40),
        creationDate DATE,
    );
''')

# create driver table
cur_obj.execute('''
    CREATE TABLE driver(
        driverID INT NOT NULL PRIMARY KEY,
        fullName VARCHAR(40),
        rating DECIMAL,
        driverMode VARCHAR(20),
        licensePlate VARCHAR(7),
    );
''')

# create ride table
cur_obj.execute('''
    CREATE TABLE rides(
        rideID INT NOT NULL PRIMARY KEY,
        pickupLocation VARCHAR(40),
        dropoffLocation VARCHAR(40),
        dateAndTime DATETIME,
    );
''')

# Print out connection to verify and close
print(conn)
conn.close()

#start screen of code
def startScreen():
    print("Welcome to your ride share app!")


#main program
startScreen()

# ask user if they are a new or returning user
    # if new, ask if rider or driver
        # make an account for respective user
    # else, ask the user for their userID
        # determine if they are a rider or driver

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