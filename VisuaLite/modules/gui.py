import pandas as pd
import os
import datetime
import re
from PIL import Image

import tkinter as tk
import tkinter.filedialog as fd
import tkcalendar
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules import data_analysis as fcm_da
from modules import help_app
from modules import plots as fcm_plt

from modules.logging_cfg import setup_logger
logger = setup_logger()
logger.info("gui.py imported")

VERSION = "V1.00.00"
#Execution path
PATH = os.getcwd()
logger.info(f"{PATH=}")
#Get the path to the current script
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
logger.info(f"{SCRIPT_PATH=}")
#App icon path
APP_ICON = os.path.join(SCRIPT_PATH, '..', 'resources', 'ad_logo.ico')
#Resources path
RESOURCES = os.path.join(SCRIPT_PATH, '..', 'resources')
#Options for dropdowns
TIMES = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
         '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
         '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

#Custom Tkinter theme
ctk.set_appearance_mode("dark")
#ctk.set_default_color_theme("dark-blue")
ctk.set_default_color_theme(os.path.join(RESOURCES, "al-blue.json"))

#--------------------------------------------------------------------- Frames Classes
class BreadcrumbFrame(ctk.CTkFrame):
    #Frame consisting 2 columns with 2 Label imgs used to show the steps of the App
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        logger.debug("BreadcrumbFrame init")

        # Load the images
        image1_path = os.path.join(RESOURCES, 'number-1.png')
        self.step1_img = Image.open(image1_path).resize((30, 30))
        self.step1_img_tk = ctk.CTkImage(self.step1_img)
        image1g_path = os.path.join(RESOURCES, 'number-one.png')
        self.step1g_img = Image.open(image1g_path).resize((30, 30))
        self.step1g_img_tk = ctk.CTkImage(self.step1g_img)

        image2_path = os.path.join(RESOURCES, 'number-2.png')
        self.step2_img = Image.open(image2_path).resize((30, 30))
        self.step2_img_tk = ctk.CTkImage(self.step2_img)
        image2g_path = os.path.join(RESOURCES, 'number-two.png')
        self.step2g_img = Image.open(image2g_path).resize((30, 30))
        self.step2g_img_tk = ctk.CTkImage(self.step2g_img)

        # STEP 1
        self.step1 = ctk.CTkFrame(self)
        self.step1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.step1_label = ctk.CTkLabel(self.step1, text="   Import Logs", image=self.step1_img_tk, compound="left")
        self.step1_label.grid(row=0, column=0, padx=20, pady=10)

        # STEP 2
        self.step2 = ctk.CTkFrame(self)
        self.step2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.step2_label = ctk.CTkLabel(self.step2, text="   Data Analysis Generator", image=self.step2g_img_tk, compound="left")
        self.step2_label.grid(row=0, column=0, padx=20, pady=10)

        #configure grid
        self.grid_rowconfigure(0, weight=1)
    
class CurrentStep(ctk.CTkFrame):
    # Frame composed by 2 labes with the title and explanation of the current step
    # Texts are configured in the App methods
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        logger.debug("CurrentStep init")

        # create Title and command row
        self.title = ctk.CTkLabel(self, fg_color="transparent", font=ctk.CTkFont(size=22, weight="bold"), anchor="nw")
        self.title.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
        # create label with explanation
        self.text = ctk.CTkLabel(self, fg_color="transparent", font=ctk.CTkFont(size=16), anchor="nw")
        self.text.grid(row=1, column=0, padx=25, pady=10, sticky="nw")
        # action button
        self.action_bt = ctk.CTkButton(self)
        self.action_bt.grid(row=1, column=2, padx=20, pady=10, sticky="se")

        # Set row and column weights to make it take the entire space
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

class EmptyFrame(ctk.CTkFrame):
    # Placeholder for init App
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        logger.debug("EmptyFrame init")
    
        # Set row and column weights to make it take the entire space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
class CheckBoxFrame(ctk.CTkFrame):
    #Frame consisting of 1 Scrollable frame for checkboxes and 1 frame for (un)select all
    
    def add_item(self, item):
        # Creation of checkbox 
        checkbox = ctk.CTkCheckBox(self.checkboxesFrame, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        
        # Position
        checkbox.grid(row=len(self.checkbox_list), column=0, padx=5, pady=10, sticky="w")
        
        # Default value
        checkbox.select()

        # Add to checkbox list
        self.checkbox_list.append(checkbox)

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]
    
    def select_all_files(self):
        for checkbox in self.checkbox_list:
            checkbox.select()

    def unselect_all_files(self):
        for checkbox in self.checkbox_list:
            checkbox.deselect()
            
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        logger.debug("CheckBoxFrame init")

        self.command = command

        # Set row and column weights to make it take the entire space
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Scrollable frame
        self.checkboxesFrame = ctk.CTkScrollableFrame(self)
        self.checkboxesFrame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Add 1 checkbox for each item in list (csv files)
        self.checkbox_list = []
        for item in item_list:
            self.add_item(item)

        # Frame with buttons
        self.btnsFrame = ctk.CTkFrame(self)
        self.btnsFrame.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
        self.select_all = ctk.CTkButton(self.btnsFrame, text="Select all", command=self.select_all_files)
        self.select_all.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        self.unselect_all = ctk.CTkButton(self.btnsFrame, text="Unselect all", command=self.unselect_all_files)
        self.unselect_all.grid(row=0, column=1, padx=10, pady=5, sticky="e")

