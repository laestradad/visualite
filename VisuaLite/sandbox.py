from modules import data_analysis as fcm_da
from modules import plots as fcm_plt
import matplotlib.pyplot as plt
import tkinter.filedialog as fd
import os
# Execution path
PATH = os.getcwd()

dirname = fd.askdirectory(title='Select a directory with log files')

csv_files_list = []
for filename in os.listdir(dirname):
    if filename.lower().endswith('.csv'):
        csv_files_list.append(filename)

custom_dark_style = {
    'axes.facecolor': '#29292929',  # Custom background color / DEFAULT '#1e1e1e'
    'axes.edgecolor': '#333333',  # Color of axes edges / DEFAULT '#ffffff'
    'axes.labelcolor': '#333333',  # Color of axes labels / DEFAULT 
    'text.color': '#333333',  # Color of text / DEFAULT '#ffffff'
    'xtick.color': '#333333',  # Color of x-axis ticks / DEFAULT '#ffffff'
    'ytick.color': '#333333',  # Color of y-axis ticks / DEFAULT '#ffffff'
    'figure.facecolor': '#29292929',  # Figure background color / DEFAULT '#1e1e1e'
    'figure.edgecolor': '#29292929',  # Figure edge color / DEFAULT '#1e1e1e'
    'axes.grid': False,  # Show grid / DEFAULT True
    'grid.color': '#333333',  # Color of grid lines / DEFAULT '#333333'
}

custom_light_style = {
    'axes.facecolor': '#d9d9d9d9',  # Custom background color / DEFAULT '#1e1e1e'
    'axes.edgecolor': '#e6e6e6e6',  # Color of axes edges / DEFAULT '#ffffff'
    'axes.labelcolor': '#e6e6e6e6',  # Color of axes labels / DEFAULT 
    'text.color': '#e6e6e6e6',  # Color of text / DEFAULT '#ffffff'
    'xtick.color': '#e6e6e6e6',  # Color of x-axis ticks / DEFAULT '#ffffff'
    'ytick.color': '#e6e6e6e6',  # Color of y-axis ticks / DEFAULT '#ffffff'
    'figure.facecolor': '#d9d9d9d9',  # Figure background color / DEFAULT '#1e1e1e'
    'figure.edgecolor': '#d9d9d9d9',  # Figure edge color / DEFAULT '#1e1e1e'
    'axes.grid': False,  # Show grid / DEFAULT True
    'grid.color': '#e6e6e6e6',  # Color of grid lines / DEFAULT '#333333'
}

def change_over_preview(df):

    plt.style.use(custom_light_style)

    # Create a two-row plot
    fig, ax1 = plt.subplots()

    ax1.set_title('Change Over Preview')
    ax1.grid(axis='both', linestyle='--', linewidth=0.5, alpha=0.7)  # Add auxiliary x-axis grid

    # Data
    x = df['DateTime']
    y1 = df['TT2']
    y2 = df['VT']

    #y1
    ax1.plot(x, y1, color='#e6e6e6e6', label='TT2') #e6e6e6e6 light #333333 dark
    ax1.set_ylabel('Temperature', color='#e6e6e6e6')
    ax1.tick_params(axis='y', labelcolor='#e6e6e6e6')

    #y2
    ax2 = ax1.twinx()
    ax2.plot(x, y2, color='#e6e6e6e6', label='VT')
    ax2.set_ylabel('Viscosity', color='#e6e6e6e6')
    ax2.tick_params(axis='y', labelcolor='#e6e6e6e6')

    # Set fewer ticks on the x-axis
    min_date = df['DateTime'].min()
    max_date = df['DateTime'].max()
    # Calculate the time interval between dates
    num_dates = 5
    date_delta = (max_date - min_date) / (num_dates - 1)
    # Generate the equally spaced dates
    x_ticks = [min_date + i * date_delta for i in range(num_dates)]

    # Set custom tick positions and labels on the x-axis
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels((date.strftime('%d/%m %H:%M') for date in x_ticks), rotation=45)  # Format and rotate tick labels

    # Adjust layout
    plt.tight_layout()

    return fig

import_success, mch_info, COs, LogsStandard, LogsAlarms, LogsEvents = fcm_da.import_data(dirname, csv_files_list)
print(f"{import_success=}")

fig = change_over_preview(fcm_da.ChangeOverToDF(logs=LogsStandard, CO=COs[1]))
fig.savefig("test.png", dpi=300, bbox_inches='tight', format='png')

#fcm_da.split_df(LogsStandard)

#fig = fcm_plt.new_change_over(fcm_da.ChangeOverToDF(logs=LogsStandard, CO=COs[0]),LogsAlarms,LogsEvents,mch_info)
#fig.write_html(PATH+"/test1.html", config={'displaylogo': False})
#
#fig2 = fcm_plt.new_change_over_overlap(fcm_da.ChangeOverToDF(logs=LogsStandard, CO=COs[0]),LogsAlarms,LogsEvents,mch_info)
#fig2.write_html(PATH+"/test2.html", config={'displaylogo': False})
