import tkinter as tk
import customtkinter as ctk
import tkinter.filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkcalendar
from PIL import Image
import os

from modules import fcm_one as fcm 
# use fcm.bla bla to use data analysis functions

#execution path
PATH = os.getcwd()

# Get the path to the current script
script_path = os.path.dirname(os.path.abspath(__file__))
print(script_path)
# Construct the path to the file.txt in the resources directory
icon_path = os.path.join(script_path, '..', 'resources', 'ad_logo.ico')

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

TIMES = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
         '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
         '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
         ]
    
class BreadcrumbFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Load the images
        image1_path = os.path.join(script_path, '..', 'resources', 'number-1.png')
        self.step1_img = Image.open(image1_path).resize((30, 30))
        self.step1_img_tk = ctk.CTkImage(self.step1_img)
        image1g_path = os.path.join(script_path, '..', 'resources', 'number-one.png')
        self.step1g_img = Image.open(image1g_path).resize((30, 30))
        self.step1g_img_tk = ctk.CTkImage(self.step1g_img)

        image2_path = os.path.join(script_path, '..', 'resources', 'number-2.png')
        self.step2_img = Image.open(image2_path).resize((30, 30))
        self.step2_img_tk = ctk.CTkImage(self.step2_img)
        image2g_path = os.path.join(script_path, '..', 'resources', 'number-two.png')
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
        self.step2_label = ctk.CTkLabel(self.step2, text="   Data Analysis", image=self.step2g_img_tk, compound="left")
        self.step2_label.grid(row=0, column=0, padx=20, pady=10)

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
    