class ProgressFrame(ctk.CTkFrame):
    # Frame with a generic Progess bar to show during import data
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        logger.debug("ProgressFrame init")

        # Set row and column weights to make it take the entire space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Progress bar
        self.progressbar_1 = ctk.CTkProgressBar(self)
        self.progressbar_1.grid(row=0, column=0, padx=20, pady=50, sticky="ew")
        self.progressbar_1.configure(mode="indeterminate")
        self.progressbar_1.start()

class NavFrame(ctk.CTkFrame):
    # Frame in the bottom of the app to go back and forward

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        logger.debug("NavFrame init")

        # Left button
        self.bt_navigation1 = ctk.CTkButton(self)
        self.bt_navigation1.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Right button
        self.bt_navigation2 = ctk.CTkButton(self)
        self.bt_navigation2.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        # Set row and column weights to make it take the entire space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

#--------------------------------------------------------------------- Custom Tkinter App
class App(ctk.CTk):

    # Version
    version = VERSION

    # GUI management
    frames = {} #dictionary containing frames
    current = None #class ctkFrame of current frame selected

    # Files selection
    dirname = None #folder with logs
    csv_files_list = [] #list of imported files
    
    # Import data
    import_success = 0 # bool of import data result
    mch_info = None # First 3 rows of csv files
    COs = None # List of changeovers
    LogsStandard = pd.DataFrame() #DataFrame with process logs
    LogsAlarms = pd.DataFrame() #DataFrame with alarm logs
    LogsEvents = pd.DataFrame() #DataFrame with event logs

    # ------------------------ Methods to change widgets properties
    def step_00_init(self):
        logger.debug("Widgets update step_00_init()")

        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure(1, weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)
        App.frames["BCFrame"].step1_label.configure(font=ctk.CTkFont(size=18, weight="bold"), image=App.frames["BCFrame"].step1_img_tk)
        App.frames["BCFrame"].step2_label.configure(font=ctk.CTkFont(size=15, weight="normal"), image=App.frames["BCFrame"].step2g_img_tk)

        #Update texts and action button
        App.frames["CSFrame"].title.configure(text="Import Logs")
        App.frames["CSFrame"].text.configure(text="Please select the folder containing the .csv files you want to analyse")
        App.frames["CSFrame"].action_bt.configure(text="Select folder")
        App.frames["CSFrame"].action_bt.configure(command=self.select_folder)
        App.frames["CSFrame"].action_bt.grid(row=1, column=2, padx=20, pady=10, sticky="se")

        # Machine Type dropdown
        #self.mch_type_dropdown.configure(state="enabled")

        #WorkSpace: Empty
        self.show_frame("WSFrame")
        
        #Update Navigation buttons
        App.frames["NFrame"].bt_navigation1.grid_forget()
        App.frames["NFrame"].bt_navigation2.configure(text="Import logs", state="disabled")
        App.frames["NFrame"].bt_navigation2.configure(command= self.import_data_cmd)
        App.frames["NFrame"].bt_navigation2.grid(row=0, column=2, padx=20, pady=10, sticky="e")

    def step_10_folderSelected(self):
        logger.debug("Widgets update step_10_folderSelected()")

        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure(1, weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)

        #Update texts and buttons
        App.frames["CSFrame"].title.configure(text="Import Logs")
        App.frames["CSFrame"].text.configure(text="Folder selected: " + str(self.dirname))
        App.frames["CSFrame"].action_bt.configure(text="Select folder")
        App.frames["CSFrame"].action_bt.grid(row=1, column=2, padx=20, pady=10, sticky="se")

        # Machine Type dropdown
        #self.mch_type_dropdown.configure(state="enabled")

        #WorkSpace: Scrollable frame
        App.frames["FilesUpload"] = CheckBoxFrame(self.right_side_panel, command=self.checkbox_frame_event,
                                                                 item_list=self.csv_files_list)
        self.show_frame("FilesUpload")

        #Update buttons
        App.frames["NFrame"].bt_navigation1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        App.frames["NFrame"].bt_navigation1.configure(text= "Clear all")
        App.frames["NFrame"].bt_navigation1.configure(command= self.back_to_selectfolder)
        if len(self.csv_files_list) > 0:
            App.frames["NFrame"].bt_navigation2.configure(state="enabled")
        else:
            App.frames["NFrame"].bt_navigation2.configure(state="disabled")
        App.frames["NFrame"].bt_navigation2.grid(row=0, column=2, padx=20, pady=10, sticky="e")
    
    def step_20_importingData(self):
        logger.debug("Widgets update step_20_importingData()")

        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure(1, weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)

        # Machine Type dropdown
        #self.mch_type_dropdown.configure(state="disabled")

        #Update texts
        App.frames["CSFrame"].title.configure(text="Importing data")
        App.frames["CSFrame"].text.configure(text="Please wait")

        #WorkSpace: Empty or Progressbar
        App.frames["PFrame"] = ProgressFrame(self.right_side_panel)
        self.show_frame("PFrame")

        #Update buttons
        App.frames["CSFrame"].action_bt.grid_forget()
        App.frames["NFrame"].bt_navigation1.grid_forget()
        App.frames["NFrame"].bt_navigation2.grid_forget()

    def step_30_dataImported(self):
        logger.debug("Widgets update step_30_dataImported()")

        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure(0, weight=0)
        App.frames["BCFrame"].grid_columnconfigure(1, weight=1)
        App.frames["BCFrame"].step1_label.configure(font=ctk.CTkFont(size=15, weight="normal"), image=App.frames["BCFrame"].step1g_img_tk)
        App.frames["BCFrame"].step2_label.configure(font=ctk.CTkFont(size=18, weight="bold"), image=App.frames["BCFrame"].step2_img_tk)

        # Machine Type dropdown
        #self.mch_type_dropdown.configure(state="disabled")

        #Update texts
        App.frames["CSFrame"].title.configure(text="Select Analysis type")
        App.frames["CSFrame"].text.configure(text="In each type you can generate plots to make your own analysis")
        App.frames["CSFrame"].action_bt.grid_forget()
        
        #WorkSpace: TabFrame
        App.frames["TFrame"] = TabsFrame(self.right_side_panel, self) # Pass the instance of App to TabsFrame
        self.show_frame("TFrame")

        #Update Buttons
        App.frames["NFrame"].bt_navigation1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        App.frames["NFrame"].bt_navigation1.configure(text= "Clear all and Go back")
        App.frames["NFrame"].bt_navigation1.configure(command= self.back_to_selectfolder)
        App.frames["NFrame"].bt_navigation2.grid_forget()

    def left_side_widgets(self, parent):
        # Left side panel / does not change during App execution
        logger.debug("Widgets update left_side_widgets()")

        # create sidebar logo
        self.logo_label = ctk.CTkLabel(parent, text="VisuaLite", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # create dropdown of machine type
        self.mt_label = ctk.CTkLabel(parent, text="Machine type:", font=ctk.CTkFont(size=16))
        self.mt_label.grid(row=1, column=0, padx=20, pady=(20, 5))
        self.mch_type = ctk.StringVar(value="FCM LPG")
        self.mch_type_dropdown = ctk.CTkOptionMenu(parent, dynamic_resizing=False, 
                                    variable=self.mch_type, values=["FCM LPG"])
        self.mch_type_dropdown.grid(row=2, column=0, padx=20, pady=0)
        self.mch_type_dropdown.set("FCM LPG")
        self.mch_type_dropdown.configure(state="disabled")

        # make middle "empty" row have the priority
        parent.grid_rowconfigure(3, weight=1)
        # Progress bar (not positioned, only declared)
        self.progress = ctk.CTkProgressBar(parent, width=100)
        self.progress.configure(mode="indeterminate")
        self.progress.start()

        #Help button
        #self.help_img = ctk.CTkImage(Image.open(os.path.join(RESOURCES, 'help1_dark.png')), size=(20, 20))
        #self.btn_help = ctk.CTkButton(parent, text="Help", image=self.help_img, font=ctk.CTkFont(size=12), height=30, width=110,
        #    compound="right", command=self.help_cmd)
        #self.btn_help.grid(row=4, column=0, padx=20, pady=10)

        # create app controls of appearance and scaling
        self.appearance_mode_label = ctk.CTkLabel(parent, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(parent, values=["Light", "Dark"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 10))
        self.appearance_mode_optionemenu.set("Dark")

        self.scaling_label = ctk.CTkLabel(parent, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(parent, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 20))
        self.scaling_optionemenu.set("100%")

    def help_cmd(self):
        logger.info("help button pressed")
        self.app2 = help_app.App()
        self.app2.mainloop()

    def __init__(self):
        super().__init__()
        logger.debug("App init")

        # configure window
        self.title("VisuaLite " + self.version + " | Data analysis for FCS Oil Modules")
        # set the dimensions of the screen 
        w = 1380 # width
        h = 900 # height

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # and where it is placed
        #Simple call of geometry: self.geometry(f"{1300}x{820}")
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.iconbitmap(APP_ICON)
        
        # Function to be executed when app is closed
        self.protocol("WM_DELETE_WINDOW", self.before_close)

        # Make right side (column 1) the main part of the App
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Left side panel
        self.left_side_panel = ctk.CTkFrame(self, corner_radius=8, width=300)
        self.left_side_panel.grid(row=0, column=0, rowspan=8, sticky="nsew", padx=(20, 10), pady=20)
        self.left_side_widgets(self.left_side_panel)

        self.grid_rowconfigure(0, weight=1)

        # Right side panel
        self.right_side_panel = ctk.CTkFrame(self, corner_radius=8)
        self.right_side_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        
        # Set right_side_panel's row and column weights to make the row2 expand to fill the available space
        self.right_side_panel.grid_rowconfigure(2, weight=1)
        self.right_side_panel.grid_columnconfigure(0, weight=1)

        #Create frames inside right side panel
        App.frames["BCFrame"] = BreadcrumbFrame(self.right_side_panel)
        App.frames["BCFrame"].grid(row=0, column=0, padx=5, pady= 5, sticky="nsew")

        App.frames["CSFrame"] = CurrentStep(self.right_side_panel)
        App.frames["CSFrame"].grid(row=1, column=0,  padx=5, pady= 5, sticky="nsew")

        App.frames["WSFrame"] = EmptyFrame(self.right_side_panel)
        App.frames["WSFrame"].grid(row=2, column=0,  padx=5, pady= 5, sticky="nsew")
        App.current = "WSFrame" # WorkSpace

        App.frames["NFrame"] = NavFrame(self.right_side_panel)
        App.frames["NFrame"].grid(row=3, column=0, padx=5, pady= 5,  sticky="nsew")

        # Init widgets
        self.step_00_init()    

        #Disclaimer
        tk.messagebox.showinfo(title='DISCLAIMER', 
            message=f'Welcome to VisuaLite {self.version}\n\nThis tool is intended for INTERNAL USE of ALFA LAVAL employees. Please note this is a BETA Version, so it is currently not supported.\n\nHappy plotting!') # type: ignore

    def before_close(self):
        # Close matplotlib figures if they exist
        if "TFrame" in self.frames:
            
            if App.frames["TFrame"].plot_fig is not None:
                App.frames["TFrame"].close_plot(App.frames["TFrame"].plot_fig,
                                                App.frames["TFrame"].plot_window)

        # Close App
        self.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        logger.debug("change_appearance_mode_event")
        logger.debug(new_appearance_mode)

        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        logger.debug("change_scaling_event")
        logger.debug(new_scaling)

        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def clear_all(self):
        # Delete memory
        logger.debug("--- Clear memory ---")
        self.dirname = None
        self.csv_files_list = []
        self.import_success = 0
        self.mch_info = None
        self.COs = None
        self.LogsStandard = pd.DataFrame()
        self.LogsAlarms = pd.DataFrame()
        self.LogsEvents = pd.DataFrame()

        # Close matplotlib figures if they exist
        if "TFrame" in self.frames:
            
            if App.frames["TFrame"].plot_fig is not None:
                App.frames["TFrame"].close_plot(App.frames["TFrame"].plot_fig,
                                                App.frames["TFrame"].plot_window)

            #if App.frames["TFrame"].preview is not None:
            #    App.frames["TFrame"].preview.destroy()

            App.frames["TFrame"].hide_progress_bar()
    
    def show_frame(self, frame_id):
        # method to change frames in position row 2, column 0 of right_side_panel
        logger.debug("show_frame")
        logger.debug(frame_id)
 
        if App.current is not None:
            App.frames[App.current].grid_forget() # Hide the current frame

        App.frames[frame_id].grid(row=2, column=0, padx=5, pady= 5, sticky="nsew") # Show the selected frame
        App.current = frame_id

    def back_to_selectfolder (self):
        logger.debug("Step1 - Back button pressed")
        
        # Clear memory and upload widgets of init
        self.clear_all()
        self.step_00_init()

    def select_folder(self):
        logger.debug("Step1 - Select folder button pressed")

        #Open file dialog to select folder
        self.sel_folder = fd.askdirectory(parent=self, title='Select a directory with log files')
        logger.debug("Selected folder:")
        logger.debug(self.sel_folder)

        if self.sel_folder != '':
            #Save selection until a new valid folder is selected
            self.dirname = self.sel_folder
            #Look for csv files in the selected folder    
            self.csv_files_list = []
            for filename in os.listdir(self.dirname):
                if filename.lower().endswith('.csv'):
                    self.csv_files_list.append(filename)

            logger.debug("Files found:")
            logger.debug(self.csv_files_list)

            #Update widgets
            self.step_10_folderSelected()
            
            #Pop up with result
            tk.messagebox.showinfo(title='Information', message=str(len(self.csv_files_list)) + ' files found in the folder selected: ' + self.dirname) # type: ignore
        else:
            logger.debug("--- no folder selected")

    def checkbox_frame_event(self):
        return self.frames['FilesUpload'].get_checked_items()
    
    def importing_data(self):
        logger.debug("...continue")

        # Call Data Analysis function and assign outputs to App variables
        try:
            self.import_success, self.LogsStandard, self.LogsAlarms = fcm_da.import_LPGdata(self.dirname, self.selected_files, self.mch_type.get())
            logger.debug(f"{self.import_success=}")

        except Exception as e:
            logger.error("--- Error importing data")
            logger.error(e, exc_info=True)
            self.import_success == 4
    
        if self.import_success == 1: #success
            self.step_30_dataImported()
            tk.messagebox.showinfo(title='Information', message='Import procedure successful!') # type: ignore

            ## Save DataFrames to .pkl for debugging 
            #import pickle 
            #self.LogsStandard.to_pickle('LogsStandard.pkl')
            #self.LogsAlarms.to_pickle('LogsAlarms.pkl')
            #self.LogsEvents.to_pickle('LogsEvents.pkl')
        
        # ERRORS
        elif self.import_success == 0: #file from another machine / file wrong columns / file name not standard
            self.step_10_folderSelected()
            tk.messagebox.showerror(title='Import failed', message='Wrong File: ' + str(self.mch_info)) # type: ignore

        elif self.import_success == 2: #no file with standard name in csv selected
            self.step_10_folderSelected()
            tk.messagebox.showerror(title='Import failed', message='Visualite could not find log files in the .csv files selected') # type: ignore

        else:
            self.step_10_folderSelected()
            tk.messagebox.showerror(title='Import failed', message='Unknown error. Please restart the application and try again') # type: ignore

    def import_data_cmd(self):
        logger.debug("Step1 - Import data started ")
        # Get names of selected files
        self.selected_files = self.checkbox_frame_event()
        logger.debug("Files selected:")
        logger.debug(self.selected_files)

        if self.selected_files == []:
            logger.debug("no files selected -> Stop")
            tk.messagebox.showerror(title='Import failed', message='Please select at least one log file') # type: ignore
            return #Stop
        else:
            # Show progressBar Frame
            self.step_20_importingData()
            logger.debug("wait 1000ms...")
            self.after(1000, self.importing_data) #wait 1000ms to show frame and next step

class TabsFrame(ctk.CTkFrame):
    # Data Analysis Frame with 3 Tabs, need to be after App 
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, **kwargs)

        logger.debug("TabsFrame init")

        # Receive all App attributes and methods
        self.app = app_instance
        self.plot_fig = None

        # Make it of the entire width and height
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Get arrays from txt file
        if not self.app.LogsStandard.empty:
            self.columns = list(fcm_da.DATA['units'].keys())
            self.columns.remove('Alarms')

        if not self.app.LogsAlarms.empty:
            self.columns.append('Alarms')

        # Get arrays of options from dataframes
        # if not self.app.LogsAlarms.empty:
        #     # Alarms for Tab2 dropdown
        #     self.alm_list = self.app.LogsAlarms['Alm_Code_Label'].unique().tolist()

        #     # Variables for Tab2 and Tab3 switches
        #     self.columns = self.columns + self.app.LogsAlarms.columns.tolist()
        #     remove_cols = ['DateTime', 'Alm_Code_Label', 'Label']
        #     for col in remove_cols:
        #         self.columns.remove(col)
        # else:
        #     self.alm_list = []
            
        # if not self.app.LogsStandard.empty:
        #     # Variables for Tab2 and Tab3
        #     self.columns = self.columns + self.app.LogsStandard.columns.tolist()

        #     # Remove columns not eligible to plot according to machine type
        #     if self.app.mch_type.get() == "FCM One | 1.5":
        #         remove_cols = ['DateTime', 'GpsPos', 'CV1_Label', 'CV2_Label', 'CV3_Label', 
        #                         'CV4_Label', 'CV5_Label', 'ChangeoverCMDchange', 'CC_Label']
        #     elif self.app.mch_type.get() == "FCM Oil 2b":
        #         remove_cols = ['DateTime', 'CV1_Label', 'CV2_Label', 'CV3_Label', 
        #                         'CV4_Label', 'STS_Label', 'ChangeoverCMDchange', 'CC_Label']
        #     for col in remove_cols:
        #         self.columns.remove(col)

        #Aux plot button
        #self.aux_plot.grid(row=0, column=1, padx=20, pady=10, sticky="ne")
        #self.label_tab_3.grid(row=0, column=0, padx=20, columnspan=2, pady=5, sticky="sw")

        #Frame for calendars
        self.frame_left_t3 = ctk.CTkFrame(self)
        self.frame_left_t3.grid(row=1, column=0, padx=(20,10), pady=10, sticky="nsew")

        #Labels and Calendars left side
        self.cal1_text = ctk.CTkLabel(self.frame_left_t3, text='From:')
        self.cal1_text.grid(row=0, column=0, padx=20, pady=2, sticky="nw") 
        # TODO: set default date to min StdLogs date, if no StdLogs then min of Alm or Eve
        self.cal1d = tkcalendar.Calendar(self.frame_left_t3, selectmode="day", date_pattern="yyyy/MM/dd")
        self.cal1d.grid(row=1, column=0, padx=(20,10), pady=2)
        self.cal1t = ctk.CTkOptionMenu(self.frame_left_t3, dynamic_resizing=False, values=TIMES)
        self.cal1t.grid(row=2, column=0, padx=20, pady=10)
        self.cal1t.set("00:00")

        self.cal1_text = ctk.CTkLabel(self.frame_left_t3, text='To:')
        self.cal1_text.grid(row=0, column=1, padx=20, pady=2, sticky="nw")
        # TODO: set default date to max StdLogs date, if no StdLogs then max of Alm or Eve
        self.cal2d = tkcalendar.Calendar(self.frame_left_t3, selectmode="day", date_pattern="yyyy/MM/dd")
        self.cal2d.grid(row=1, column=1, padx=(10,20), pady=2)
        self.cal2t = ctk.CTkOptionMenu(self.frame_left_t3, dynamic_resizing=False, values=TIMES)
        self.cal2t.grid(row=2, column=1, padx=20, pady=10)
        self.cal2t.set("00:00")

        #Information of date limits
        if not self.app.LogsStandard.empty:
            mindateS = self.app.LogsStandard['Timestamp'].min()
            maxdateS = self.app.LogsStandard['Timestamp'].max()
            s_text = '  - Standard Logs:    ' + str(mindateS) + '  ---  ' + str(maxdateS) + '\n'
        else:
            s_text = '\n'

        if not self.app.LogsAlarms.empty:
            mindateA = self.app.LogsAlarms['Timestamp'].min()
            maxdateA = self.app.LogsAlarms['Timestamp'].max()
            a_text = '  - Alarm Logs:          ' + str(mindateA) + '  ---  ' + str(maxdateA) + '\n'
        else:
            a_text = '\n'

        self.dates_info = ctk.CTkLabel(self.frame_left_t3, 
                                       text='* Be aware of date range of the logs imported:\n\n' +
                                            s_text + a_text, justify='left')
        self.dates_info.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="nw") 

        #Variables right side
        self.var_sel_t3 = ctk.CTkScrollableFrame(self)
        self.var_sel_t3.grid(row=1, column=1, padx=(10,20), pady=10, sticky="nsew")
        self.switch_list_t3 = []
        for column_name in self.columns:
            self.add_switch_t3(column_name)

        #Action button Tab3
        self.export_t3 = ctk.CTkButton(self, text="Export data",
                                         command=self.export_excel_T3)
        self.export_t3.grid(row=2, column=0, padx=10, pady=(5,10), sticky="e")
        self.plot_t3 = ctk.CTkButton(self, text="Generate and save plot",
                                         command=self.generate_personalized_plot)
        self.plot_t3.grid(row=2, column=1, padx=10, pady=(5,10), sticky="w")

    #TAB3 functions
    def show_plot(self):
        #Create aux plot if it does not exit
        if self.plot_fig is None:
            self.plot_fig = fcm_plt.create_aux_plot(self.app.LogsStandard, self.app.LogsAlarms, self.app.LogsEvents)
            
            #Create popup
            self.plot_window = ctk.CTkToplevel(self.app)
            self.plot_window.resizable(width=False, height=False)
            self.plot_window.title("Auxiliary Plot")
            # Keep the toplevel window in front of the root window
            self.plot_window.wm_transient(self.app)
            
            #Place plot in popup
            self.canvas = FigureCanvasTkAgg(self.plot_fig, master=self.plot_window)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

            # Ensure figures are closed properly when the window is closed
            self.plot_window.protocol("WM_DELETE_WINDOW", lambda: self.close_plot(self.plot_fig, self.plot_window))
        else:
            logger.debug("Plot already exists")
            return #Stop

    def close_plot(self, fig, window):
        fig.clf()  # Clear the figure
        fcm_plt.plt.close(fig)  # Close the figure
        window.destroy()  # Destroy the Toplevel window
        # Init plot
        self.plot_fig = None

    def add_switch_t3(self, label):
        # Add variable swithces 
        switch = ctk.CTkSwitch(self.var_sel_t3, text=label)
        switch.grid(row=len(self.switch_list_t3), column=0, padx=10, pady=5, sticky="w")
        self.switch_list_t3.append(switch)

    def get_selected_vars_t3(self):
        return [switch.cget("text") for switch in self.switch_list_t3 if switch.get() == 1]

    def generate_personalized_plot(self):
        logger.debug("Tab3 - PersonalizedPlot function started ---")
        self.show_progress_bar() 

        date1 = self.cal1d.get_date()
        time1 = self.cal1t.get()
        date2 = self.cal2d.get_date()
        time2 = self.cal2t.get() 

        logger.debug("User selections:")
        logger.debug(f"{date1=}, {time1=}, {date2=}, {time2=}")
        
        # Convert inputs to exact datetimes
        datetime1 = datetime.datetime(int(date1.split('/')[0]), int(date1.split('/')[1]), int(date1.split('/')[2]),
                                          int(time1.split(':')[0]), 0, 0)  # Year, month, day, hour, minute, second
        datetime2 = datetime.datetime(int(date2.split('/')[0]), int(date2.split('/')[1]), int(date2.split('/')[2]),
                                          int(time2.split(':')[0]), 0, 0)  # Year, month, day, hour, minute, second

        time_difference = datetime2 - datetime1

        # Input verification
        if (time_difference.days < 0):
            logger.debug("date range not valid -> Stop")
            tk.messagebox.showwarning(title='Incorrect dates', message='"From:" date is bigger than "To:" date') # type: ignore
            self.hide_progress_bar()
            return #Stop
        elif (time_difference.days > 5):
            logger.debug("date range bigger than 5 days -> Stop")
            tk.messagebox.showwarning(title='Date range too big', message='Please select a date range smaller than 5 days') # type: ignore
            self.hide_progress_bar()
            return #Stop
        elif time_difference.days == 0 and time_difference.seconds // 3600 == 0: #//integer division
            logger.debug("date range = 0 hours -> Stop")
            tk.messagebox.showwarning(title='Date range = 0', message='Please select a valid date range') # type: ignore
            self.hide_progress_bar()
            return #Stop
        
        cols = self.get_selected_vars_t3()
        logger.debug(f"{cols=}")

        if cols == []:
            logger.debug("no variable selected -> Stop")
            tk.messagebox.showwarning(title='No variable selected', message='Please select at least one variable to plot') # type: ignore
            return #Stop:

        # Ask user for personalized title
        self.name_file = self.get_file_name()

        # Create plot
        self.fig = fcm_plt.custom_LPGplot_divided(self.app.LogsStandard, self.app.LogsAlarms, cols, datetime1, datetime2, self.name_file)
        logger.debug("Tab3 - fig created")
        
        # Save png preview
        png_path = os.path.join(PATH, '__vl.log', 'preview.png')
        try:
            logger.debug("saving image")
            self.fig.write_image(png_path)
            logger.debug("--- png saved")
    
        except Exception as e:
            logger.error("--- Error saving file")
            logger.error(e, exc_info=True)
            tk.messagebox.showwarning(title='Error creating preview png', message="Error creating preview png") # type: ignore
            # Load an image for the popup

        # Load image file
        self.image_preview = ctk.CTkImage(Image.open(png_path), size=(700, 500))
        # Create PopUp with preview / In popup save html or abort
        self.create_preview_popup()        
        # Delete image file
        os.remove(png_path)

        self.hide_progress_bar()

    def create_preview_popup(self):
        logger.debug("creating popup")
        
        # Create a new TopLevel window for the popup
        self.preview = ctk.CTkToplevel(self.app)
        self.preview.title("Preview Plot")
        self.preview.grab_set()

        # TopLevel widgets
        self.popup_label = ctk.CTkLabel(self.preview, text="Do you want to save the following plot?", font=ctk.CTkFont(size=18))
        self.popup_label.grid(row=0, column=0, padx=10, pady=(20,10))
        self.popup_img = ctk.CTkLabel(self.preview, text="", image=self.image_preview)
        self.popup_img.grid(row=1, column=0, padx=20, pady=10)
        self.popup_btn1 = ctk.CTkButton(self.preview, text="Confirm", command= lambda: self.save_html(self.fig, self.name_file))
        self.popup_btn1.grid(row=2, column=0, padx=30, pady=(10,20), sticky="nw")
        self.popup_btn2 = ctk.CTkButton(self.preview, text="Abort", command=self.close_preview)
        self.popup_btn2.grid(row=2, column=0, padx=30, pady=(10,20), sticky="ne")

    def close_preview(self):
        self.preview.grab_release()
        self.preview.destroy()

    def save_html (self, fig, name_file):
        logger.debug("save_html started ---")
        self.show_progress_bar() 

        dest_folder = fd.askdirectory(parent=self, title='Select a destination directory')
        if dest_folder =='':
            logger.debug("no folder selected")
            tk.messagebox.showwarning(title='No folder selected', message="Figure not saved as no folder was selected.\nPlease try again.") # type: ignore
            self.hide_progress_bar()    
            self.close_preview()
            logger.debug("--- save_html finished")
            self.fig = None
            return

        logger.debug("Folder selected:")
        logger.debug(dest_folder)

        file_path = os.path.join(dest_folder, (name_file + ".html"))
        logger.debug("File to be saved:")
        logger.debug(file_path)

        try:
            fig.write_html(file_path, config={'displaylogo': False})
            logger.debug("--- save_html successful")
            tk.messagebox.showinfo(title='Plot saved!', message="Plot saved in destination folder") # type: ignore
            self.hide_progress_bar()
            self.close_preview()
            self.fig = None

        except Exception as e:
            logger.error("--- Error saving file")
            logger.error(e, exc_info=True)
            tk.messagebox.showwarning(title='Error creating html', message="Error creating figure, check permissions") # type: ignore
            self.hide_progress_bar()
            self.close_preview()
            self.fig = None

    def get_file_name(self):
        dialog = ctk.CTkInputDialog(text="Plot Title without special characters\n(Optional)", title="Plot title / File name (Optional)")
        input_text = dialog.get_input()

        if input_text is not None:
            # Check input from user
            if self.is_valid_filename(input_text):
                name_file = input_text
            else:
                #default name
                now_dt = datetime.datetime.now()
                format_dt = now_dt.strftime('%Y.%m.%d_%H%M%S')
                name_file = "Custom_Plot_{}".format(format_dt)
        else:
            #default name
            now_dt = datetime.datetime.now()
            format_dt = now_dt.strftime('%Y.%m.%d_%H%M%S')
            name_file = "Custom_Plot_{}".format(format_dt)

        return name_file

    def is_valid_filename(self, filename):
        # Define a regular expression pattern for valid filenames
        # This pattern allows letters, digits, spaces, underscores, and hyphens
        pattern = r'^[a-zA-Z0-9 _-]+$'
        """
        ^: start of the string
        [a-zA-Z0-9 _-]: defines the allowed characters in the string

        a-z: Any lowercase letter from 'a' to 'z'.
        A-Z: Any uppercase letter from 'A' to 'Z'.
        0-9: Any digit from '0' to '9'.
        _: The underscore character.
        -: The hyphen character.
        (space): A space character.
        +: This quantifier indicates that the previous character set can appear one or more times

        $: This indicates the end of the string
        """
        
        # Use re.match to check if the filename matches the pattern
        return re.match(pattern, filename) is not None

    def show_progress_bar(self):
        self.app.progress.grid(row=3, column=0, padx=10, pady=50, sticky="ew") 
    
    def hide_progress_bar(self):
        self.app.progress.grid_forget()

    def export_excel_T3(self):
        logger.debug("Tab3 - export_excel_T3 function started ---")
        self.show_progress_bar() 

        date1 = self.cal1d.get_date()
        time1 = self.cal1t.get()
        date2 = self.cal2d.get_date()
        time2 = self.cal2t.get() 

        logger.debug("User selections:")
        logger.debug(f"{date1=}, {time1=}, {date2=}, {time2=}")
        
        # Convert inputs to exact datetimes
        datetime1 = datetime.datetime(int(date1.split('/')[0]), int(date1.split('/')[1]), int(date1.split('/')[2]),
                                          int(time1.split(':')[0]), 0, 0)  # Year, month, day, hour, minute, second
        datetime2 = datetime.datetime(int(date2.split('/')[0]), int(date2.split('/')[1]), int(date2.split('/')[2]),
                                          int(time2.split(':')[0]), 0, 0)  # Year, month, day, hour, minute, second

        time_difference = datetime2 - datetime1

        # Input verification
        if (time_difference.days < 0):
            logger.debug("date range not valid -> Stop")
            tk.messagebox.showwarning(title='Incorrect dates', message='"From:" date is bigger than "To:" date') # type: ignore
            self.hide_progress_bar()
            return #Stop
        elif (time_difference.days > 5):
            logger.debug("date range bigger than 5 days -> Stop")
            tk.messagebox.showwarning(title='Date range too big', message='Please select a date range smaller than 5 days') # type: ignore
            self.hide_progress_bar()
            return #Stop
        elif time_difference.days == 0 and time_difference.seconds // 3600 == 0: #//integer division
            logger.debug("date range = 0 hours -> Stop")
            tk.messagebox.showwarning(title='Date range = 0', message='Please select a valid date range') # type: ignore
            self.hide_progress_bar()
            return #Stop
        
        cols = self.get_selected_vars_t3()
        logger.debug(f"{cols=}")

        if cols == []:
            logger.debug("no variable selected -> Stop")
            tk.messagebox.showwarning(title='No variable selected', message='Please select at least one variable to plot') # type: ignore
            return #Stop:

        # Current datetime to create personalized file name
        now_dt = datetime.datetime.now()
        format_dt = now_dt.strftime('%Y.%m.%d_%H%M%S')
        name_file="Filtered_Logs_{}".format(format_dt)

        # Filter DFs and save excel
        self.export_excel(
            dfs = [self.app.LogsStandard, self.app.LogsAlarms, self.app.LogsEvents],
            sheetNames = ['Standard', 'Alarms', 'Events'],
            date1 = datetime1, date2 = datetime2,
            cols = cols,
            fileName = name_file)

        self.hide_progress_bar()

    def export_excel(self, dfs, sheetNames, date1, date2, cols, fileName):
        logger.debug('export_excel started ---')

        dest_folder = fd.askdirectory(parent=self, title='Select a destination directory')
        if dest_folder =='':
            logger.debug("no folder selected")
            tk.messagebox.showwarning(title='No folder selected', message="File not saved as no folder was selected.\nPlease try again.") # type: ignore
            self.hide_progress_bar()
            logger.debug("--- export_excel finished")
            return

        logger.debug("Folder selected:")
        logger.debug(dest_folder)

        file_path = os.path.join(dest_folder, (fileName + ".xlsx"))
        logger.debug("File to be saved:")
        logger.debug(file_path)

        try:
            with pd.ExcelWriter(file_path) as writer:  
                for i, df in enumerate(dfs):
                    if not df.empty:
                        logger.debug(i)
                        logger.debug(sheetNames[i])

                        df_export = df[(df['Timestamp'] >= date1) & (df['Timestamp'] <= date2)]

                        if 'AlarmNumber' in cols:
                            cols.remove('AlarmNumber')
                        if 'EventNumber' in cols:
                            cols.remove('EventNumber')

                        if set(cols).issubset(df_export.columns.tolist()):
                            cols.insert(0, 'Timestamp')
                            df_export = df_export[cols]
                        elif 'Evn_Code_Label' in df_export.columns.tolist():
                            del df_export['Evn_Code_Label']
                        elif 'Alm_Code_Label' in df_export.columns.tolist():
                            del df_export['Alm_Code_Label']

                        df_export.to_excel(writer, sheet_name=sheetNames[i], index=False)

                    else:
                        logger.debug('df empty')
            
            tk.messagebox.showinfo(title='Excel File saved!', message="Excel file saved in destination folder") # type: ignore
            logger.debug('--- export_excel finished')

        except Exception as e:
            logger.error("--- Error saving excel file")
            logger.error(e, exc_info=True)
            tk.messagebox.showwarning(title='Error creating excel file', message="Error creating excel file, check permissions") # type: ignore
            self.hide_progress_bar()

