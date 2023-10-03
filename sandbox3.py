import os
import tkinter.filedialog as fd
# Execution path
PATH = os.getcwd()

#dirname = fd.askdirectory(title='Select a directory with log files')
#
#csv_files_list = []
#for filename in os.listdir(dirname):
#    if filename.lower().endswith('.csv'):
#        csv_files_list.append(filename)

import pandas as pd

data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}

#load data into a DataFrame object:
df = pd.DataFrame(data)

# Export to excel
import xlsxwriter
newfile=os.path.join(PATH,'LogsData.xlsx')

writer = pd.ExcelWriter(newfile, engine='xlsxwriter')
#workbook  = writer.book

df.to_excel(writer, 'LogsStandard', index=False)
worksheet = writer.sheets['LogsStandard'] 

writer.save()
#C:\_Projects\_REPO\_otherREPO\_VisuaLite_DEV\sandbox3.py:33: 
#FutureWarning: save is not part of the public API, usage can give unexpected results and will be removed in a future version writer.save()

