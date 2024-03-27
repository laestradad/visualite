import pandas as pd
import glob

foldername = "LPG/"
file_name = "LPG.html" 

y1=['PIT1103 - Pressure transmitter PIT1103','PIT1003 - Pressure transmitter PIT1003','PIC1003 - Setpoint','PIC1103 - Setpoint']
y2=['Main sequence','Local stopping sub sequence','Stopping sub sequence']


# -------------------------------------------------------------------------------------------------------- import data
# Define files path
Path = "ProcessLog?*.csv"

# Read all the files name in the directory
AllFilesname = glob.glob(foldername + Path)

# Create an empty list to store the dataframes
ListDataframe = list()

# Total file number
NoFiles = len(AllFilesname)

# For each file in the specified directory import the data and add it in the list
for Filename in AllFilesname:
    ListDataframe.append(pd.read_csv(Filename, sep=';', skiprows=3, decimal=',', encoding='unicode_escape'))

# Concatenate the files in the list in unique dataframe
DataImport = pd.concat(ListDataframe, axis=0, ignore_index=True)

# Change datatypes
DataImport['Timestamp'] = pd.to_datetime(DataImport['Timestamp'], format='%Y %m %d %H:%M:%S:%f')
# ordering ascending
DataImport = DataImport.sort_values(by='Timestamp', ascending=True)

# -------------------------------------------------------------------------------------------------------- import data

import plotly.graph_objects as go
fig = go.Figure()
for column in y1:
    
    fig.add_trace(go.Scatter(x=DataImport['Timestamp'], y=DataImport[column], name=column))

for column in y2:
    
    fig.add_trace(go.Scatter(x=DataImport['Timestamp'], y=DataImport[column], name=column, yaxis="y2"))
    
fig.update_layout(
        legend=dict(orientation="v", borderwidth= 1),
        title_text='LPG',
        xaxis=dict(domain=[0, 0.9]),

        yaxis=dict(title="Vibration"),

        yaxis2=dict(
            title="INT",
            anchor="free",
            overlaying="y",
            side="right",
            position=0.9))

fig.write_html(file_name)


# Example of 4 y axis:
"""
fig.update_layout(
    legend=dict(orientation="v", borderwidth= 1),
    title_text=filename[:-4],
    xaxis=dict(domain=[0.2, 0.8]),

    yaxis=dict(title="Vibration"),

    yaxis2=dict(
        title="BOOL",
        anchor="free",
        overlaying="y",
        side="left",
        position=0.1),

    yaxis3=dict(
        title="INT_Status",
        anchor="x",
        overlaying="y",
        side="right"
    ),

    yaxis4=dict(
        title="",
        anchor="free",
        overlaying="y",
        side="right",
        position=0.9
    )
)
"""