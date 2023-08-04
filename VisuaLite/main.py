from modules import fcm_one as fcm 
import glob

# Folder name / TODO: GET FROM USER
foldername = "FCM_B_C/FCM_C/LogExport202107061025/"

# Define files path, read all the files name in the directory
Name = "S?*.csv"
DataFiles = glob.glob(foldername + Name)
print(DataFiles)

# Define files path, read all the files name in the directory
Name = "A?*.csv"
AlarmFiles = glob.glob(foldername + Name)
print(AlarmFiles)

# Define files path, read all the files name in the directory
Name = "E?*.csv"
EventFiles = glob.glob(foldername + Name)
print(EventFiles)

#Check if all files are from the same machine / flag_files=1 if all good
files = DataFiles + AlarmFiles + EventFiles
flag_files, mch_info = fcm.check_files(files)

# Import data and creat DataFrames
if flag_files:

    # LOGS STANDARD
    if DataFiles:
        LogsStandard = fcm.Format_DF_SLogs(DataFiles)
        COs = fcm.IdentifyCOs(LogsStandard)

    # ALARMS
    if AlarmFiles:
        LogsAlarms = fcm.Format_DF_ALogs(AlarmFiles)

    # EVENTS
    if EventFiles:
        LogsEvents = fcm.Format_DF_ELogs(EventFiles)

df = fcm.ChangeOverToDF(COs[1], LogsStandard)

fig = fcm.Plot_ChangeOver(df, mch_info, LogsAlarms, LogsEvents)
fig.write_html("ChangeOver_test4ROWS.html", config={'displaylogo': False})
#fig.update_layout(autosize=False, width=1000, height=800)
#fig.show(config={'displaylogo': False})

fig2 = fcm.Plot_ChangeOver_simple(df)
fig2.write_html("ChangeOver_test1ROW.html", config={'displaylogo': False})
#fig2.update_layout(autosize=False, width=1000, height=800)
#fig2.show(config={'displaylogo': False})

