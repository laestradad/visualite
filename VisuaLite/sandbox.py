import pandas as pd
import os
# Execution path
PATH = os.getcwd()
print(PATH)

# Import saved dataframes for testing
LogsStandard = pd.read_pickle('PKL_One/LogsStandard.pkl')
print(LogsStandard.columns)
print(LogsStandard.shape)
mindate = LogsStandard['DateTime'].min()
maxdate = LogsStandard['DateTime'].max()
print(mindate, maxdate)

LogsAlarms = pd.read_pickle('PKL_One/LogsAlarms.pkl')
print(LogsAlarms.columns)
print(LogsAlarms.shape)

LogsEvents = pd.read_pickle('PKL_One/LogsEvents.pkl')
print(LogsEvents.columns)
print(LogsEvents.shape)
print(type(LogsEvents.columns.tolist()))

# ------------------------------------------------------------- EXPORT PLOT AS PNG
import modules.plots as fcm_plt

# Load txt file according machine type
fcm_plt.fcm.load_data('FCM One | 1.5')
#fcm_plt.fcm.load_data('FCM Oil 2b')

# Create figure and export image
#fig = fcm_plt.custom_plot_divided(LogsStandard, LogsAlarms, LogsEvents, ['PT1','PT2'], '2021-06-04', '2021-06-08', 'Plot_Title')
#fig.write_html('test.html', config={'displaylogo': False})
#file_path = "__vl.log/preview.png"
#fig.write_image(file_path)

# ------------------------------------------------------------- FUNCTION TO EXPORT EXCEL
def export_excel(dfs, sheetNames, date1, date2, cols, fileName):
	
	with pd.ExcelWriter(fileName) as writer:  
		for i, df in enumerate(dfs):
			if not df.empty:
				print(i)
				df_export = df[(df['DateTime'] > date1) & (df['DateTime'] <= date2)]

				if set(cols).issubset(df_export.columns.tolist()):
					cols.insert(0, 'DateTime')
					df_export = df_export[cols]
				elif 'Evn_Code_Label' in df_export.columns.tolist():
					del df_export['Evn_Code_Label']
				elif 'Alm_Code_Label' in df_export.columns.tolist():
					del df_export['Alm_Code_Label']

				df_export.to_excel(writer, sheet_name=sheetNames[i], index=False)

export_excel(
	dfs = [LogsStandard, LogsAlarms, LogsEvents],
	sheetNames = ['Standard', 'Alarms', 'Events'],
	date1 = '2021-06-04', date2 = '2021-06-08', 
	cols = ['PT1','PT2'], 
	fileName = 'test.xlsx'
	)

# ------------------------------------------------------------- POP UP EXAMPLE

import customtkinter as ctk
from PIL import Image

# Function to create and display the popup
def create_popup():
	# Create figure and export image
	fig = fcm_plt.custom_plot_divided(LogsStandard, LogsAlarms, LogsEvents, ['PT1','PT2'], '2021-06-04', '2021-06-08', 'Plot_Title')
	#fig.write_html('test.html', config={'displaylogo': False})
	file_path = "__vl.log/preview.png"
	fig.write_image(file_path)

	# Create a new TopLevel window for the popup
	popup = ctk.CTkToplevel(app)
	popup.title("Confirmation Popup")

	# Label in the popup
	label = ctk.CTkLabel(popup, text="Are you sure you want to continue?")
	label.pack()

	# Load an image for the popup
	image_import = ctk.CTkImage(Image.open("__vl.log/preview.png"), size=(700, 500))
	image_label = ctk.CTkLabel(popup, text="", image=image_import)
	image_label.pack()

	# Delete image file
	os.remove(file_path)

	# Button to confirm
	confirm_button = ctk.CTkButton(popup, text="Confirm", command=popup.destroy)
	confirm_button.pack()

	# Button to abort
	abort_button = ctk.CTkButton(popup, text="Abort", command=popup.destroy)
	abort_button.pack()

# Create the main app
app = ctk.CTk()
app.title("CustomTkinter App")

# Button to open the popup
popup_button = ctk.CTkButton(app, text="Open Popup", command=create_popup)
popup_button.pack()

app.mainloop()
