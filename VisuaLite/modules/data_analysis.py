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
UNITS = os.path.join(SCRIPT_PATH, '..', 'resources', 'units.txt')

#----------------------------------------------------------- IMPORT UNITS FOR FCM ONE LOG FILES
with open(UNITS, 'r') as file:
    units = json.load(file)

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

    #Standard columns of FCM_ONE log files
    std_cols = ['DateTime','GpsPos','PT1','PT2','TT1','TT2','TargetTemperature','TemperatureLowLimit','TemperatureHighLimit',
                'VT','TargetViscosity','ViscosityLowLimit','ViscosityHighLimit','Density','FM1_MassFlow','FM1_Density',
                'FM1_Temperature','FM2_MassFlow','FM2_Density','FM2_Temperature','FM3_MassFlow','FM3_Density',
                'FM3_Temperature','FM4_MassFlow','FM4_Density','FM4_Temperature','FT_VolumeFlow','FT_MassFlow',
                'FT_Density','FT_Temperature','SO2','CO2','SC','CV1_Position','CV2_Position','CV3_Position','CV4_Position','CV5_Position',
                'CurrentControl','SupplyCurrentPump','CircCurrentPump','CurrentFilter','F60InAutoMode','ChangeOverInProgress','DPT_AI']
    alm_cols = ['DateTime', 'AlarmNumber']
    eve_cols = ['DateTime', 'GpsPos', 'EventNumber', 'Data']

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
                        check_cols = std_cols
                        
                    elif file_name[0] == 'A':
                        check_cols = alm_cols

                    elif file_name[0] == 'E':
                        check_cols = eve_cols

                    # Iterate row4 and check cols
                    for j, col in enumerate(check_cols):
                        if row[j] != col:
                            logger.error('--- File does not match with FCM One/1.5 log file structure')
                            logger.error(file)
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

    # DateTime
    DF_Data['DateTime'] = pd.to_datetime(DF_Data['DateTime'], format="%Y-%m-%d %H:%M:%S")
    # ordering ascending
    DF_Data = DF_Data.sort_values(by='DateTime', ascending=True).reset_index(drop=True)

    #Remove duplicates
    DF_Data.drop_duplicates(keep=False, inplace=True)
    
    logger.debug("--- raw data imported:")
    logger.debug(DF_Data.shape)
    logger.debug(DF_Data.columns.tolist())

    return(DF_Data)

@custom_callback # wrapper to catch errors
def import_data(dirname, file_list):
    logger.debug("--- import_data started ---")

    mch_info = None
    LogsStandard = pd.DataFrame()
    COs = []
    LogsAlarms = pd.DataFrame()
    LogsEvents = pd.DataFrame()

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
    
    logger.debug("Formatting Standard Logs ---")

    # Format LogsStandard
    LogsStandard = LogsStandard[['DateTime','GpsPos', 'ChangeOverInProgress','F60InAutoMode','CV1_Position', 'CV2_Position',
                    'CV3_Position', 'CV4_Position', 'CV5_Position', 'SupplyCurrentPump',
        'CircCurrentPump', 'CurrentControl', 'CurrentFilter',
        'PT1', 'PT2', 'TT1', 'TT2', 'TargetTemperature',
        'TemperatureLowLimit', 'TemperatureHighLimit', 'VT', 'TargetViscosity',
        'ViscosityLowLimit', 'ViscosityHighLimit', 'Density', 'FM1_MassFlow',
        'FM1_Density', 'FM1_Temperature', 'FM2_MassFlow', 'FM2_Density',
        'FM2_Temperature', 'FM3_MassFlow', 'FM3_Density', 'FM3_Temperature',
        'FM4_MassFlow', 'FM4_Density', 'FM4_Temperature', 'FT_VolumeFlow',
        'FT_MassFlow', 'FT_Density', 'FT_Temperature', 'SO2', 'CO2', 'SC','DPT_AI']]

    # Columns as float
    LogsStandard.iloc[:,13:] = LogsStandard.iloc[:,13:].astype(float)

    # Create labels for CV positions
    LogsStandard[['CV1_Label','CV2_Label','CV3_Label','CV4_Label','CV5_Label']] = LogsStandard[['CV1_Position','CV2_Position','CV3_Position','CV4_Position','CV5_Position']]

    LogsStandard[['CV1_Label']] = LogsStandard[['CV1_Label']] .replace({ 
        0: "Both LS activated",
        1: "Fuel 1 Position",
        2: "No LS activated",
        3: "Other fuel Position"
    }).fillna('Unknown')

    LogsStandard[['CV2_Label']] = LogsStandard[['CV2_Label']] .replace({ 
        0: "Both LS activated",
        1: "Fuel 2 Position",
        2: "No LS activated",
        3: "Other Fuel Position"
    }).fillna('Unknown')

    LogsStandard[['CV3_Label']] = LogsStandard[['CV3_Label']] .replace({ 
        0: "Both LS activated",
        1: "Fuel 3 Position",
        2: "No LS activated",
        3: "Fuel 4 Position"
    }).fillna('Unknown')

    LogsStandard[['CV4_Label']] = LogsStandard[['CV4_Label']] .replace({ 
        0: "Both LS activated",
        1: "Heater Position",
        2: "No LS activated",
        3: "Cooler Position"
    }).fillna('Unknown')

    LogsStandard[['CV5_Label']] = LogsStandard[['CV5_Label']] .replace({ 
        0: "Both LS activated",
        1: "Cooler Position",
        2: "No LS activated",
        3: "Bypass Position"
    }).fillna('Unknown')

    # Identify when Change Over Started and Finished
    # ChangeOverInProgress = O : no change
    # ChangeOverInProgress = 1 : started
    # ChangeOverInProgress = -1 : finished

    # Create column with value change
    LogsStandard['ChangeoverCMDchange'] = LogsStandard['ChangeOverInProgress'].diff()

    logger.debug("--- Standard Logs formatted")
    logger.debug(LogsStandard.shape)
    logger.debug(LogsStandard.columns.tolist())
    logger.debug(LogsStandard.dtypes)

    return(LogsStandard)

