import tkinter as tk
import customtkinter as ctk
import tkinter.filedialog as fd
from PIL import Image
import os

from modules import fcm_one as fcm 
# use fcm.bla bla to use data analysis functions

PATH = os.getcwd()
print(PATH)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
    
class BreadcrumbFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Load the images 1, 2, 3
        image1_path = os.path.join(PATH, "number-1.png")
        self.step1_img = Image.open(image1_path).resize((30, 30))
        self.step1_img_tk = ctk.CTkImage(self.step1_img)

        image2_path = os.path.join(PATH, "number-2.png")
        self.step2_img = Image.open(image2_path).resize((30, 30))
        self.step2_img_tk = ctk.CTkImage(self.step2_img)

        image3_path = os.path.join(PATH, "number-3.png")
        self.step3_img = Image.open(image3_path).resize((30, 30))
        self.step3_img_tk = ctk.CTkImage(self.step3_img)

        # STEP 1
        self.step1 = ctk.CTkFrame(self)
        self.step1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.step1_label = ctk.CTkLabel(self.step1, text="   Import Logs", image=self.step1_img_tk,
                                         compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.step1_label.grid(row=0, column=0, padx=20, pady=10)

        # STEP 2
        self.step2 = ctk.CTkFrame(self)
        self.step2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.step2_label = ctk.CTkLabel(self.step2, text="   Analysis Type", image=self.step2_img_tk,
                                         compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.step2_label.grid(row=0, column=0, padx=20, pady=10)

        # STEP 3
        self.step3 = ctk.CTkFrame(self)
        self.step3.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.step3_label = ctk.CTkLabel(self.step3, text="   Results", image=self.step3_img_tk,
                                         compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.step3_label.grid(row=0, column=0, padx=20, pady=10)

        #configure grid
        self.grid_rowconfigure(0, weight=1)
    
class CurrentStep(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create Title and command row
        self.title = ctk.CTkLabel(self, fg_color="transparent", font=ctk.CTkFont(size=22, weight="bold"), anchor="nw")
        self.title.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
        # create label with explanation
        self.text = ctk.CTkLabel(self, fg_color="transparent", font=ctk.CTkFont(size=12), anchor="nw")
        self.text.grid(row=1, column=0, padx=25, pady=10, sticky="nw")
        # action button
        self.action_bt = ctk.CTkButton(self)
        self.action_bt.grid(row=1, column=2, padx=20, pady=10, sticky="se")

        # Set row and column weights to make it take the entire space
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

class EmptyFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Set row and column weights to make it take the entire space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)
    
        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, padx=5, pady=10, sticky="w")
        checkbox.select()
        self.checkbox_list.append(checkbox)

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

class TabsFrame(ctk.CTkFrame):
    def __init__(self, master, COs, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create tabview
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Change Overs")
        self.tabview.tab("Change Overs").grid_columnconfigure(0, weight=1)
        self.label1 = ctk.CTkLabel(self.tabview.tab("Change Overs"))
        self.label1.grid(row=0, column=0, padx=20, pady=20, sticky = 'nw')
        if COs:
            self.checkbox_list = []
            self.label1.configure(text="In the logs imported there are " + str(len(COs)) + " changeovers. Please select the ")
            for i, CO in enumerate(COs):
                text= str(i+1) + '. From ' + str(CO['Start']) + ' to ' + str(CO['Finish']) + '. Duration: ' + str(CO['Duration'])
                self.add_item(text)
        else:
            self.label1.configure(text="No Change Overs detected in data inserted")
            

        self.tabview.add("Search Event/Alarm")
        self.tabview.tab("Search Event/Alarm").grid_columnconfigure(0, weight=1)
        self.label_tab_2 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.tabview.add("Personalized Analysis")
        self.tabview.tab("Personalized Analysis").grid_columnconfigure(0, weight=1)
        self.label_tab_3 = ctk.CTkLabel(self.tabview.tab("Personalized Analysis"), text="CTkLabel on Tab 3")
        self.label_tab_3.grid(row=0, column=0, padx=20, pady=20)
      
    def add_item(self, item):
            checkbox = ctk.CTkCheckBox(self.tabview.tab("Change Overs"), text=item)
            checkbox.grid(row=len(self.checkbox_list)+1, column=0, padx=5, pady=10, sticky="w")
            self.checkbox_list.append(checkbox)

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

class ResultsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Set row and column weights to make it take the entire space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class NavFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Add widgets to the blue frame
        self.bt_navigation1 = ctk.CTkButton(self)
        self.bt_navigation1.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Add widgets to the blue frame
        self.bt_navigation2 = ctk.CTkButton(self)
        self.bt_navigation2.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        # Set blue frame's row and column weights to make it take the entire space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class App(ctk.CTk):

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
    LogsStandard = None #DataFrame with process logs
    LogsAlarms = None #DataFrame with alarm logs
    LogsEvents = None #DataFrame with event logs

    def step_00_init(self):
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure((1,2), weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)

        #Update texts and action button
        App.frames["CSFrame"].title.configure (text="Import Logs")
        App.frames["CSFrame"].text.configure (text="Please select the folder containing the .csv files you want to analyse")
        App.frames["CSFrame"].action_bt.configure(text="Select folder")
        App.frames["CSFrame"].action_bt.configure(command=self.select_folder)

        #WorkSpace: Empty
        self.show_frame("WSFrame")

        #Update Navigation buttons
        App.frames["NFrame"].bt_navigation1.grid_forget()
        App.frames["NFrame"].bt_navigation2.configure(text="Import logs", state="disabled")
        App.frames["NFrame"].bt_navigation2.configure (command= self.import_data)

    def step_10_folderSelected(self):
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure((1,2), weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)

        #Update texts
        App.frames["CSFrame"].title.configure (text="Import Logs")
        App.frames["CSFrame"].text.configure (text="Folder selected" + str(self.dirname))

        #WorkSpace: Scrollable frame
        App.frames["FilesUpload"] = ScrollableCheckBoxFrame(self.right_side_panel, command=self.checkbox_frame_event,
                                                                 item_list=self.csv_files_list)
        self.show_frame("FilesUpload")

        #Update buttons
        App.frames["NFrame"].bt_navigation1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        App.frames["NFrame"].bt_navigation1.configure (text= "Clear all")
        App.frames["NFrame"].bt_navigation1.configure (command= self.back_to_selectfolder)
        if len(self.csv_files_list) > 0:
            App.frames["NFrame"].bt_navigation2.configure(state="enabled")
    
    def step_20_importingData(self):
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure((1,2), weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)

        #Update texts
        App.frames["CSFrame"].title.configure (text="Importing data")
        App.frames["CSFrame"].text.configure (text="Please wait")

        #WorkSpace: Empty or Progressbar
        self.show_frame("WSFrame")

        #Update buttons
        App.frames["CSFrame"].action_bt.grid_forget()
        App.frames["NFrame"].bt_navigation1.grid_forget()
        App.frames["NFrame"].bt_navigation2.grid_forget()

    def step_30_dataImported(self):
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure((0,2), weight=0)
        App.frames["BCFrame"].grid_columnconfigure(1, weight=1)

        #Update texts
        App.frames["CSFrame"].title.configure (text="Select Analysis type")
        App.frames["CSFrame"].text.configure (text="You can do 1, 2 or 3" + str(self.import_success))

        #WorkSpace: TabFrame
        App.frames["TFrame"] = TabsFrame(self.right_side_panel, self.COs)
        self.show_frame("TFrame")

        #Update Buttons
        App.frames["NFrame"].bt_navigation1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        App.frames["NFrame"].bt_navigation1.configure (text= "Clear all and Go back")
        App.frames["NFrame"].bt_navigation1.configure (command= self.back_to_selectfolder)
        App.frames["NFrame"].bt_navigation2.grid_forget()

    def step_40_results(self):
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure((0,1), weight=0)
        App.frames["BCFrame"].grid_columnconfigure(2, weight=1)
        
        #Update texts
        App.frames["CSFrame"].title.configure (text="Results")
        App.frames["CSFrame"].text.configure (text="Please find in the folder bla bla bla")

        #WorkSpace: ResultsFrame

    def left_side_widgets(self, parent):
        # create sidebar logo
        self.logo_label = ctk.CTkLabel(parent, text="VisuaLite", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # create info label
        self.info_label = ctk.CTkLabel(parent, text="FCM One | 1.5", font=ctk.CTkFont(size=15))
        self.info_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        # make middle empty row have the priority
        parent.grid_rowconfigure(2, weight=1)
        # create app controls of appearance and scaling
        self.appearance_mode_label = ctk.CTkLabel(parent, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(parent, values=["Light", "Dark"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=4, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_label = ctk.CTkLabel(parent, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(parent, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")

    def __init__(self):
        super().__init__()

        # configure window
        self.title("VisuaLite V0.1")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # -------------------------------------------------------------------------------------------------------------- left side panel
        self.left_side_panel = ctk.CTkFrame(self, corner_radius=8, width=300)
        self.left_side_panel.grid(row=0, column=0, rowspan=8, sticky="nsew", padx=(20, 10), pady=20)
        self.left_side_widgets(self.left_side_panel)

        self.grid_rowconfigure(0, weight=1)

        # -------------------------------------------------------------------------------------------------------------- right side panel
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

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def clear_all(self):
        # Delete information
        self.dirname = None
        self.csv_files_list = []
        self.import_success = 0
        self.mch_info = None
        self.COs = None
        self.LogsStandard = None
        self.LogsAlarms = None
        self.LogsEvents = None
    
    def show_frame(self, frame_id):
        # method to change frames in position row 2, column 0 of right_side_panel   
 
        if App.current is not None:
            App.frames[App.current].grid_forget() # Hide the current frame

        App.frames[frame_id].grid(row=2, column=0, padx=5, pady= 5, sticky="nsew") # Show the selected frame
        App.current = frame_id

    def back_to_selectfolder (self):
        print("button back to Select folder pressed")
        self.clear_all()
        self.step_00_init()

    def select_folder(self):
        print("button Select folder pressed")

        #Open file dialog to select folder
        self.dirname = fd.askdirectory(parent=self,initialdir=PATH,title='Please select a directory')
        print(self.dirname)

        if self.dirname != '':
            #Look for csv files in the selected folder    
            self.csv_files_list = []
            for filename in os.listdir(self.dirname):
                if filename.lower().endswith('.csv'):
                    self.csv_files_list.append(filename)

            #Update widgets
            self.step_10_folderSelected()
            
            #Pop up with result
            tk.messagebox.showinfo(title='Information', message=str(len(self.csv_files_list)) + ' files found in the folder selected: ' + self.dirname)

    def checkbox_frame_event(self):
        return self.frames['FilesUpload'].get_checked_items()
    
    def import_data(self):
        # Get file names selected
        self.csv_files_list = self.checkbox_frame_event()
        print(self.csv_files_list)
        DataFiles = [self.dirname + '/' + x for x in self.csv_files_list if x.startswith('S')]
        AlarmFiles = [self.dirname + '/' + x for x in self.csv_files_list if x.startswith('A')]
        EventFiles = [self.dirname + '/' + x for x in self.csv_files_list if x.startswith('E')]
        print(DataFiles, AlarmFiles, EventFiles)
        # Import data from csv and format DataFrames
        if len(self.csv_files_list) == 0:
            tk.messagebox.showerror(title='Import failed', message='Please select at least 1 .csv file')

        elif len(DataFiles + AlarmFiles + EventFiles) == 0:
            tk.messagebox.showerror(title='Import failed', message='Visualite could not find logs in the .csv files selected')
            
        elif len(DataFiles + AlarmFiles + EventFiles) > 0:
            #self.import_success, self.mch_info, self.COs, self.LogsStandard, self.LogsAlarms, self.LogsEvents = fcm.import_data(DataFiles, AlarmFiles, EventFiles)
            print(self.import_success)

        if not self.import_success:
            tk.messagebox.showinfo(title='Information', message='Import procedure successful!')
            self.step_30_dataImported()
        
        else:
            tk.messagebox.showerror(title='Import failed', message='Wrong File: ' + str(self.mch_info))



