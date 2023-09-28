from fcm_basic import *
import os
import tkinter.filedialog as fd
# Execution path
PATH = os.getcwd()

import json
TXT_FILE = 'Visualite/resources/fcm_one.txt'  # Replace with the path to your text file

with open(TXT_FILE, 'r') as file:
    data = json.load(file)

# Access data like this:
std_cols = data['std_cols']
print(std_cols)

if False:
    dirname = fd.askdirectory(title='Select a directory with log files')

    csv_files_list = []
    for filename in os.listdir(dirname):
        if filename.lower().endswith('.csv'):
            csv_files_list.append(filename)

#COs, LogsStandard, LogsAlarms = import_data(dirname, csv_files_list)

plot_type = "Overlap" # "Separate" or "Overlap"

if COs:
    print("COs:")
    print(COs)            
    
    for i, CO in enumerate(COs):
        df = ChangeOverToDF(CO, LogsStandard)

        #Plot Type
        if plot_type == "Overlap":
            fig = change_over_overlap(df, LogsAlarms)
            name_file= "ov_CO"+ str(i+1) + "_" + str(CO['Start'].date()) + ".html"

        elif plot_type == "Separate":
            fig = change_over_divided(df, LogsAlarms)
            name_file= "sp_CO"+ str(i+1) + "_" + str(CO['Start'].date()) + ".html"

        file_path = os.path.join(PATH, name_file)
        print("File to create:")
        print(file_path)

        try:
            fig.write_html(file_path, config={'displaylogo': False})

        except Exception as e:
            print("--- Error saving file")
            print(e)