def Format_DF_ALogs(list_files):

    LogsAlarms = concat_files(list_files)
    logger.debug("Formatting Alarm Logs ---")

    LogsAlarms = LogsAlarms[['DateTime', 'AlarmNumber']]

    # Create Labels of the Alarms
    LogsAlarms['Label'] = LogsAlarms['AlarmNumber'] 
    LogsAlarms[['Label']] = LogsAlarms[['Label']] .replace({ 
        0: "PLC battery low / Not present",
        1: "Dynamic I/O Configuration Error",
        2: "Dynamic I/O Configuration In Progress",
        3: "Dynamic I/O Configuration Done",
        4: "Invalid GPS Sig-nal ",
        5: "I/O Module Error",
        102: "Emergency stop",
        103: "Power failure",
        104: "Instrument Mod-bus Communi-cation Error",
        105: "UPS Battery Low",
        106: "Local HMI com-munication lost",
        107: "Remote HMI communication lost",
        200: "Changeover Valve 1 Alarm",
        201: "Changeover Valve 2 Alarm",
        202: "Changeover Valve 3 Alarm",
        203: "Changeover Finished",
        300: "SCT sensor fault, signal missing",
        301: "Fuel consump-tion too low for blending",
        400: "Supply Pump 1 failure",
        401: "Supply Pump 2 failure",
        402: "Supply pump 1 Not Available",
        403: "Supply pump 2 Not Available",
        404: "PT1 limit high",
        405: "PT1 limit low",
        406: "PT1 sensor fault, signal missing",
        408: "Supply Pump switch over done",
        409: "Automatic switch of Supply Pumps in a short time",
        410: "Standby Supply Pump run time reset to zero",
        411: "Supply Pump switch time elapsed",
        412: "Supply Pump switching failed",
        413: "Standby Supply Pump not avail-able Please re-store it",
        414: "Warning/Alarm on VFD 1",
        415: "Warning/Alarm on VFD 2",
        500: "Circulation Pump 1 failure",
        501: "Circulation Pump 2 failure",
        502: "Circulation pump 1 Not Available",
        503: "Circulation pump 2 Not Available",
        504: "PT2 limit high",
        505: "PT2 limit low",
        506: "PT2 sensor fault, signal missing",
        508: "Circulation Pump switch-over done",
        509: "Automatic switch of Circulation Pumps in a short time",
        510: "Standby Circulation Pump run time reset to zero",
        511: "Circulation Pump switch time elapsed",
        512: "Circulation Pump switching failed ",
        513: "Standby Circula-tion Pump not available. Please restore it.",
        600: "Automatic Filter Differential Pressure high",
        601: "Automatic Filter Failure",
        602: "DPT Filter Fault",
        800: "Mixing tank low level",
        900: "Electric Heater 1-Fault",
        901: "Electric Heater 2-Fault",
        902: "Fuel Temperature High",
        903: "Fuel Temperature Low",
        905: "Chiller Fault",
        906: "Viscosity not reached during Changeover.",
        907: "TT1 sensor fault, signal missing",
        908: "TT2 sensor fault, signal missing",
        911: "CV4 Alarm",
        912: "CV5 Alarm",
        913: "Switched to Vis-cosity control",
        914: "Switched to Temperature control",
        915: "Temperature control out of order, will be switched off within 5 minutes",
        916: "Temperature control switched off",
        917: "Very high temperature reached",
        1000: "Viscosity Sensor Fault",
        1002: "Density Sensor Fault",
        1004: "Fuel viscosity High limit alarm",
        1005: "Fuel viscosity Low limit alarm"
    }).fillna('Unknown')

    LogsAlarms['Alm_Code_Label'] = "A" + LogsAlarms['AlarmNumber'].astype(str) + "_" + LogsAlarms['Label'] 
    
    logger.debug("--- Alarm Logs formatted")
    logger.debug(LogsAlarms.shape)
    logger.debug(LogsAlarms.columns.tolist())
    logger.debug(LogsAlarms.dtypes)

    return(LogsAlarms)

def Format_DF_ELogs(list_files):
    LogsEvents = concat_files(list_files)
    logger.debug("Formatting Event Logs ---")

    LogsEvents = LogsEvents[['DateTime', 'GpsPos', 'EventNumber', 'Data']]
    LogsEvents['Label'] = LogsEvents['EventNumber'] 

    #Create Labels of the Events
    LogsEvents[['Label']] = LogsEvents[['Label']] .replace({0 : 'FCM Started',
                                                            1 : 'FCM Stopped',
                                                            2 : 'Changeover initiated',
                                                            3 : 'Changeover Finsihed',
                                                            4 : 'Any device in Manual Mode',
                                                            5 : 'All device in Auto Mode',
                                                            6 : 'P401 SPump value changed',
                                                            7 : 'P501 CPump value changed',
                                                            8 : 'P903 Heater In Use value changed',
                                                            30 : 'Auto Mode Selected',
                                                            31 : 'Manual Mode Selected'}).fillna('Unknown')

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

