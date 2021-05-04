import pandas as pd
import pymysql
import time

start_time = time.time() # time how long the insert takes

# Read data into a panda dataframe, specify column data types to speed up program since pandas doesnt have to guess,
# Were importing 90,000 rows instead of all of them so importing doesnt take forever while we test
data = pd.read_csv (r'C:\Users\Mason\Desktop\UTD Spring 2021\Computer Science Project - 4485.001\archive\HomeC.csv', nrows=503910, 
    dtype={'Kitchen12': float,'Kitchen14': float,'Kitchen38': float,'Furnace1': float,'Furnace2': float,'WineCellar': float,'GarageDoor': float,
        'Barn': float,'Well': float, 'Solar': float, 'use': float, 'icon': "string", 'summary': "string", 'apparentTemperature': float,'precipProbability': float, 
        'windBearing': float, 'visibility': float, 'cloudCover': "string",'precipIntensity': float, 'gen': float, 'time': int,'HouseOverall': float,
        'Dishwasher': float,'HomeOffice': float,'Fridge': float,'KitchenTotal': float,'Microwave': float,'LivingRoom': float,'temperature': float,
        'humidity': float,'pressure': float,'windSpeed': float,'dewPoint': float})
df = pd.DataFrame(data)

# Sum everything into Kitchen
df['KitchenTotal'] = df[['Kitchen12','Kitchen14','Kitchen38']].sum(axis=1)

# Drop columns of data we wont be using
df = df.drop(['Kitchen12','Kitchen14','Kitchen38','Furnace1','Furnace2','WineCellar','GarageDoor','Barn','Well', 'Solar', 'use', 'icon', 'summary', 'apparentTemperature','precipProbability', 
              'windBearing', 'visibility', 'cloudCover','precipIntensity', 'gen'], axis=1)

# The dataframe is only the columns of data were using
df = df[['time','HouseOverall','Dishwasher','HomeOffice','Fridge','KitchenTotal','Microwave','LivingRoom','temperature', 'humidity','pressure','windSpeed','dewPoint']]

# Index the dataframe by a readable time formate, starting with date/time of first row
time_index = pd.DatetimeIndex(pd.date_range('2016-01-01 05:00', periods=len(df),  freq='min'))
time_index = pd.DatetimeIndex(time_index)
df = df.set_index(time_index)

# Connect to either our AWS RDS or local host depending on if were testing or deploying data
# connection = pymysql.connect(host='seniordesign.ctvqo2qqwjsj.us-east-2.rds.amazonaws.com',
#                              user='UTDesign',
#                              password='qmFRbbiwhq5ibLq',
#                              database='seniordesign',
#                              cursorclass=pymysql.cursors.DictCursor)
connection = pymysql.connect(host='127.0.0.1',
                             port=3307,
                             user='root',
                             password='Lasvegas2',
                             database='seniordesign',
                             cursorclass=pymysql.cursors.DictCursor)

cur_row = 0 # holds what row were currently on to tell user our progress
# Using the connection to the database, insert the data from the csv file
with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO House VALUES ();" #Create the house
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO Device (DeviceType, House_HouseID) VALUES (4,1);" #Create house overall
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO Device (DeviceType, House_HouseID) VALUES (5,1);" #Create dishwasher
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO Device (DeviceType, House_HouseID) VALUES (7,1);" #Create home office
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO Device (DeviceType, House_HouseID) VALUES (8,1);" #Create fridge
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO Device (DeviceType, House_HouseID) VALUES (11,1);" #Create kitchen total
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO Device (DeviceType, House_HouseID) VALUES (14,1);" #Create microwave
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO Device (DeviceType, House_HouseID) VALUES (15,1);" #Create living room
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO Weather (House_HouseID) VALUES (1);" #Create Weather
        cursor.execute(sql)
        connection.commit()

        sql = "INSERT INTO CityData (Weather_WeatherID) VALUES (1);" #Create City Data
        cursor.execute(sql)
        connection.commit()


        for row in df.itertuples(): # insert data into each device, row by row

            cur_row += 1 # were 1 row closer to being done
            percent_done = (cur_row / 503910) * 100 # calc what percent were at
            if(percent_done % 10 == 0): # every 10 weve finished tell the user
                print(str(percent_done) + "\% done")

            cursor.execute('INSERT INTO DeviceData (time, energyUse, Device_DeviceID) values (%s,%s,1);' % (row.time, row.HouseOverall))
            connection.commit()

            cursor.execute('INSERT INTO DeviceData (time, energyUse, Device_DeviceID) values (%s,%s,2);' % (row.time, row.Dishwasher))
            connection.commit()

            cursor.execute('INSERT INTO DeviceData (time, energyUse, Device_DeviceID) values (%s,%s,3);' % (row.time, row.HomeOffice))
            connection.commit()

            cursor.execute('INSERT INTO DeviceData (time, energyUse, Device_DeviceID) values (%s,%s,4);' % (row.time, row.Fridge))
            connection.commit()

            cursor.execute('INSERT INTO DeviceData (time, energyUse, Device_DeviceID) values (%s,%s,5);' % (row.time, row.KitchenTotal))
            connection.commit()

            cursor.execute('INSERT INTO DeviceData (time, energyUse, Device_DeviceID) values (%s,%s,6);' % (row.time, row.Microwave))
            connection.commit()

            cursor.execute('INSERT INTO DeviceData (time, energyUse, Device_DeviceID) values (%s,%s,7);' % (row.time, row.LivingRoom))
            connection.commit()

            cursor.execute('INSERT INTO WeatherData (CityData_CityID, time, temp, humidity, pressure, windSpeed, dewPoint) values (1,%s,%s,%s,%s,%s,%s);' % (row.time, row.temperature, row.humidity, row.pressure, row.windSpeed, row.dewPoint))
            connection.commit()

# Calc and display execution time of inserting all the data to the database
time = (time.time() - start_time)   # execution time in seconds is cur time - start time
day = time // (24 * 3600)           # integer division of seconds in a day
time = time % (24 * 3600)           # remainder after seconds in a day
hour = time // 3600                 # seconds in an hour
time %= 3600                        # remainder after seconds in an hour
minutes = time // 60                # seconds in a minute
time %= 60                          # remainder after seconds in a minute
seconds = time                      # how many seconds are left
print("Execution took %d days, %d hours, %d minutes, and %d seconds" % (day, hour, minutes, seconds)) # tell the user how long execution took