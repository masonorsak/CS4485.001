# scp -i C:\Users\Mason\Desktop\seniordesign_ec2.pem C:\Users\Mason\Desktop\ML_single_device.py ec2-user@ec2-52-14-96-236.us-east-2.compute.amazonaws.com:/home/ec2-user

# import json
# import urllib.parse
import boto3
import pandas as pd 
import pymysql
# import sys
import pickle
import sklearn
import logging
# import time 
import numpy as np
import getopt
import sys
print('Loading function')

s3 = boto3.resource('s3')

rds_host  = "seniordesign.ctvqo2qqwjsj.us-east-2.rds.amazonaws.com"
name = "UTDesign"
password = "qmFRbbiwhq5ibLq"
db_name = "seniordesign"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# command line arguments list
argumentList = sys.argv[1:]
 
# Options for command line
options = "d:"
long_options = ["device"]

def lambda_handler():
    
    selectedDevice = 99

    try:
        # Parsing the arguments
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # Loop through each argument
        for currentArgument, currentValue in arguments:
            
            # if the current argumnet is valid
            if currentArgument in ("-d", "--device"):

                # ensure the argumnet is a integer
                try:
                    val = int(currentValue)
                    selectedDevice = val
                    print (("Selected device: %s") % (currentValue))
                except ValueError:
                    print("Command line argument for device is not a integer, aborting execution")
                    sys.exit("Invalid command line argument for device")

    except getopt.error as err:
        # output error, and return with an error code
        sys.exit(str(err))

    print(selectedDevice)

    try:
        connection = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        print("Connected to the database")
    except pymysql.MySQLError as e:
        print("Failed to connect to database")
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()
    
    sql = 'select time from devicedata where Device_DeviceID = %s and time >= ((select time from devicedata where Device_DeviceID = %s ORDER BY DeviceDataID DESC LIMIT 1) - 1440) GROUP BY time;' %(selectedDevice, selectedDevice)
    df = pd.read_sql(sql, con=connection)
    
    dftemp = pd.read_sql('select temp from weatherdata where CityData_CityID = 1 and time >= ((select time from weatherdata where CityData_CityID = 1 ORDER BY WeatherID DESC LIMIT 1) - 1440) GROUP BY time;', con=connection)
    
    
    
    time_index = pd.date_range('2016-01-07 00:34', periods=len(df),  freq='T')
    time_index = pd.DatetimeIndex(time_index)
    df = df.set_index(time_index)
    #df = df.drop(['time'], axis=1)
    
    df.iloc[np.r_[0:5,-5:0]].iloc[:,0]
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'time_data'})
    
    df['new_date'] = [d.date() for d in df['time_data']]
    df['new_time'] = [d.time() for d in df['time_data']]
    
    df["new_date"] = df["new_date"].astype(str)
    df["new_time"] = df["new_time"].astype(str)
    
    df['year'] = df['new_date'].str.split('-').str[0]
    df['month'] = df['new_date'].str.split('-').str[1]
    df['day'] = df['new_date'].str.split('-').str[2]
    
    df['hour'] = df['new_time'].str.split(':').str[0]
    df['minutes'] = df['new_time'].str.split(':').str[1]
    df['temp'] = dftemp['temp']
    # print(df)
    
    day = df.groupby(['hour'],as_index = False).median()
    device = pd.get_dummies(day, columns=['hour'])
    # print(device)
    
    
    x_int = device[['hour_01',
       'hour_02', 'hour_03', 'hour_04', 'hour_05', 'hour_06', 'hour_07',
       'hour_08', 'hour_09', 'hour_10', 'hour_11', 'hour_12', 'hour_13',
       'hour_14', 'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19',
       'hour_20', 'hour_21', 'hour_22', 'hour_23', 'temp']]
    # print(x_int)
    
    with open("/tmp/linear_reg.pk1", 'wb') as data:
        s3.Bucket("modelfile").download_fileobj("sagemaker/DEMO-xgboost-dm/linear_reg.pk1", data)
        
    
    model = None
    with open('/tmp/linear_reg.pk1', 'rb') as data:
        model = pickle.load(data)
    
    y_pred = model.predict(x_int)
    #print(y_pred)
    
    sql = 'select time, average from deviceavg where Device_DeviceID = %s;' %(selectedDevice)
    dfenergy = pd.read_sql(sql, con=connection)
    print(dfenergy)
    
    i = 0
    for actual in dfenergy.itertuples():
        
        # for pred in y_pred:
        #     print(actual.average)
        #     print(pred)
        if i > 23:
            i = 0
        if actual.average > y_pred[i]:
            #print('Alert')
            print(actual.time)
            with connection.cursor() as cursor:
                cursor.execute('update devicedata set anomaly = 1 where time = %s and device_deviceid = %s' % (actual.time, selectedDevice))
                connection.commit()
        i += 1
    
    # with connection.cursor() as cursor:
    #     cursor.execute('select energyUse from devicedata where Device_DeviceID = 4 and time >= ((select time from devicedata where Device_DeviceID = 4 ORDER BY DeviceDataID DESC LIMIT 1) - 43800) GROUP BY time;')
    #     connection.commit()
    #     rows = cursor.fetchall()
    #     print(rows)
    
    

    # # Get the object from the event and show its content type
    # bucket = 'outpututds3'
    # key = 'sagemaker/DEMO-xgboost-dm/output_data.csv'
    # csvfile = s3.get_object(Bucket=bucket, Key=key)
    # df_s3_data = pd.read_csv(csvfile['Body'], sep=',')
    # #print(df_s3_data)

    # df = pd.DataFrame(df_s3_data)
    # # The dataframe is only the columns of data were using
    # df = df[['Error','time']]
    # # print(df)

    # with connection.cursor() as cursor:
    #     for row in df.itertuples():
    #         if row.Error == "Alert":
    #             cursor.execute('update devicedata set anomaly = 1 where time = %s and device_deviceid = 4' % (row.time))
    #             connection.commit()
    print("Finished getting row times") 

            #print(row.time)
            # my_data.append(row.time)
    
    # print(my_data)

       
        # cursor.execute('update devicedata set anomaly = 1 where time = %s and device_deviceid = 4' % (row.time))
        # # rows = cursor.fetchall()
        # # for i in rows:
        # #     print(i)
        # connection.commit()

lambda_handler()