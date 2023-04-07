from helper import helper
from datetime import date
from datetime import datetime
from tabulate import tabulate

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
        rating DECIMAL(2,1),
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
        print("Rider account created!")
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
        print("Driver account created")
        
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
    
    if max_riderID == None and max_driverID == None:
        return 1
    if max_riderID == 1 and max_driverID == None:
        return 2
    if max_riderID == None and max_driverID == 1:
        return 2
    
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
    print('''\nSelect from the following menu options:
    1. View current rating
    2. View all rides you have driven for
    3. Change driver mode
        ''')
    return helper.get_choice([1,2,3])

# shows the rider their options
def rider_menu():
    print('''\nSelect from the following menu options:
    1. View all past rides
    2. Find a driver
    3. Rate a driver
          ''')
    return helper.get_choice([1,2,3])

# shows the driver their current rating
def current_rating(driver_id):
    query = '''
    SELECT rating
    FROM driver
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (driver_id,))
    return cur_obj.fetchone()[0]

# changes the driver mode
def change_driver_mode():
    print("\nWould you like to activate (1) or deactivate (0) driver mode?")
    choice = helper.get_choice([0,1])
    
    query = '''
    UPDATE driver
    SET driverMode = %s
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (choice, userID))
    conn.commit()
    
    if choice == 1:
        print("\nDriver mode activated!")
    if choice == 0:
        print("\nDriver mode deactivated!")

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
    
    print("\nThis is your rideID: " + str(rideID))
    
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

# lets the rider rate their driver 
def rate_driver():
    last_driverID = last_ride()
    driver_info(last_driverID)
    
    while True:
        print("\nIs this the correct driver you would like to rate? Yes (1) or No (2)")
        isCorrect = helper.get_choice([1,2])
        
        if isCorrect == 1:
            user_rating = input("\nOn a scale of 1-5, what would you like to rate your driver?\nRating: ")
            cur_rating = current_rating(last_driverID)
            new_rating = float((int(user_rating) + int(cur_rating)) / 2)
            update_rating(last_driverID, new_rating)
            break
        else:
            new_ride = input("\nEnter the rideID of the ride you would like to rate: ")
            new_driver = get_driverID(new_ride)
            driver_info(new_driver)

# return the driverID of the last ride that the rider took
def last_ride():
    query = '''
    SELECT driverID
    FROM rides
    WHERE riderID = %s
    ORDER BY dateAndTime DESC
    LIMIT 1
    '''
    cur_obj.execute(query, (userID,))
    driverID = cur_obj.fetchall()[0][0]
    return driverID

# prints driver's information to the user
def driver_info(driver_id):
    query = '''
    SELECT *
    FROM driver
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (driver_id,))
    results = cur_obj.fetchone()
    
    # prints all attributes of the driverID, except driverMode
    print("\nDriver information: ")
    for attribute in range(len(results) - 1):
        name = cur_obj.description[attribute][0]
        value = results[attribute]
        print(str(name) + ": " + str(value))
        
# get driverID from rideID
def get_driverID(ride_id):
    query = '''
    SELECT driverID
    FROM rides
    WHERE rideID = %s
    '''
    cur_obj.execute(query, (ride_id,))
    results = cur_obj.fetchall()[0][0]
    return results

# updates driver's rating
def update_rating(driver_id, new_rating):
    query = '''
    UPDATE driver
    SET rating = %s
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (new_rating, driver_id))
    conn.commit()
    print("\nSuccessfully rated driver!")
    
# list all rides of rider
def list_rider_rides():
    query = '''
    SELECT rideID, pickupLocation, dropoffLocation, dateAndTime
    FROM rides
    WHERE riderID = %s
    '''
    cur_obj.execute(query, (userID,))
    results = cur_obj.fetchall()
    
    print("\nYour rides: ")
    print(tabulate(results, headers=['Ride ID', 'Pickup Location', 'Dropoff Location', 'Date and Time'],tablefmt='psql'))

# list all rides of driver
def list_driver_rides():
    query = '''
    SELECT rideID, pickupLocation, dropoffLocation, dateAndTime
    FROM rides
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (userID,))
    results = cur_obj.fetchall()
    
    print("\nYour rides: ")
    print(tabulate(results, headers=['Ride ID', 'Pickup Location', 'Dropoff Location', 'Date and Time'],tablefmt='psql'))

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
        print("\nWelcome rider!")
        while True:
            user_choice = rider_menu()
            if user_choice == 1:
                # view all rides
                list_rider_rides()
                break
            if user_choice == 2:
                # find a driver
                find_driver()
            if user_choice == 3:
                # rate a driver
                rate_driver()
                break
    else:
        print("\nWelcome driver!")
        user_choice = driver_menu()
        if user_choice == 1:
            # view current rating
            rating = current_rating(userID)
            print("Your current rating: " + str(rating))
        if user_choice == 2:
            # view all rides
            list_driver_rides()
        if user_choice == 3:
            # change driver mode
            change_driver_mode()

conn.close()