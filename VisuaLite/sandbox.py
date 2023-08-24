from modules import data_analysis as fcm_da
from modules import plots as fcm_plt

import tkinter.filedialog as fd
import os
# Execution path
PATH = os.getcwd()

dirname = fd.askdirectory(title='Select a directory with log files')

csv_files_list = []
for filename in os.listdir(dirname):
    if filename.lower().endswith('.csv'):
        csv_files_list.append(filename)

if dirname != None:
    DataFiles = [dirname + '/' + x for x in csv_files_list if x.startswith('S')]
    AlarmFiles = [dirname + '/' + x for x in csv_files_list if x.startswith('A')]
    EventFiles = [dirname + '/' + x for x in csv_files_list if x.startswith('E')]
    print("DataFiles:")
    print(DataFiles)
    print("AlarmFiles:")
    print(AlarmFiles)
    print("EventFiles:")
    print(EventFiles)
else:
    print("dir name== None -> Stop")

# Import data from csv and format DataFrames
if len(DataFiles + AlarmFiles + EventFiles) == 0:
    print("no .csv files starting with S*, A* or E* --> Stop")
    print('Visualite could not find logs in the .csv files selected')


elif len(DataFiles + AlarmFiles + EventFiles) > 0:
    # TODO Check it is FCM One Log files
    import_success, mch_info, COs, LogsStandard, LogsAlarms, LogsEvents = fcm_da.import_data(DataFiles, AlarmFiles, EventFiles)
    print(f"{import_success=}")

fig = fcm_plt.new_change_over(fcm_da.ChangeOverToDF(logs=LogsStandard, CO=COs[0]),LogsAlarms,LogsEvents,mch_info)
fig.write_html(PATH+"/test1.html", config={'displaylogo': False})

fig2 = fcm_plt.new_change_over_overlap(fcm_da.ChangeOverToDF(logs=LogsStandard, CO=COs[0]),LogsAlarms,LogsEvents,mch_info)
fig2.write_html(PATH+"/test2.html", config={'displaylogo': False})