class CheckBoxFrame(ctk.CTkFrame):
    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self.checkboxesFrame, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, padx=5, pady=10, sticky="w")
        checkbox.select()
        self.checkbox_list.append(checkbox)

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]
    
    def select_all_files(self):
        for checkbox in self.checkbox_list:
            checkbox.select()

    def deselect_all_files(self):
        for checkbox in self.checkbox_list:
            checkbox.deselect()
            
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)
    
        self.command = command

        self.checkboxesFrame = ctk.CTkScrollableFrame(self)
        self.checkboxesFrame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.btnsFrame = ctk.CTkFrame(self)
        self.btnsFrame.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
        self.select_all = ctk.CTkButton(self.btnsFrame, text="Select all", command=self.select_all_files)
        self.select_all.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        self.deselect_all = ctk.CTkButton(self.btnsFrame, text="Deselect all", command=self.deselect_all_files)
        self.deselect_all.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_list = []
        for item in item_list:
            self.add_item(item)

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Set row and column weights to make it take the entire space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.progressbar_1 = ctk.CTkProgressBar(self)
        self.progressbar_1.grid(row=0, column=0, padx=20, pady=50, sticky="ew")
        
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        
class TabsFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, **kwargs)

        self.app = app_instance

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create tabview
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        #-----------------------------------TAB1
        self.tabview.add("Change Overs")
        self.tabview.tab("Change Overs").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Change Overs").grid_rowconfigure(0, weight=1)
        
        self.results_t1 = ctk.CTkScrollableFrame(self.tabview.tab("Change Overs"))
        self.results_t1.grid(row=0, column=0, padx=20, pady=20, sticky = 'nsew')

        self.label1 = ctk.CTkLabel(self.results_t1)
        self.label1.grid(row=0, column=0, padx=20, pady=20, sticky = 'nw')

        self.plot_sel = ctk.CTkButton(self.results_t1, text="Save plots for selection")
        self.plot_all = ctk.CTkButton(self.results_t1, text="Save all plots")
        
        self.COs = []
        if self.app.COs:  
            self.COs = self.app.COs

            self.checkbox_list = []
            self.label1.configure(text="In the logs imported there are " + str(len(self.COs)) + " changeovers. Please select the ")
            for i, CO in enumerate(self.COs):
                text= str(i+1) + '. From ' + str(CO['Start']) + ' to ' + str(CO['Finish']) + '. Duration: ' + str(CO['Duration'])
                self.add_checkbox_t1(text)

            self.plot_sel.grid(row=len(self.checkbox_list)+2, column=0, padx=20, pady=10, sticky="w")
            self.plot_all.grid(row=len(self.checkbox_list)+2, column=0, padx=20, pady=10, sticky="e")

        else:
            self.label1.configure(text="No Change Overs detected in data inserted")
        

        #-----------------------------------TAB2
        self.tabview.add("Search Event/Alarm")
        self.tabview.tab("Search Event/Alarm").grid_rowconfigure(2, weight=1)
        self.tabview.tab("Search Event/Alarm").grid_columnconfigure((0,1,2,3,4), weight=0)
        self.tabview.tab("Search Event/Alarm").grid_columnconfigure(5, weight=1)

        # Get arrays of options from dataframes
        self.columns = []
        if not self.app.LogsAlarms.empty:
            self.alm_list = self.app.LogsAlarms['Alm_Code_Label'].unique().tolist()
            self.columns = self.columns + self.app.LogsAlarms.columns.tolist()
            remove_cols = ['DateTime', 'Alm_Code_Label', 'Label']
            for col in remove_cols:
                self.columns.remove(col)
        else:
            self.alm_list = []

        if not self.app.LogsEvents.empty:
            self.eve_list = self.app.LogsEvents['Evn_Code_Label'].unique().tolist()
            self.columns = self.columns + self.app.LogsEvents.columns.tolist()
            remove_cols = ['DateTime', 'Evn_Code_Label', 'Label', 'Data', 'GpsPos']
            for col in remove_cols:
                self.columns.remove(col)
        else:
            self.eve_list = []

        if not self.app.LogsStandard.empty:
            self.columns = self.columns + self.app.LogsStandard.columns.tolist()
            remove_cols = ['DateTime', 'GpsPos', 'CV1_Label', 'CV2_Label', 'CV3_Label', 'CV4_Label', 'CV5_Label', 'ChangeoverCMDchange']
            for col in remove_cols:
                self.columns.remove(col)

        # Label
        self.label2 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="Please select an event/alarm bla bla")
        self.label2.grid(row=0, column=0, columnspan=5, padx=20, pady=5, sticky="nw")

        # Radio buttons to select Alarm or Event
        self.radio_var = tk.IntVar(value=0)
        self.radio_button_1 = ctk.CTkRadioButton(self.tabview.tab("Search Event/Alarm"), variable=self.radio_var, text="Alarm" ,value=0,
            command=self.update_optionmenu)
        self.radio_button_1.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        self.radio_button_2 = ctk.CTkRadioButton(self.tabview.tab("Search Event/Alarm"), variable=self.radio_var, text="Event" , value=1,
            command=self.update_optionmenu)
        self.radio_button_2.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        # Dropdown
        self.search_var = ctk.StringVar(value="")
        self.optionmenu_1 = ctk.CTkOptionMenu(self.tabview.tab("Search Event/Alarm"), dynamic_resizing=False, variable=self.search_var)
        self.optionmenu_1.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
        self.update_optionmenu()

        # Search Button
        self.search_bt = ctk.CTkButton(self.tabview.tab("Search Event/Alarm"), text="Search", command=self.searchAE)
        self.search_bt.grid(row=1, column=4, padx=(5,10), pady=5, sticky="w")

        # Variable Selection
        self.label3 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="Variable list",font=ctk.CTkFont(weight="bold"))
        self.label3.grid(row=1, column=5, padx=20, pady=5, sticky="w")
        self.var_sel = ctk.CTkScrollableFrame(self.tabview.tab("Search Event/Alarm"))
        self.var_sel.grid(row=2, column=5, padx=(10,20), pady=5, sticky="nsew")
        self.switch_list_t2 = []
        for column_name in self.columns:
            self.add_switch_t2(column_name)

        # Search results
        self.results_t2 = ctk.CTkScrollableFrame(self.tabview.tab("Search Event/Alarm"))
        self.results_t2.grid(row=2, column=0, columnspan=5, padx=(20,10), pady=5, sticky="nsew")
        self.label_results_t2 = ctk.CTkLabel(self.results_t2, text="Search results shown here")
        self.label_results_t2.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        #Dropdowns and Label for time interval
        self.label6 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="Please select the time before/after the selected alarm/event to generate your report")
        self.label6.grid(row=3, column=0, columnspan=5, padx=20, pady=5, sticky="nw")

        self.low_limit = ctk.StringVar(value="")
        self.label4 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="Time before: ")
        self.label4.grid(row=4, column=0, padx=5, pady=(5,20), sticky="e")
        self.optionmenu_2 = ctk.CTkOptionMenu(self.tabview.tab("Search Event/Alarm"), dynamic_resizing=False, variable=self.low_limit,
                                                        values=["1 hour", "2 hours", "4 hours", "8 hours", "1 day"])
        self.optionmenu_2.grid(row=4, column=1, padx=5, pady=(5,20), sticky="ew")
        self.optionmenu_2.set("Select")

        self.high_limit = ctk.StringVar(value="")
        self.label5 = ctk.CTkLabel(self.tabview.tab("Search Event/Alarm"), text="Time after: ")
        self.label5.grid(row=4, column=2, padx=5, pady=(5,20), sticky="e")
        self.optionmenu_3 = ctk.CTkOptionMenu(self.tabview.tab("Search Event/Alarm"), dynamic_resizing=False, variable=self.high_limit,
                                                        values=["1 hour", "2 hours", "4 hours", "8 hours", "1 day"])
        self.optionmenu_3.grid(row=4, column=3, padx=5, pady=(5,20), sticky="ew")
        self.optionmenu_3.set("Select")

        #Action Button
        self.action_t2 = ctk.CTkButton(self.tabview.tab("Search Event/Alarm"), text="Generate and Save Plot", command=self.generate_search_ae_plot)
        self.action_t2.grid(row=4, column=5, padx=(5,20), pady=(5,20), sticky="e")
        self.action_t2.configure(state="disabled")

        # Enable or disable buttons based on alarms/events not imported
        if (not self.alm_list) and (not self.eve_list):
            self.search_bt.configure(state="disabled")
            self.radio_button_1.configure(state="disabled")
            self.radio_button_2.configure(state="disabled")
        
        if (not self.alm_list) and (self.eve_list):
            self.radio_var.set(1)
            self.radio_button_1.configure(state="disabled")

        if (not self.eve_list) and (self.alm_list):
            self.radio_var.set(0)
            self.radio_button_2.configure(state="disabled")

        #-----------------------------------TAB3
        self.tabview.add("Personalized Analysis")
        self.tabview.tab("Personalized Analysis").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Personalized Analysis").grid_rowconfigure(1, weight=1)

        self.aux_plot = ctk.CTkButton(self.tabview.tab("Personalized Analysis"), text="Show Auxiliary Plot", command=self.show_plot)
        self.aux_plot.grid(row=0, column=0, columnspan=2, padx=20, pady=5)

        self.frame_left_t3 = ctk.CTkFrame(self.tabview.tab("Personalized Analysis"))
        self.frame_left_t3.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.label_tab_3 = ctk.CTkLabel(self.frame_left_t3, text="Left side description")
        self.label_tab_3.grid(row=0, column=0, padx=20, columnspan=2, pady=5, sticky="nw")
        self.cal1_text = ctk.CTkLabel(self.frame_left_t3, text='From:')
        self.cal1_text.grid(row=1, column=0, padx=20, pady=2, sticky="nw") 
        self.cal1d = tkcalendar.Calendar(self.frame_left_t3, selectmode="day", date_pattern="yyyy/MM/dd")
        self.cal1d.grid(row=2, column=0, padx=20, pady=2)
        self.cal1t = ctk.CTkOptionMenu(self.frame_left_t3, dynamic_resizing=False, values=TIMES)
        self.cal1t.grid(row=3, column=0, padx=20, pady=(10,20))
        self.cal1t.set("00:00")

        self.cal1_text = ctk.CTkLabel(self.frame_left_t3, text='To:')
        self.cal1_text.grid(row=1, column=1, padx=20, pady=2, sticky="nw")
        self.cal2d = tkcalendar.Calendar(self.frame_left_t3, selectmode="day", date_pattern="yyyy/MM/dd")
        self.cal2d.grid(row=2, column=1, padx=20, pady=2)
        self.cal2t = ctk.CTkOptionMenu(self.frame_left_t3, dynamic_resizing=False, values=TIMES)
        self.cal2t.grid(row=3, column=1, padx=20, pady=(10,20))
        self.cal2t.set("00:00")

        self.action_t3 = ctk.CTkButton(self.tabview.tab("Personalized Analysis"), text="Generate and save Plot", command=self.generate_personalized_plot)
        self.action_t3.grid(row=2, column=1, padx=20, pady=20, sticky="se")

        self.var_sel_t3 = ctk.CTkScrollableFrame(self.tabview.tab("Personalized Analysis"))
        self.var_sel_t3.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.switch_list_t3 = []
        for column_name in self.columns:
            self.add_switch_t3(column_name)

    #TAB1 functions
    def add_checkbox_t1(self, item):
        checkbox = ctk.CTkCheckBox(self.results_t1, text=item)
        checkbox.grid(row=len(self.checkbox_list)+1, column=0, padx=5, pady=10, sticky="w")
        self.checkbox_list.append(checkbox)

    def get_checked_items(self):
        COs_sts = []
        for checkbox in self.checkbox_list:
            COs_sts.append(checkbox.get())
        return COs_sts
        
    #TAB2 functions
    def update_optionmenu(self): 
        
        if self.radio_var.get() == 0:
            print("Alarm selected")
            self.optionmenu_1.configure(values=self.alm_list)
        elif self.radio_var.get() == 1:
            print("Event selected")
            self.optionmenu_1.configure(values=self.eve_list)

        self.optionmenu_1.set("Search value")

    def searchAE(self):
        if self.search_var.get() == "Search value":
            tk.messagebox.showwarning(title='No option selected!', message='Select an Alarm o Event to search') # type: ignore
        else:
            self.action_t2.configure(state="enabled")

            selected_item = self.search_var.get()
            self.ae_number= int(selected_item[1:selected_item.index('_')]) 
            #text.index('_') returns position of _ char / or int(text.split('_')[0][1:]) this function splits string by _
            
            self.timestamps = []
            if selected_item[0] == 'A':
                print("Searching Alarm ", self.ae_number)
                self.timestamps = self.app.LogsAlarms[self.app.LogsAlarms['AlarmNumber'] == self.ae_number]['DateTime'].tolist()
                
            elif selected_item[0] == 'E':
                print("Searching Event ", self.ae_number)
                self.timestamps = self.app.LogsEvents[self.app.LogsEvents['EventNumber'] == self.ae_number]['DateTime'].tolist()
            
            print(self.timestamps)
            for t in self.timestamps:
                text=str(t.date()) + " at " + str(t.time())
                print(text)
            
            self.result_selection = tk.IntVar(value=0)
            if self.timestamps:

                self.radiobtn_list = []
                self.label_results_t2.configure(text="In the imported logs there are " + str(len(self.timestamps)) + " occurrences of " + selected_item + "." +
                                                "\n\nPlease select the occurence you want to plot:", justify='left')
                
                for i, t in enumerate(self.timestamps):
                    text= str(i+1) + ". " + str(t.date()) + " at " + str(t.time())
                    self.add_radiobtn_t2(text, i)

            tk.messagebox.showinfo(title='Search results', message="Found " + str(len(self.timestamps)) + " occurrences of " + selected_item) # type: ignore

    def add_radiobtn_t2(self, item, i):
        radiobtn = ctk.CTkRadioButton(self.results_t2, text=item, variable=self.result_selection, value=i)
        radiobtn.grid(row=len(self.radiobtn_list)+1, column=0, padx=15, pady=5, sticky="w")
        self.radiobtn_list.append(radiobtn)

    def add_switch_t2(self, label):
        switch = ctk.CTkSwitch(self.var_sel, text=label)
        switch.grid(row=len(self.switch_list_t2), column=0, padx=10, pady=5, sticky="w")
        self.switch_list_t2.append(switch)

    def get_selected_vars_t2(self):
        return [switch.cget("text") for switch in self.switch_list_t2 if switch.get() == 1]

    def generate_search_ae_plot (self):
        if (self.high_limit.get() == "Select") or (self.low_limit.get()== "Select"):
            tk.messagebox.showwarning(title='No option selected!', message='Select time boundaries for the report') # type: ignore
            return #Stop
        
        cols = self.get_selected_vars_t2()

        dest_folder = fd.askdirectory(parent=self,initialdir=PATH,title='Select a destination directory')
        if dest_folder =='': #no folder selected
            print('no folder selected')
            return #Stop
        
        now_dt = fcm.datetime.datetime.now()
        format_dt = now_dt.strftime('%Y.%m.%d_%H%M%S')
        name_file = ""
        if self.radio_var.get() == 0:
            name_file="Custom_Plot_A{}_{}".format(self.ae_number, format_dt)
        elif self.radio_var.get() == 1:
            name_file="Custom_Plot_E{}_{}".format(self.ae_number, format_dt)

        file_path = os.path.join(dest_folder, (name_file + '.html')) # type: ignore
        print(file_path)

        date1, date2 = fcm.date_limits(self.timestamps[self.result_selection.get()],self.low_limit.get(), self.high_limit.get())
        fig = fcm.custom_plot1 (self.app.LogsStandard, self.app.LogsAlarms, self.app.LogsEvents, cols, date1, date2, name_file)
        try:
            fig.write_html(file_path, config={'displaylogo': False})
            print("File saved successfully.")
            tk.messagebox.showinfo(title='Plot saved!', message="Plot saved in destination folder") # type: ignore

        except Exception as e:
            tk.messagebox.showwarning(title='Error saving file', message="Error saving file:" + e) # type: ignore
            print("Error saving file:", e)

    #TAB3 functions
    def show_plot(self):
        plot_fig = fcm.create_aux_plot(self.app.LogsStandard, self.app.LogsAlarms, self.app.LogsEvents)
        plot_window = ctk.CTkToplevel(self.app)
        plot_window.resizable(width=False, height=False)
        plot_window.title("Auxiliary Plot")
        # Keep the toplevel window in front of the root window
        plot_window.wm_transient(self.app)
        
        canvas = FigureCanvasTkAgg(plot_fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def add_switch_t3(self, label):
        switch = ctk.CTkSwitch(self.var_sel_t3, text=label)
        switch.grid(row=len(self.switch_list_t3), column=0, padx=10, pady=5, sticky="w")
        self.switch_list_t3.append(switch)

    def get_selected_vars_t3(self):
        return [switch.cget("text") for switch in self.switch_list_t3 if switch.get() == 1]

    def generate_personalized_plot(self):
        date1 = self.cal1d.get_date()
        time1 = self.cal1t.get()
        date2 = self.cal2d.get_date()
        time2 = self.cal2t.get() 
        
        datetime1 = fcm.datetime.datetime(int(date1.split('/')[0]), int(date1.split('/')[1]), int(date1.split('/')[2]), int(time1.split(':')[0]), 0, 0)  # Year, month, day, hour, minute, second
        datetime2 = fcm.datetime.datetime(int(date2.split('/')[0]), int(date2.split('/')[1]), int(date2.split('/')[2]), int(time2.split(':')[0]), 0, 0)  # Year, month, day, hour, minute, second
        print(datetime1, datetime2)

        time_difference = datetime2 - datetime1

        if (time_difference.days < 0):
            tk.messagebox.showwarning(title='Incorrect dates', message='"From:" date is bigger than "To:" date') # type: ignore
            return #Stop
        elif (time_difference.days > 5):
            tk.messagebox.showwarning(title='Date range too big', message='Please select a date range smaller than 5 days') # type: ignore
            return #Stop:
        
        cols = self.get_selected_vars_t3()

        dest_folder = fd.askdirectory(parent=self,initialdir=PATH,title='Select a destination directory')
        if dest_folder =='': #no folder selected
            print('no folder selected')
            return #Stop
        
        now_dt = fcm.datetime.datetime.now()
        format_dt = now_dt.strftime('%Y.%m.%d_%H%M%S')
        name_file="Custom_Plot_{}".format(format_dt)
        
        file_path = os.path.join(dest_folder, (name_file + ".html"))
        print(file_path)

        fig = fcm.custom_plot1(self.app.LogsStandard, self.app.LogsAlarms, self.app.LogsEvents, cols, datetime1, datetime2, name_file)
        try:
            fig.write_html(file_path, config={'displaylogo': False})
            print("File saved successfully.")
            tk.messagebox.showinfo(title='Plot saved!', message="Plot saved in destination folder") # type: ignore

        except Exception as e:
            tk.messagebox.showwarning(title='Error saving file', message="Error saving file:" + e) # type: ignore
            print("Error saving file:", e)

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
    LogsStandard = fcm.pd.DataFrame() #DataFrame with process logs
    LogsAlarms = fcm.pd.DataFrame() #DataFrame with alarm logs
    LogsEvents = fcm.pd.DataFrame() #DataFrame with event logs

    def step_00_init(self):
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure(1, weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)
        App.frames["BCFrame"].step1_label.configure(font=ctk.CTkFont(size=18, weight="bold"))
        App.frames["BCFrame"].step2_label.configure(font=ctk.CTkFont(size=15, weight="normal"))
        #App.frames["BCFrame"].step3_label.configure(font=ctk.CTkFont(size=15, weight="normal"))

        #Update texts and action button
        App.frames["CSFrame"].title.configure(text="Import Logs")
        App.frames["CSFrame"].text.configure(text="Please select the folder containing the .csv files you want to analyse")
        App.frames["CSFrame"].action_bt.configure(text="Select folder")
        App.frames["CSFrame"].action_bt.configure(command=self.select_folder)
        App.frames["CSFrame"].action_bt.grid(row=1, column=2, padx=20, pady=10, sticky="se")

        #WorkSpace: Empty
        self.show_frame("WSFrame")
        
        #Update Navigation buttons
        App.frames["NFrame"].bt_navigation1.grid_forget()
        App.frames["NFrame"].bt_navigation2.configure(text="Import logs", state="disabled")
        App.frames["NFrame"].bt_navigation2.configure(command= self.import_data_cmd)
        App.frames["NFrame"].bt_navigation2.grid(row=0, column=2, padx=20, pady=10, sticky="e")

    def step_10_folderSelected(self):
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure(1, weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)

        #Update texts
        App.frames["CSFrame"].title.configure(text="Import Logs")
        App.frames["CSFrame"].text.configure(text="Folder selected" + str(self.dirname))

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
    
    def step_20_importingData(self):
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure(1, weight=0)
        App.frames["BCFrame"].grid_columnconfigure(0, weight=1)

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
        #Update breadcrumb
        App.frames["BCFrame"].grid_columnconfigure(0, weight=0)
        App.frames["BCFrame"].grid_columnconfigure(1, weight=1)
        App.frames["BCFrame"].step1_label.configure(font=ctk.CTkFont(size=15, weight="normal"), image=App.frames["BCFrame"].step1g_img_tk)
        App.frames["BCFrame"].step2_label.configure(font=ctk.CTkFont(size=18, weight="bold"), image=App.frames["BCFrame"].step2_img_tk)
        #App.frames["BCFrame"].step3_label.configure(font=ctk.CTkFont(size=15, weight="normal"))

        #Update texts
        App.frames["CSFrame"].title.configure(text="Select Analysis type")
        App.frames["CSFrame"].text.configure(text="You can do 1, 2 or 3")
        App.frames["CSFrame"].action_bt.grid_forget()
        
        #WorkSpace: TabFrame
        App.frames["TFrame"] = TabsFrame(self.right_side_panel, self) # Pass the instance of App to TabsFrame
        self.show_frame("TFrame")
        App.frames["TFrame"].plot_all.configure(command= self.plot_all_COs)
        App.frames["TFrame"].plot_sel.configure(command= self.plot_sel_COs)


        #Update Buttons
        App.frames["NFrame"].bt_navigation1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        App.frames["NFrame"].bt_navigation1.configure(text= "Clear all and Go back")
        App.frames["NFrame"].bt_navigation1.configure(command= self.back_to_selectfolder)
        App.frames["NFrame"].bt_navigation2.grid_forget()

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
        # set the dimensions of the screen 
        w = 1300 # width
        h = 820 # height

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # and where it is placed
        #self.geometry(f"{1300}x{820}")
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.iconbitmap(icon_path)

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
        self.dirname = fd.askdirectory(parent=self,initialdir=PATH,title='Select a directory with log files')
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
            tk.messagebox.showinfo(title='Information', message=str(len(self.csv_files_list)) + ' files found in the folder selected: ' + self.dirname) # type: ignore

    def checkbox_frame_event(self):
        return self.frames['FilesUpload'].get_checked_items()
    
    def importing_data(self):
        if self.dirname != None:
            DataFiles = [self.dirname + '/' + x for x in self.csv_files_list if x.startswith('S')]
            AlarmFiles = [self.dirname + '/' + x for x in self.csv_files_list if x.startswith('A')]
            EventFiles = [self.dirname + '/' + x for x in self.csv_files_list if x.startswith('E')]
            print(DataFiles, AlarmFiles, EventFiles)
        else:
            return #Stop
        # Import data from csv and format DataFrames
        if len(self.csv_files_list) == 0:
            tk.messagebox.showerror(title='Import failed', message='Please select at least 1 .csv file') # type: ignore

        elif len(DataFiles + AlarmFiles + EventFiles) == 0:
            tk.messagebox.showerror(title='Import failed', message='Visualite could not find logs in the .csv files selected') # type: ignore
            
        elif len(DataFiles + AlarmFiles + EventFiles) > 0:
            self.import_success, self.mch_info, self.COs, self.LogsStandard, self.LogsAlarms, self.LogsEvents = fcm.import_data(DataFiles, AlarmFiles, EventFiles)
            print(self.import_success)

        if self.import_success:
            self.step_30_dataImported()
            tk.messagebox.showinfo(title='Information', message='Import procedure successful!') # type: ignore
        
        else:
            self.step_10_folderSelected()
            tk.messagebox.showerror(title='Import failed', message='Wrong File: ' + str(self.mch_info)) # type: ignore
        
        print(self.COs)
    
    def import_data_cmd(self):
        # Bypass state to show progressBar
        self.step_20_importingData()

        # Get file names selected
        self.csv_files_list = self.checkbox_frame_event()
        print(self.csv_files_list)

        if self.csv_files_list == []:
            tk.messagebox.showerror(title='Import failed', message='Please select at least one log file') # type: ignore
            self.step_10_folderSelected()
        else:
            self.after(1000, self.importing_data) #wait 1000ms and next step
    
    def plot_all_COs(self):
        dest_folder = fd.askdirectory(parent=self,initialdir=PATH,title='Select a destination directory')
        if dest_folder =='': #no folder selected
            print('no folder selected')
            return #Stop
        
        if self.COs:
            for i, CO in enumerate(self.COs):
                df = fcm.ChangeOverToDF(CO, self.LogsStandard)
                fig = fcm.Plot_ChangeOver(df, self.mch_info, self.LogsAlarms, self.LogsEvents)
                name_file= "CO"+ str(i+1) + "_" + str(CO['Start'].date()) + ".html"
                file_path = os.path.join(dest_folder, name_file)
                print(file_path)
                try:
                    fig.write_html(file_path, config={'displaylogo': False})
                    print("File saved successfully.")
                except Exception as e:
                    print("Error saving file:", e)

    def plot_sel_COs(self):
        
        COs = App.frames["TFrame"].get_checked_items()
        
        dest_folder =''
        flag = 0
        
        for i, CO_sts in enumerate(COs):
            print(i)
            if CO_sts == 1:
                #first plot
                if flag == 0: 
                    #Open file dialog to select folder
                    dest_folder = fd.askdirectory(parent=self,initialdir=PATH,title='Select a destination directory')

                    if dest_folder == '': #no folder selected
                        print('no folder selected')
                        return #Stop
                
                flag=1
                df = fcm.ChangeOverToDF(self.COs[i], self.LogsStandard)
                fig = fcm.Plot_ChangeOver(df, self.mch_info, self.LogsAlarms, self.LogsEvents)
                name_file= "CO"+ str(i+1) + "_" + str(self.COs[i]['Start'].date()) + ".html"
                file_path = os.path.join(dest_folder, name_file)
                print(file_path)
                try:
                    fig.write_html(file_path, config={'displaylogo': False})
                    print("File saved successfully.")
                except Exception as e:
                    print("Error saving file:", e)

        if flag == 0:
            tk.messagebox.showwarning(title='No option selected!', message='Select at least one ChangeOver to plot') # type: ignore
            return #Stop



        
            



