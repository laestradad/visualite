import pandas as pd
import datetime
import os
from csv import reader
import json
import re

from modules.logging_cfg import setup_logger
logger = setup_logger()
logger.info("data_analysis.py imported")

# Get the path to the current script
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
# Alfa Laval Logo path
AL_LOGO = os.path.join(SCRIPT_PATH, '..', 'resources', 'ALlogo.png')
# Construct the path to the file.txt in the resources directory
FCM_BASIC = os.path.join(SCRIPT_PATH, '..', 'resources', 'fcm_basic.txt')
FCM_ONE = os.path.join(SCRIPT_PATH, '..', 'resources', 'fcm_one.txt')
# Empty variable to load data of txt files
DATA = None
# Empty variable to save Machine Type
MT = None

#----------------------------------------------------------- DECORATORS
def custom_callback(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error("--- Callback failed ---")
            logger.error(e, exc_info=True)
    return wrapper

#----------------------------------------------------------- FUNCTIONS
# Check csv files
def read_mch_info(file):
    with open(file, 'r') as csv_file:
        csv_reader = reader(csv_file, delimiter=';')
        mch_info = []
        for i, row in enumerate(csv_reader):
            # row variable is a list that represents a row in csv
            mch_info.append(row[0])
            if i == 2:
                break          
    return(mch_info)

def load_data(mch_type):
    logger.debug("load_data started ---")
    
    if mch_type == "FCM One | 1.5":
        txt_file = FCM_ONE

    elif mch_type == "FCM Oil 2b":
        txt_file = FCM_BASIC

    global DATA
    with open(txt_file, 'r') as file:
        DATA = json.load(file)

    logger.debug(DATA)
    logger.debug("--- load_data finsihed")

def check_files (files):
    logger.debug("check_files started ---")

    #Standard file name pattern
    pattern = r"^[ASE]_\d{4}_\d{1,2}_\d{1,2}__\d{1,2}_\d{1,2}_\d{1,2}\.csv$"
    """
    ^: Start of the string 
    [ASE]: either "A", "S", or "E" 
    _: character 
    \d{4}: Matches exactly 4 digits 
    \d{1,2}: Matches 1 or 2 digits 
    \.csv: Matches the ".csv" extension
    $: End of the string
    """

    #Retrieve sample Machine information
    mch_info_check = read_mch_info(files[0])
    logger.debug(f"{mch_info_check=}")

    for file in (files):
        #Check file name
        file_name = file.split('/')[-1] #get file name from path
        if re.match(pattern, file_name) is None: #re library
            logger.error('--- File name does not correspond to FCM structure')
            logger.error(file)
            return 0, file

        with open(file, 'r') as csv_file:
            csv_reader = reader(csv_file, delimiter=';')
            mch_info = []
            for i, row in enumerate(csv_reader):
                if i < 3:
                    #Save first three rows
                    mch_info.append(row[0])
                elif i == 3:
                    # Compare it with sample machine info
                    if mch_info != mch_info_check:
                        logger.error('--- File does not correspond to the same machine')
                        logger.error(file)
                        return 0, file

                    #Standard columns
                    if file_name[0] == 'S':
                        check_cols = DATA['std_cols']
                        
                    elif file_name[0] == 'A':
                        check_cols = DATA['alm_cols']

                    elif file_name[0] == 'E':
                        check_cols = DATA['eve_cols']

                    # Iterate row4 and check cols are from fcm logs
                    for col in check_cols:
                        if not (col in row):
                            logger.debug(row)
                            logger.error("Column not found in std_cols: " + col)
                            logger.debug(check_cols)
                            logger.error(file)
                            logger.error('--- File does not match with FCM One/1.5 log file structure')
                            return 0, file

    logger.debug('--- All files correspond to the same machine and FCM One/1.5 log file structure')
    return 1, mch_info_check

# Import data
def concat_files(AllFilesNames):
    logger.debug("concat_files started ---")
   # Create an empty list to store the dataframes
    ListDataframe = list()

    # For each file in the specified directory import the data and add it in the list
    for Filename in AllFilesNames:
        ListDataframe.append(pd.read_csv(Filename, sep=';', skiprows=3, decimal=',', encoding='unicode_escape'))

    # Concatenate the files in the list in unique dataframe
    DF_Data = pd.concat(ListDataframe, axis=0, ignore_index=True)

    #Remove duplicates
    DF_Data.drop_duplicates(keep=False, inplace=True)
    
    logger.debug("--- raw data imported:")
    logger.debug(DF_Data.shape)
    logger.debug(DF_Data.columns.tolist())

    return(DF_Data)

@custom_callback # wrapper to catch errors
def import_LPGdata(dirname,file_list):
    logger.debug("--- import_LPGdata started ---")

    LogsStandard = pd.DataFrame()
    LogsAlarms = pd.DataFrame()

    #Create paths joining folder and file names
    if dirname != None:
        DataFiles = [dirname + '/' + x for x in file_list if x.startswith('ProcessLog')]
        AlarmFiles = [dirname + '/' + x for x in file_list if x.startswith('Alarms')]
    else:
        logger.debug("dirname == None -> Stop")
        return 4, None, None
    
    # Check file names first
    if len(DataFiles + AlarmFiles) == 0:
        logger.debug("no .csv files starting with ProcessLog* or Alarms* --> Stop")
        return 2, None, None
    
    #Check file missing

    # Import process logs
    logger.debug("Importing LPG Process Logs ---")
    LogsStandard = Format_LPG_PLogs(DataFiles)
    LogsAlarms = Format_LPG_ALogs(AlarmFiles)

    return 1, LogsStandard, LogsAlarms


# Formatting of DataFrames
def Format_LPG_PLogs(list_files):
    LogsStandard = concat_files(list_files)

    # Change datatypes
    LogsStandard['Timestamp'] = pd.to_datetime(LogsStandard['Timestamp'], format='%Y %m %d %H:%M:%S:%f')
    # ordering ascending
    LogsStandard = LogsStandard.sort_values(by='Timestamp', ascending=True)

    logger.debug("--- LPG Process Logs formatted")
    logger.debug(LogsStandard.shape)
    logger.debug(LogsStandard.columns.tolist())
    logger.debug(LogsStandard.dtypes)

    return(LogsStandard)

# Formatting of DataFrames
def Format_LPG_ALogs(list_files):
    LogsAlarms = concat_files(list_files)

    # there should be only 1 Alarm file
    LogsAlarms = pd.read_csv(list_files[0], sep=',', decimal='.', encoding='unicode_escape')

    # Rename Time
    LogsAlarms.rename(columns = {'Time':'Timestamp',' Change':'Change',
                            ' Instance':'Instance', ' Name':'Name',
                            ' Code':'Code', ' Severity':'Severity',
                            ' AdditionalInformation1':'AdditionalInformation1',
                            ' AdditionalInformation2':'AdditionalInformation2',
                            ' Message':'Message'}, inplace = True)


    # Change datatypes
    LogsAlarms['Timestamp'] = pd.to_datetime(LogsAlarms['Timestamp'], format='%Y-%m-%d %H:%M:%S:%f')
    # ordering ascending
    LogsAlarms = LogsAlarms.sort_values(by='Timestamp', ascending=True)
    # translate values
    LogsAlarms['Change_val'] = LogsAlarms['Change'].replace({' Active -> Inactive' : '0',
                                                    ' Inactive -> Active' : '1',
                                                    ' Unacknowledged -> Acknowledged': '2'})
    LogsAlarms['Change_val'] = LogsAlarms['Change_val'].astype(int)


    logger.debug("--- LPG Process Logs formatted")
    logger.debug(LogsAlarms.shape)
    logger.debug(LogsAlarms.columns.tolist())
    logger.debug(LogsAlarms.dtypes)

    return(LogsAlarms)

@custom_callback # wrapper to catch errors
def import_data(dirname, file_list, mch_type):
    logger.debug("--- import_data started ---")
    
    # Save machine type
    global MT
    MT = mch_type
    logger.debug(f"{mch_type=}")

    # Load data from txt files
    load_data(MT)

    #Init variables
    mch_info = None
    LogsStandard = pd.DataFrame()
    COs = []
    LogsAlarms = pd.DataFrame()
    LogsEvents = pd.DataFrame()

    #Create paths joining folder and file names
    if dirname != None:
        DataFiles = [dirname + '/' + x for x in file_list if x.startswith('S')]
        AlarmFiles = [dirname + '/' + x for x in file_list if x.startswith('A')]
        EventFiles = [dirname + '/' + x for x in file_list if x.startswith('E')]
    else:
        logger.debug("dirname == None -> Stop")
        return 4, None, None, None, None, None 

    # Check file names first
    if len(DataFiles + AlarmFiles + EventFiles) == 0:
        logger.debug("no .csv files starting with S*, A* or E* --> Stop")
        return 2, None, None, None, None, None 

    #Check if all files are from the same machine and corrispond to csv log file structure / flag_files=1 if all good
    files = DataFiles + AlarmFiles + EventFiles
    flag_files, mch_info = check_files(files)

    # Import data and creat DataFrames
    if flag_files == 1:

        # LOGS STANDARD
        if DataFiles:
            logger.debug("Importing Standard Logs ---")

            LogsStandard = Format_DF_SLogs(DataFiles)
            COs = IdentifyCOs(LogsStandard)

        # ALARMS
        if AlarmFiles:
            logger.debug("Importing Alarm Logs ---")
            LogsAlarms = Format_DF_ALogs(AlarmFiles)

        # EVENTS
        if EventFiles:
            logger.debug("Importing Event Logs ---")
            LogsEvents = Format_DF_ELogs(EventFiles)

        logger.debug("--- import_data success")
        return 1, mch_info, COs, LogsStandard, LogsAlarms, LogsEvents
    
    else:
        logger.debug("--- import_data aborted")
        return 0, mch_info, None, None, None, None  

# Formatting of DataFrames
def Format_DF_SLogs(list_files):

    LogsStandard = concat_files(list_files)
    
    # DateTime
    LogsStandard['DateTime'] = pd.to_datetime(LogsStandard['DateTime'], format="%Y-%m-%d %H:%M:%S")
    # ordering ascending
    LogsStandard = LogsStandard.sort_values(by='DateTime', ascending=True).reset_index(drop=True)
    
    logger.debug("Formatting Standard Logs ---")

    # Format LogsStandard
    LogsStandard = LogsStandard[DATA['std_cols']]

    if MT == "FCM One | 1.5":
        # Columns as float
        LogsStandard.iloc[:,13:] = LogsStandard.iloc[:,13:].astype(float)

        # Create labels for CV positions
        LogsStandard[['CV1_Label','CV2_Label','CV3_Label','CV4_Label','CV5_Label']] = LogsStandard[['CV1_Position','CV2_Position','CV3_Position','CV4_Position','CV5_Position']].astype(str)

        LogsStandard[['CV1_Label']] = LogsStandard[['CV1_Label']].replace(DATA['cv1_labels']).fillna('Unknown')

        LogsStandard[['CV2_Label']] = LogsStandard[['CV2_Label']].replace(DATA['cv2_labels']).fillna('Unknown')

        LogsStandard[['CV3_Label']] = LogsStandard[['CV3_Label']].replace(DATA['cv3_labels']).fillna('Unknown')

        LogsStandard[['CV4_Label']] = LogsStandard[['CV4_Label']].replace(DATA['cv4_labels']).fillna('Unknown')

        LogsStandard[['CV5_Label']] = LogsStandard[['CV5_Label']].replace(DATA['cv5_labels']).fillna('Unknown')

        LogsStandard['CC_Label'] = LogsStandard['CurrentControl'].astype(str)
        LogsStandard['CC_Label'] = LogsStandard['CC_Label'].replace(DATA['current_ctrl_label']).fillna('Unknown')

        # Identify when Change Over Started and Finished
        # ChangeOverInProgress = O : no change
        # ChangeOverInProgress = 1 : started
        # ChangeOverInProgress = -1 : finished

        # Create column with value change
        LogsStandard['ChangeoverCMDchange'] = LogsStandard['ChangeOverInProgress'].diff()

    elif MT == "FCM Oil 2b":
        # Columns as float
        LogsStandard.iloc[:,8:] = LogsStandard.iloc[:,8:].astype(float)

        # Create labels for CV positions
        LogsStandard[['CV1_Label','CV2_Label','CV3_Label','CV4_Label']] = LogsStandard[['CV1_Position','CV2_Position','CV3_Position','CV4_Position']].astype(str)

        LogsStandard[['CV1_Label']] = LogsStandard[['CV1_Label']].replace(DATA['cv1_labels']).fillna('Unknown')

        LogsStandard[['CV2_Label']] = LogsStandard[['CV2_Label']].replace(DATA['cv2_labels']).fillna('Unknown')

        LogsStandard[['CV3_Label']] = LogsStandard[['CV3_Label']].replace(DATA['cv3_labels']).fillna('Unknown')

        LogsStandard[['CV4_Label']] = LogsStandard[['CV4_Label']].replace(DATA['cv4_labels']).fillna('Unknown')

        LogsStandard['STS_Label'] = LogsStandard['MachineStatus'].astype(str)
        LogsStandard['STS_Label'] = LogsStandard['STS_Label'].replace(DATA['machine_sts_label']).fillna('Unknown')

        LogsStandard['CC_Label'] = LogsStandard['ControlType'].astype(str)
        LogsStandard['CC_Label'] = LogsStandard['CC_Label'].replace(DATA['current_ctrl_label']).fillna('Unknown')

        # Identify when Change Over Started and Finished
        # ChangeOverInProgress = 0 : no change
        # ChangeOverInProgress = 1 : started
        # ChangeOverInProgress = -1 : finished

        # Create column with value change
        LogsStandard['ChangeoverCMDchange'] = LogsStandard['ChangeoverInProgress'].diff()

    logger.debug("--- Standard Logs formatted")
    logger.debug(LogsStandard.shape)
    logger.debug(LogsStandard.columns.tolist())
    logger.debug(LogsStandard.dtypes)

    return(LogsStandard)

def Format_DF_ALogs(list_files):

    LogsAlarms = concat_files(list_files)
    logger.debug("Formatting Alarm Logs ---")

    # DateTime
    LogsAlarms['DateTime'] = pd.to_datetime(LogsAlarms['DateTime'], format="%Y-%m-%d %H:%M:%S")
    # ordering ascending
    LogsAlarms = LogsAlarms.sort_values(by='DateTime', ascending=True).reset_index(drop=True)

    LogsAlarms = LogsAlarms[['DateTime', 'AlarmNumber']]

    # Create Labels of the Alarms
    LogsAlarms['Label'] = LogsAlarms['AlarmNumber'].astype(str)
    LogsAlarms[['Label']] = LogsAlarms[['Label']] .replace(DATA['alarm_labels']).fillna('Unknown')

    LogsAlarms['Alm_Code_Label'] = "A" + LogsAlarms['AlarmNumber'].astype(str) + "_" + LogsAlarms['Label'] 
    
    logger.debug("--- Alarm Logs formatted")
    logger.debug(LogsAlarms.shape)
    logger.debug(LogsAlarms.columns.tolist())
    logger.debug(LogsAlarms.dtypes)

    return(LogsAlarms)

def Format_DF_ELogs(list_files):
    LogsEvents = concat_files(list_files)
    logger.debug("Formatting Event Logs ---")

    # DateTime
    LogsEvents['DateTime'] = pd.to_datetime(LogsEvents['DateTime'], format="%Y-%m-%d %H:%M:%S")
    # ordering ascending
    LogsEvents = LogsEvents.sort_values(by='DateTime', ascending=True).reset_index(drop=True)

    LogsEvents = LogsEvents[['DateTime', 'GpsPos', 'EventNumber', 'Data']]
    LogsEvents['Label'] = LogsEvents['EventNumber'].astype(str) 

    #Create Labels of the Events
    LogsEvents[['Label']] = LogsEvents[['Label']].replace(DATA['event_labels']).fillna('Unknown')

    # For events with relevant "Data", add it to label (e.g. parameter value)
    LogsEvents.loc[(LogsEvents['EventNumber'] == 6) |
                (LogsEvents['EventNumber'] == 7) | 
                (LogsEvents['EventNumber'] == 8), 'Label'] = LogsEvents['Label'].astype(str) + ": " + LogsEvents['Data'].astype(str)
    
    LogsEvents['Evn_Code_Label'] = "E" + LogsEvents['EventNumber'].astype(str) + "_" + LogsEvents['Label'] 

    logger.debug("--- Event Logs formatted")
    logger.debug(LogsEvents.shape)
    logger.debug(LogsEvents.columns.tolist())
    logger.debug(LogsEvents.dtypes)

    return(LogsEvents)

def IdentifyCOs(logs):
    logger.debug("IdentifyCOs started ---")

    # memorize starting DateTimes
    COstart = logs[logs['ChangeoverCMDchange'] == 1]['DateTime'].tolist()

    # memorize finishing DateTimes
    COfinish = logs[(logs['ChangeoverCMDchange'] == -1)]['DateTime'].tolist()

    COs = []
    for i in range(len(COfinish)):
        duration = COfinish[i]-COstart[i]
        if duration > datetime.timedelta(minutes = 1):
            COs.append({'Start': COstart[i], 'Finish': COfinish[i], 'Duration': duration})

    logger.debug('In the logs imported there are ' + str(len(COs)) + ' changeovers')
    for CO in COs:
        logger.debug('- From ' + str(CO['Start']) + ' to ' + str(CO['Finish']) + '. Duration: ' + str(CO['Duration'])) 

    return COs

@custom_callback # wrapper to catch errors
def ChangeOverToDF(CO, logs):
    logger.debug("ChangeOverToDF started ---")
    logger.debug(CO)

    delta = datetime.timedelta(minutes = 20)
    df = logs[(logs['DateTime'] >= CO['Start']-delta) & (logs['DateTime'] <= CO['Finish']+delta)]

    logger.debug(df.shape)
    return(df)

# custom plot funcions
@custom_callback # wrapper to catch errors
def classify_cols(selected):
    logger.debug("classify_cols started ---")
    logger.debug(f"{selected=}")

    units = DATA['units']

    filter_unit_cols = {col : unit for col, unit in units.items() if col in selected}
    # {key_expression: value_expression for item in iterable if condition}
    logger.debug(f"{filter_unit_cols=}")

    classified_cols = {}
    for col, unit in filter_unit_cols.items():
        if unit not in classified_cols:
            classified_cols[unit] = [] #if first column of this unit, create key and an empty array as value
        classified_cols[unit].append(col)
    
    logger.debug(f"{classified_cols=}")
    return classified_cols

@custom_callback # wrapper to catch errors
def date_limits (timestamp, lower, upper):
    logger.debug("date_limits started ---")
    #From dropdown options ("1hour", "2hours", etc) return datetimes

    date1 = timestamp
    date2 = timestamp

    if lower == "1 hour":
        date1 = timestamp - datetime.timedelta(hours=1)
    elif lower == "2 hours":
        date1 = timestamp - datetime.timedelta(hours=2)
    elif lower == "4 hours":
        date1 = timestamp - datetime.timedelta(hours=4)
    elif lower == "8 hours":
        date1 = timestamp - datetime.timedelta(hours=8)
    elif lower == "1 day":
        date1 = timestamp - datetime.timedelta(days=1)

    if upper == "1 hour":
        date2 = timestamp + datetime.timedelta(hours=1)
    elif upper == "2 hours":
        date2 = timestamp + datetime.timedelta(hours=2)
    elif upper == "4 hours":
        date2 = timestamp + datetime.timedelta(hours=4)
    elif upper == "8 hours":
        date2 = timestamp + datetime.timedelta(hours=8)
    elif upper == "1 day":
        date2 = timestamp + datetime.timedelta(days=1)
    
    return date1, date2

def split_df(LogsStandard):
    # Legacy function to divide dataframes in 5 days slices to minimize plot.html file size
    mindate = LogsStandard['DateTime'].min()
    maxdate = LogsStandard['DateTime'].max()
    print(mindate,maxdate)

    step = 5

    limits = []
    limits.append(mindate.date()-datetime.timedelta(days=1)) # first

    interval = maxdate - mindate

    while interval > datetime.timedelta(days=step):
        limits.append(limits[-1] + datetime.timedelta(days=step))
        interval = interval - datetime.timedelta(days=step)
        
    limits.append(maxdate.date()+datetime.timedelta(days=1)) # last

    import numpy as np
    limits = np.array(limits, dtype='datetime64')
    
    # Show Results
    for item in limits:
        print (item)

    # Divide all data in slices of 5 days
    dfs = []
    totalshape = 0

    for i in range(len(limits)-1):
        df = pd.DataFrame()
        df = LogsStandard[(LogsStandard['DateTime'] > limits[i]) & (LogsStandard['DateTime'] <= limits[i+1])]
        dfs.append(df)
        
        totalshape = totalshape + df.shape[0]
        print(df.shape)
        
    print (totalshape)

    for df in dfs:
        mindate = df['DateTime'].min()
        maxdate = df['DateTime'].max()
        print(mindate, maxdate)
        print('--')
