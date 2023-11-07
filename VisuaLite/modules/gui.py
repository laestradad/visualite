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

VERSION = "V0.00.04"
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
ctk.set_default_color_theme("dark-blue")

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
        self.mch_type_dropdown.configure(state="enabled")

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
        self.mch_type_dropdown.configure(state="enabled")

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
        self.mch_type_dropdown.configure(state="disabled")

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
        self.mch_type_dropdown.configure(state="disabled")

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
        self.mch_type = ctk.StringVar(value="FCM One | 1.5")
        self.mch_type_dropdown = ctk.CTkOptionMenu(parent, dynamic_resizing=False, 
                                    variable=self.mch_type, values=["FCM One | 1.5", "FCM Oil 2b"])
        self.mch_type_dropdown.grid(row=2, column=0, padx=20, pady=0)
        self.mch_type_dropdown.set("FCM One | 1.5")

        # make middle "empty" row have the priority
        parent.grid_rowconfigure(3, weight=1)
        # Progress bar (not positioned, only declared)
        self.progress = ctk.CTkProgressBar(parent, width=100)
        self.progress.configure(mode="indeterminate")
        self.progress.start()

        #Help button
        self.help_img = ctk.CTkImage(Image.open(os.path.join(RESOURCES, 'help1_dark.png')), size=(20, 20))
        self.btn_help = ctk.CTkButton(parent, text="Help", image=self.help_img, font=ctk.CTkFont(size=12), height=30, width=110,
            compound="right", command=self.help_cmd)
        self.btn_help.grid(row=4, column=0, padx=20, pady=10)

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
        self.title("VisuaLite " + self.version)
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
            if App.frames["TFrame"].fig1 is not None:
                App.frames["TFrame"].clear_co_preview(App.frames["TFrame"].fig1)
            
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
            if App.frames["TFrame"].fig1 is not None:
                App.frames["TFrame"].clear_co_preview(App.frames["TFrame"].fig1)
            
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
            self.import_success, self.mch_info, self.COs,self.LogsStandard, self.LogsAlarms, self.LogsEvents = fcm_da.import_data(self.dirname, self.selected_files, self.mch_type.get())
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

        # Make it of the entire width and height
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create tabview
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        #-----------------------------------TAB1
        logger.debug("tab1 init")

        self.tabview.add("Change Overs")
        self.tabview.tab("Change Overs").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Change Overs").grid_columnconfigure(0, minsize=480)
        self.tabview.tab("Change Overs").grid_rowconfigure(0, weight=1)

        #Frame for plot preview
        self.co_preview = ctk.CTkFrame(self.tabview.tab("Change Overs"))
        self.co_preview.grid(row=0, column=0, padx=(20,10), pady=20, sticky = 'nsew')
        self.co_preview.grid_columnconfigure(0, weight=1)
        self.co_preview.grid_rowconfigure(1, weight=1)

        #Option menu with CO options
        self.co_sel = ctk.StringVar(value="")
        self.preview_options = ctk.CTkOptionMenu(self.co_preview, dynamic_resizing=False, variable=self.co_sel,
                                                 command=self.preview_co)
        self.preview_options.grid(row=0, column=0, padx=20, pady=(20,10), sticky="w")
        self.preview_options.set("Changeover #")

        #Button to clear preview
        self.clear_btn = ctk.CTkButton(self.co_preview, text="Clear", command= lambda: self.clear_co_preview(self.fig1))
        self.clear_btn.grid(row=0, column=1, padx=20, pady=(20,10), sticky="w")

        #Plot declaration
        self.fig1 = None
        #Dummy img of plot
        dummy_plot_dark = os.path.join(RESOURCES, 'dark_co_preview.png')
        dummy_plot_light = os.path.join(RESOURCES, 'light_co_preview.png')
        self.dummy_plot_tk = ctk.CTkImage(light_image=Image.open(dummy_plot_light),
                                          dark_image=Image.open(dummy_plot_dark),
                                          size=(500, 375))
        self.dummy_plot = ctk.CTkLabel(self.co_preview, text="", image=self.dummy_plot_tk)
        self.dummy_plot.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=10)

        #Frame with list of Change overs
        self.results_t1 = ctk.CTkScrollableFrame(self.tabview.tab("Change Overs"))
        self.results_t1.grid(row=0, column=1, padx=(10,20), pady=20, sticky = 'nsew')

        #Text before COs
        self.label1 = ctk.CTkLabel(self.results_t1) #text defined later if COs founded
        self.label1.grid(row=0, column=0, padx=20, pady=20, sticky = 'nw')

        #Declaration of buttons
        self.plot_sel = ctk.CTkButton(self.results_t1, text="Save plot", command= self.plot_sel_COs)
        self.plot_all = ctk.CTkButton(self.results_t1, text="Export data", command= self.export_excel_T1)
        self.plot_type = ctk.StringVar(value="")
        self.plot_type_tk = ctk.CTkOptionMenu(self.results_t1, dynamic_resizing=False, variable=self.plot_type, 
                                            values=["Overlap","Separate"])
        self.plot_type_tk.set("Separate")
        
        self.COs = []
        if self.app.COs:  
            self.COs = self.app.COs

            #If Changeovers detected, create widgets
            self.co_list = [] #list of radiobuttons for each Changeover#
            self.cos_options = [] #list of strings with Changeover#
            self.label1.configure(text="In the logs imported there are " + str(len(self.COs)) + " changeovers.")
            
            # Add radiobuttons for each Changeover
            self.sel_co = tk.IntVar(value=0)
            for i, CO in enumerate(self.COs):
                text= str(i+1) + '. From ' + str(CO['Start']) + ' to ' + str(CO['Finish']) + '. Duration: ' + str(CO['Duration'])
                self.add_co_radiobtn(text, i+1)
                self.cos_options.append("Changeover "+ str(i+1))

            self.preview_options.configure(values=self.cos_options)
            self.plot_type_tk.grid(row=len(self.co_list)+2, column=0, padx=10, pady=10, sticky="w")
            self.plot_sel.grid(row=len(self.co_list)+2, column=0, padx=10, pady=10)
            self.plot_all.grid(row=len(self.co_list)+2, column=0, padx=10, pady=10, sticky="e")
        
        else:
            #Disable widgets if no ChangeOvers detected
            self.label1.configure(text="No Change Overs detected in data inserted")
            self.preview_options.configure(state="disabled")
            self.clear_btn.configure(state="disabled")

        #-----------------------------------TAB2
        logger.debug("tab2 init")

        self.tabview.add("Search Event/Alarm")
        self.tabview.tab("Search Event/Alarm").grid_rowconfigure(2, weight=1)
        self.tabview.tab("Search Event/Alarm").grid_columnconfigure((0,1,2,3,4), weight=0)
        self.tabview.tab("Search Event/Alarm").grid_columnconfigure(5, weight=1)

        # Get arrays of options from dataframes
        self.columns = []
        if not self.app.LogsAlarms.empty:
            # Alarms for Tab2 dropdown
            self.alm_list = self.app.LogsAlarms['Alm_Code_Label'].unique().tolist()

            # Variables for Tab2 and Tab3 switches
            self.columns = self.columns + self.app.LogsAlarms.columns.tolist()
            remove_cols = ['DateTime', 'Alm_Code_Label', 'Label']
            for col in remove_cols:
                self.columns.remove(col)
        else:
            self.alm_list = []

        if not self.app.LogsEvents.empty:
            # Events for Tab2 dropdown
            self.eve_list = self.app.LogsEvents['Evn_Code_Label'].unique().tolist()
            
            # Variables for Tab2 and Tab3 switches
            self.columns = self.columns + self.app.LogsEvents.columns.tolist()
            remove_cols = ['DateTime', 'Evn_Code_Label', 'Label', 'Data', 'GpsPos']
            for col in remove_cols:
                self.columns.remove(col)
        else:
            self.eve_list = []

        if not self.app.LogsStandard.empty:
            # Variables for Tab2 and Tab3
            self.columns = self.columns + self.app.LogsStandard.columns.tolist()

            # Remove columns not eligible to plot according to machine type
            if self.app.mch_type.get() == "FCM One | 1.5":
                remove_cols = ['DateTime', 'GpsPos', 'CV1_Label', 'CV2_Label', 'CV3_Label', 
                                'CV4_Label', 'CV5_Label', 'ChangeoverCMDchange', 'CC_Label']
            elif self.app.mch_type.get() == "FCM Oil 2b":
                remove_cols = ['DateTime', 'CV1_Label', 'CV2_Label', 'CV3_Label', 
                                'CV4_Label', 'STS_Label', 'ChangeoverCMDchange', 'CC_Label']
            for col in remove_cols:
                self.columns.remove(col)

        # Label tab2
        self.label2 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"),
                                   text="Please select an event or alarm, and generate a customized plot around the selected occurence.")
        self.label2.grid(row=0, column=0, columnspan=5, padx=20, pady=5, sticky="nw")

        # Radio buttons to select Alarm or Event
        self.sel_ae = tk.IntVar(value=0)
        self.radio_button_1 = ctk.CTkRadioButton(self.tabview.tab("Search Event/Alarm"), variable=self.sel_ae,
                                                            text="Alarm" ,value=0, command=self.update_optionmenu)
        self.radio_button_1.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        self.radio_button_2 = ctk.CTkRadioButton(self.tabview.tab("Search Event/Alarm"), variable=self.sel_ae, 
                                                            text="Event" , value=1, command=self.update_optionmenu)
        self.radio_button_2.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        # Dropdown
        self.search_var = ctk.StringVar(value="")
        self.optionmenu_1 = ctk.CTkOptionMenu(self.tabview.tab("Search Event/Alarm"), dynamic_resizing=False, 
                                                                                            variable=self.search_var)
        self.optionmenu_1.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
        self.update_optionmenu()

        # Search Button
        self.search_bt = ctk.CTkButton(self.tabview.tab("Search Event/Alarm"), text="Search", command=self.searchAE)
        self.search_bt.grid(row=1, column=4, padx=(5,10), pady=5, sticky="w")

        # Variable Selection
        self.label3 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="Variable list",
                                                                            font=ctk.CTkFont(weight="bold"))
        self.label3.grid(row=1, column=5, padx=20, pady=5, sticky="w")
        self.var_sel = ctk.CTkScrollableFrame(self.tabview.tab("Search Event/Alarm"))
        self.var_sel.grid(row=2, column=5, padx=(10,20), pady=5, sticky="nsew")
        self.switch_list_t2 = []
        for column_name in self.columns:
            self.add_switch_t2(column_name)

        # Aux plot
        self.aux_plot2 = ctk.CTkButton(self.tabview.tab("Search Event/Alarm"), text="Show Auxiliary Plot", 
                                        command=self.show_plot)
        self.aux_plot2.grid(row=1, column=5, padx=20, pady=10, sticky="ne")

        # Search results
        self.radiobtn_list = []
        self.results_t2 = ctk.CTkScrollableFrame(self.tabview.tab("Search Event/Alarm"))
        self.results_t2.grid(row=2, column=0, columnspan=5, padx=(20,10), pady=5, sticky="nsew")
        self.label_results_t2 = ctk.CTkLabel(self.results_t2, text="Search results shown here.")
        self.label_results_t2.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        #Dropdowns and Labels for time interval
        self.label6 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), 
                                text="Please select the time before/after the selected alarm/event to generate your report")
        self.label6.grid(row=3, column=0, columnspan=5, padx=20, pady=5, sticky="nw")

        self.low_limit = ctk.StringVar(value="")
        self.label4 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="Time before: ")
        self.label4.grid(row=4, column=0, padx=5, pady=(5,20), sticky="e")
        self.optionmenu_2 = ctk.CTkOptionMenu(self.tabview.tab("Search Event/Alarm"), dynamic_resizing=False, 
                                    variable=self.low_limit, values=["1 hour", "2 hours", "4 hours", "8 hours", "1 day"])
        self.optionmenu_2.grid(row=4, column=1, padx=5, pady=(5,20), sticky="ew")
        self.optionmenu_2.set("Select")

        self.high_limit = ctk.StringVar(value="")
        self.label5 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="Time after: ")
        self.label5.grid(row=4, column=2, padx=5, pady=(5,20), sticky="e")
        self.optionmenu_3 = ctk.CTkOptionMenu(self.tabview.tab("Search Event/Alarm"), dynamic_resizing=False, 
                                    variable=self.high_limit, values=["1 hour", "2 hours", "4 hours", "8 hours", "1 day"])
        self.optionmenu_3.grid(row=4, column=3, padx=5, pady=(5,20), sticky="ew")
        self.optionmenu_3.set("Select")

        #Plot Button
        self.plot_t2 = ctk.CTkButton(self.tabview.tab("Search Event/Alarm"), text="Generate and save plot",
                                        command=self.generate_search_ae_plot)
        self.plot_t2.grid(row=4, column=5, padx=(5,20), pady=(5,20), sticky="e")
        self.plot_t2.configure(state="disabled")
        
        #Export Button
        self.export_t2 = ctk.CTkButton(self.tabview.tab("Search Event/Alarm"), text="Export data",
                                        command=self.export_excel_T2)
        self.export_t2.grid(row=4, column=5, padx=(5,20), pady=(5,20), sticky="w")
        self.export_t2.configure(state="disabled")

        # Enable or disable buttons based on alarms/events not imported
        if (not self.alm_list) and (not self.eve_list):
            self.search_bt.configure(state="disabled")
            self.radio_button_1.configure(state="disabled")
            self.radio_button_2.configure(state="disabled")
            self.label_results_t2.configure(text="Funtion not available. Please import Alarm or Event logs")
        
        if (not self.alm_list) and (self.eve_list):
            self.sel_ae.set(1)
            self.radio_button_1.configure(state="disabled")
            self.label_results_t2.configure(text="Search results shown here.\nAlarm logs not imported", justify='left')

        if (not self.eve_list) and (self.alm_list):
            self.sel_ae.set(0)
            self.radio_button_2.configure(state="disabled")
            self.label_results_t2.configure(text="Search results shown here.\nEvent logs not imported", justify='left')

        #-----------------------------------TAB3
        logger.debug("tab3 init")

        self.tabview.add("Personalized Analysis")
        self.tabview.tab("Personalized Analysis").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Personalized Analysis").grid_rowconfigure(1, weight=1)

        #Aux plot button
        self.plot_fig = None
        self.aux_plot = ctk.CTkButton(self.tabview.tab("Personalized Analysis"), text="Show Auxiliary Plot", 
                                        command=self.show_plot)
        self.aux_plot.grid(row=0, column=1, padx=20, pady=10, sticky="ne")
        self.label_tab_3 = ctk.CTkLabel(self.tabview.tab("Personalized Analysis"), text="Select the desired time interval and variables you want to plot:")
        self.label_tab_3.grid(row=0, column=0, padx=20, columnspan=2, pady=5, sticky="sw")

        #Frame for calendars
        self.frame_left_t3 = ctk.CTkFrame(self.tabview.tab("Personalized Analysis"))
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
            mindateS = self.app.LogsStandard['DateTime'].min()
            maxdateS = self.app.LogsStandard['DateTime'].max()
            s_text = '  - Standard Logs:    ' + str(mindateS) + '  ---  ' + str(maxdateS) + '\n'
        else:
            s_text = '\n'

        if not self.app.LogsAlarms.empty:
            mindateA = self.app.LogsAlarms['DateTime'].min()
            maxdateA = self.app.LogsAlarms['DateTime'].max()
            a_text = '  - Alarm Logs:          ' + str(mindateA) + '  ---  ' + str(maxdateA) + '\n'
        else:
            a_text = '\n'

        if not self.app.LogsEvents.empty:
            mindateE = self.app.LogsEvents['DateTime'].min()
            maxdateE = self.app.LogsEvents['DateTime'].max()
            e_text = '  - Event Logs:           ' + str(mindateE) + '  ---  ' + str(maxdateE) + '\n\n'
        else:
            e_text = '\n\n'

        self.dates_info = ctk.CTkLabel(self.frame_left_t3, 
                                       text='* Be aware of date range of the logs imported:\n\n' +
                                            s_text + a_text + e_text +
                                            'For more details, use Auxiliary Plot (top right button)',
                                       justify='left')
        self.dates_info.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="nw") 

        #Variables right side
        self.var_sel_t3 = ctk.CTkScrollableFrame(self.tabview.tab("Personalized Analysis"))
        self.var_sel_t3.grid(row=1, column=1, padx=(10,20), pady=10, sticky="nsew")
        self.switch_list_t3 = []
        for column_name in self.columns:
            self.add_switch_t3(column_name)

        #Action button Tab3
        self.export_t3 = ctk.CTkButton(self.tabview.tab("Personalized Analysis"), text="Export data",
                                         command=self.export_excel_T3)
        self.export_t3.grid(row=2, column=0, padx=10, pady=(5,10), sticky="e")
        self.plot_t3 = ctk.CTkButton(self.tabview.tab("Personalized Analysis"), text="Generate and save plot",
                                         command=self.generate_personalized_plot)
        self.plot_t3.grid(row=2, column=1, padx=10, pady=(5,10), sticky="w")

    #TAB1 functions
    def add_co_radiobtn(self, item, i):
        radiobutton = ctk.CTkRadioButton(self.results_t1, variable=self.sel_co, text=item, value=i)
        radiobutton.grid(row=len(self.co_list)+1, column=0, padx=5, pady=10, sticky="w")
        self.co_list.append(radiobutton)

    def export_excel_T1(self):
        logger.debug("Tab1 - export_excel_T1 started ---")
        self.show_progress_bar()

        index = self.sel_co.get()
        logger.debug("selected item:")
        logger.debug(index)

        if index == 0:
            logger.debug("--- no option selected -> Stop")
            tk.messagebox.showwarning(title='No option selected!', message='Select one ChangeOver to plot') # type: ignore
            self.hide_progress_bar()
            return #Stop
        
        df = fcm_da.ChangeOverToDF(self.app.COs[index-1], self.app.LogsStandard)
        all_co_cols = [col for category in fcm_da.DATA['change_over_vars'].values() for col in category]

        self.name_file = "CO"+ str(index) + "_" + str(self.app.COs[index-1]['Start'].date())

        # Filter DFs and save excel
        self.export_excel(
            dfs = [df, self.app.LogsAlarms, self.app.LogsEvents],
            sheetNames = ['Standard', 'Alarms', 'Events'],
            date1 = df['DateTime'].min(), date2 = df['DateTime'].max(),
            cols = all_co_cols,
            fileName = self.name_file)

        self.hide_progress_bar()
        logger.debug("--- Tab1 - export_excel_T1 finished")

    def plot_sel_COs(self):
        logger.debug("Tab1 - plot_sel_COs started ---")
        self.show_progress_bar()

        index = self.sel_co.get()
        logger.debug("selected item:")
        logger.debug(index)

        if index == 0:
            logger.debug("--- no option selected -> Stop")
            tk.messagebox.showwarning(title='No option selected!', message='Select one ChangeOver to plot') # type: ignore
            self.hide_progress_bar()
            return #Stop
        
        dest_folder =''
        dest_folder = fd.askdirectory(parent=self, title='Select a destination directory')
        logger.debug("Selected folder:")
        logger.debug(dest_folder)

        if dest_folder == '': #no folder selected
            logger.debug("no folder selected -> Stop")
            self.hide_progress_bar()
            return #Stop

        plot_type = self.plot_type.get()
        logger.debug(f"{plot_type=}")

        df = fcm_da.ChangeOverToDF(self.app.COs[index-1], self.app.LogsStandard)
        
        #Plot Type
        if plot_type == "Overlap":
            fig = fcm_plt.change_over_overlap(df, self.app.LogsAlarms, self.app.LogsEvents, self.app.mch_info)
            name_file= "ov_CO"+ str(index) + "_" + str(self.app.COs[index-1]['Start'].date()) + ".html"

        elif plot_type == "Separate":
            fig = fcm_plt.change_over_divided(df, self.app.LogsAlarms, self.app.LogsEvents, self.app.mch_info)
            name_file= "sp_CO"+ str(index) + "_" + str(self.app.COs[index-1]['Start'].date()) + ".html"

        file_path = os.path.join(dest_folder, name_file)
        logger.debug("File to save:")
        logger.debug(file_path)
        try:
            fig.write_html(file_path, config={'displaylogo': False})
            logger.debug("File saved successfully.")
            tk.messagebox.showinfo(title='Plot saved!', message="Plot saved in destination folder") # type: ignore

        except Exception as e:
            logger.error("--- Error saving file")
            logger.error(e, exc_info=True)
            tk.messagebox.showinfo(title='Error saving html file', message="Some error may have occured saving the plot.") # type: ignore

        self.hide_progress_bar()
        logger.debug("--- Tab1 - plot_sel_COs finished")

    def preview_co(self, CO):
        logger.debug("preview_co started ---")

        #If callback from optionmenu, value is passed as argument
        #CO = self.co_sel.get()
        
        if CO == "Changeover #": #defult value of dropdown
            logger.debug("no changeover selected -> Stop")
            return #Stop

        else:
            if self.fig1 is not None:
                self.clear_co_preview(self.fig1) #close fig if there is another plot

            self.dummy_plot.grid_forget() #close dummy img

            i = int(CO[-1]) #last character of string in options menu to get index of Changeover
            
            # Create plot
            self.fig1 = fcm_plt.change_over_preview(fcm_da.ChangeOverToDF(self.app.COs[i-1], self.app.LogsStandard))

            # Show plot in App
            self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.co_preview)
            self.canvas1.draw()
            self.canvas1.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=10)
        
        logger.debug("--- preview_co finished")

    def clear_co_preview(self, fig):
        logger.debug("clear_co_preview started ---")

        fig.clf()  # Clear the figure
        fcm_plt.plt.close(fig)  # Close the figure
        self.canvas1.get_tk_widget().grid_forget()

        #Show dummy plot
        self.dummy_plot.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=10)

        # init fig
        self.fig1 = None
        logger.debug("--- clear_co_preview finished")

    #TAB2 functions
    def update_optionmenu(self): 
        # Change options in optionmenu if Radio button choice change
        if self.sel_ae.get() == 0:
            logger.debug("Tab2 - Alarm radiobutton selected")
            self.optionmenu_1.configure(values=self.alm_list)
        elif self.sel_ae.get() == 1:
            logger.debug("Tab2 - Event radiobutton selected")
            self.optionmenu_1.configure(values=self.eve_list)

        # Set default value
        self.optionmenu_1.set("Search value")

    def searchAE(self):
        logger.debug("Tab2 - Search function started ---")
        if self.search_var.get() == "Search value":
            logger.debug("deafault 'Search Value' selected -> Stop")
            tk.messagebox.showwarning(title='No option selected!', message='Select an Alarm o Event to search') # type: ignore
            return #Stop
        else:
            self.plot_t2.configure(state="enabled")
            self.export_t2.configure(state="enabled")

            selected_item = self.search_var.get()
            logger.debug("%s selected", selected_item)

            self.ae_number= int(selected_item[1:selected_item.index('_')]) 
            #text.index('_') returns position of _ char / or int(text.split('_')[0][1:]) this function splits string by _
            
            self.timestamps = []
            if selected_item[0] == 'A':
                logger.debug("Searching for AlarmNumber %s", self.ae_number)
                self.timestamps = self.app.LogsAlarms[self.app.LogsAlarms['AlarmNumber'] == self.ae_number]['DateTime'].tolist()
                
            elif selected_item[0] == 'E':
                logger.debug("Searching for EventNumber %s", self.ae_number)
                self.timestamps = self.app.LogsEvents[self.app.LogsEvents['EventNumber'] == self.ae_number]['DateTime'].tolist()
            
            logger.debug("Search results:")
            logger.debug(self.timestamps)
            
            logger.debug("Creating results' widgets")
            self.result_selection = tk.IntVar(value=0)
            if self.timestamps:

                # Clean previous results
                if self.radiobtn_list:
                    for radiobtn in self.radiobtn_list:
                        radiobtn.grid_forget()
                    self.radiobtn_list = []

                self.label_results_t2.configure(text="In the imported logs there are " + str(len(self.timestamps)) + " occurrences of " + selected_item + "." +
                                                "\n\nPlease select the occurence you want to plot:", justify='left')
                
                for i, t in enumerate(self.timestamps):
                    text= str(i+1) + ". " + str(t.date()) + " at " + str(t.time())
                    self.add_radiobtn_t2(text, i)
            
            logger.debug("--- Results' widgets created")
            tk.messagebox.showinfo(title='Search results', message="Found " + str(len(self.timestamps)) + " occurrences of " + selected_item) # type: ignore

    def add_radiobtn_t2(self, item, i):
        # Occurences of search, radiobutton because user can only choose one
        radiobtn = ctk.CTkRadioButton(self.results_t2, text=item, variable=self.result_selection, value=i)
        radiobtn.grid(row=len(self.radiobtn_list)+1, column=0, padx=15, pady=5, sticky="w")
        self.radiobtn_list.append(radiobtn)

    def add_switch_t2(self, label):
        # Loop to add variables switches
        switch = ctk.CTkSwitch(self.var_sel, text=label)
        switch.grid(row=len(self.switch_list_t2), column=0, padx=10, pady=5, sticky="w")
        self.switch_list_t2.append(switch)

    def get_selected_vars_t2(self):
        return [switch.cget("text") for switch in self.switch_list_t2 if switch.get() == 1]

    def generate_search_ae_plot (self):
        logger.debug("Tab2 - Generation search_AE plot started ---")
        self.show_progress_bar() 

        logger.debug("Limits selected:")
        logger.debug(self.high_limit.get())
        logger.debug(self.low_limit.get())

        if (self.high_limit.get() == "Select") or (self.low_limit.get()== "Select"):
            tk.messagebox.showwarning(title='No option selected!', message='Select time boundaries for the report') # type: ignore
            logger.debug("default values selected -> Stop")
            self.hide_progress_bar()
            return #Stop
        
        # from "1hour" type input to exact datetime
        date1, date2 = fcm_da.date_limits(self.timestamps[self.result_selection.get()],self.low_limit.get(), self.high_limit.get())
        logger.debug("Dates to filter:")
        logger.debug(f"{date1=}, {date2=}")
        
        cols = self.get_selected_vars_t2()
        logger.debug("Variables selected:")
        logger.debug(cols)
        if cols == []:
            logger.debug("no variable selected -> Stop")
            tk.messagebox.showwarning(title='No variable selected', message='Please select at least one variable to plot') # type: ignore
            self.hide_progress_bar()
            return #Stop:

        # Current datetime to create personalized file name
        now_dt = datetime.datetime.now()
        format_dt = now_dt.strftime('%Y.%m.%d_%H%M%S')
        
        self.name_file = ""
        if self.sel_ae.get() == 0:
            self.name_file="Custom_Plot_A{}_{}".format(self.ae_number, format_dt)
        elif self.sel_ae.get() == 1:
            self.name_file="Custom_Plot_E{}_{}".format(self.ae_number, format_dt)

        #Create plot
        self.fig = fcm_plt.custom_plot_divided(self.app.LogsStandard, self.app.LogsAlarms, self.app.LogsEvents, cols, date1, date2, self.name_file)
        logger.debug("Tab2 - fig created")

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

    def export_excel_T2(self):
        logger.debug("Tab2 - export_excel_T2 plot started ---")
        self.show_progress_bar() 

        logger.debug("Limits selected:")
        logger.debug(self.high_limit.get())
        logger.debug(self.low_limit.get())

        if (self.high_limit.get() == "Select") or (self.low_limit.get()== "Select"):
            tk.messagebox.showwarning(title='No option selected!', message='Select time boundaries for the report') # type: ignore
            logger.debug("default values selected -> Stop")
            self.hide_progress_bar()
            return #Stop
        
        # from "1hour" type input to exact datetime
        date1, date2 = fcm_da.date_limits(self.timestamps[self.result_selection.get()],self.low_limit.get(), self.high_limit.get())
        logger.debug("Dates to filter:")
        logger.debug(f"{date1=}, {date2=}")
        
        cols = self.get_selected_vars_t2()
        logger.debug("Variables selected:")
        logger.debug(cols)
        if cols == []:
            logger.debug("no variable selected -> Stop")
            tk.messagebox.showwarning(title='No variable selected', message='Please select at least one variable to plot') # type: ignore
            self.hide_progress_bar()
            return #Stop:

        # Current datetime to create personalized file name
        now_dt = datetime.datetime.now()
        format_dt = now_dt.strftime('%Y.%m.%d_%H%M%S')
        
        self.name_file = ""
        if self.sel_ae.get() == 0:
            self.name_file="Filtered_Logs_A{}_{}".format(self.ae_number, format_dt)
        elif self.sel_ae.get() == 1:
            self.name_file="Filtered_Logs_E{}_{}".format(self.ae_number, format_dt)

        # Filter DFs and save excel
        self.export_excel(
            dfs = [self.app.LogsStandard, self.app.LogsAlarms, self.app.LogsEvents],
            sheetNames = ['Standard', 'Alarms', 'Events'],
            date1 = date1, date2 = date2,
            cols = cols,
            fileName = self.name_file)

        self.hide_progress_bar()

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
        self.fig = fcm_plt.custom_plot_divided(self.app.LogsStandard, self.app.LogsAlarms, self.app.LogsEvents, cols, datetime1, datetime2, self.name_file)
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

                        df_export = df[(df['DateTime'] >= date1) & (df['DateTime'] <= date2)]

                        if 'AlarmNumber' in cols:
                            cols.remove('AlarmNumber')
                        if 'EventNumber' in cols:
                            cols.remove('EventNumber')

                        if set(cols).issubset(df_export.columns.tolist()):
                            cols.insert(0, 'DateTime')
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

