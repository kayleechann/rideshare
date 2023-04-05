from helper import helper
from datetime import date
from datetime import datetime

# import MySQL
import mysql.connector

# Make connection
conn = mysql.connector.connect(host="localhost",
    user = "root",
    password = "cpsc408!",
    auth_plugin = 'mysql_native_password',
    database="RideShare")

# create cursor object
cur_obj = conn.cursor(buffered=True)

"""
# create rider table
query = '''
    CREATE TABLE rider(
        riderID INT NOT NULL PRIMARY KEY,
        fullName VARCHAR(40),
        creationDate DATE
    )
'''
cur_obj.execute(query)
conn.commit()
print('Rider Table Created')

# create driver table
query2 = '''
    CREATE TABLE driver(
        driverID INT NOT NULL PRIMARY KEY,
        fullName VARCHAR(40),
        rating DECIMAL,
        licensePlate VARCHAR(7),
        driverMode BOOLEAN
    )
'''
cur_obj.execute(query2)
conn.commit()
print('Driver Table Created')

# create rides table
query3 = '''
    CREATE TABLE rides(
        rideID INT NOT NULL PRIMARY KEY,
        pickupLocation VARCHAR(40),
        dropoffLocation VARCHAR(40),
        dateAndTime DATETIME,
        riderID INT,
        driverID INT,
        FOREIGN KEY (riderID) REFERENCES rider(riderID),
        FOREIGN KEY (driverID) REFERENCES driver(driverID)
    )
'''
cur_obj.execute(query3)
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
        global userID
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

# shows the driver their options
def driver_menu():
    print('''Select from the following menu options:
    1. View current rating
    2. View all rides you have driven for
    3. Change driver mode
        ''')
    return helper.get_choice([1,2,3])

def rider_menu():
    print('''Select from the following menu options:
    1. View all past rides
    2. Find a driver
    3. Rate a driver
          ''')
    return helper.get_choice([1,2,3])

def current_rating():
    query = '''
    SELECT rating
    FROM driver
    '''
    cur_obj.execute(query)
    return cur_obj.fetchone()[0]

def change_driver_mode():
    print("Would you like to activate (1) or deactivate (0) driver mode?")
    choice = helper.get_choice([0,1])
    
    query = '''
    UPDATE driver
    SET driverMode = %s
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (choice, userID))
    conn.commit()

# find rider a driver and create a ride
def find_driver():
    # find a driver that has driver mode activated
    query = '''
    SELECT driverID
    FROM driver
    WHERE driverMode = 1
    '''
    cur_obj.execute(query)
    driverID = cur_obj.fetchone()[0]
    print("Driver connected!")
    
    pickup = input("Enter pickup location: ")
    dropoff = input("Enter dropoff location: ")
    
    rideID = new_rideID()
    now = datetime.now()
    
    # create a ride
    query2 = '''
    INSERT INTO rides
    VALUES(%s,%s,%s,%s,%s,%s)
    '''
    cur_obj.execute(query2, (rideID, pickup, dropoff, now, userID, driverID))
    conn.commit()
    
# find an unused rideID
def new_rideID():
    # find the highest id number in the rides table
    query = '''
    SELECT MAX(rideID)
    FROM rides
    '''
    cur_obj.execute(query)
    max_riderID = cur_obj.fetchone()[0]
    
    new_id = max_riderID + 1
    return new_id
    

#main program
startScreen()

# ask user if they are a new or returning user
user_type = print("Are you a new (1) or returning user (2)?")
num = helper.get_choice([1,2])

# if new, ask if rider or driver
if num == 1:
    # make an account for respective user
    add_user()
# else, ask the user for their userID
else:
    # determine if they are a rider or driver
    # if user_type = 1, user is a rider
    # if user_type = 0, user is a driver
    user_type = check_user()
    if user_type == 1:
        user_choice = rider_menu()
        if user_choice == 1:
            # view all rides
            print("rides: ")
        if user_choice == 2:
            # find a driver
            find_driver()
    else:
        user_choice = driver_menu()
        if user_choice == 1:
            # view current rating
            rating = current_rating()
            print("Your current rating: " + str(rating))
        if user_choice == 2:
            # view all rides
            print("rides: ")
        if user_choice == 3:
            # change driver mode
            change_driver_mode()

# if user is a driver, show the following options:
    # 1. view their current rating DONE
    # 2. view all rides they have driven for
    # 3. driver mode (activate/deactivate) DONE
    
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