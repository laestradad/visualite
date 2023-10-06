import customtkinter as ctk
import os
from PIL import Image
from functools import partial

from modules.logging_cfg import setup_logger
logger = setup_logger()
logger.info("help_app.py imported")

PATH = os.path.dirname(os.path.abspath(__file__))
SCREEN = os.path.join(PATH, '..', 'resources/help_rsrc/screenshots')
ICONS = os.path.join(PATH, '..', 'resources/help_rsrc/icons')
TEXTS = os.path.join(PATH, '..', 'resources/help_rsrc/texts')
APP_ICON = os.path.join(PATH, '..', 'resources', 'ad_logo.ico')
VERSION = "V0.00.04"

class overview_frame(ctk.CTkFrame):

	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		# Config of Frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
		self.scroll_frame.grid(row=0, column=0, sticky="nsew")
		self.scroll_frame.grid_rowconfigure(6, weight=1)
		self.scroll_frame.grid_columnconfigure(0, weight=1)

		# Import images
		self.overview1 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "1_overview1.jpg")), size=(156, 204))
		self.overview2 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "1_overview2.jpg")), size=(273, 91))
		self.overview3 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "1_overview3.jpg")), size=(614, 69))

		# Title
		self.title = ctk.CTkLabel(self.scroll_frame, text="Overview", font=ctk.CTkFont(size=22, weight="bold"))

		# Text 1
		self.text_1 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=360, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_1.insert("end", self.import_text("1_overview1.txt"))
		self.text_1.configure(state="disabled") 
		# Text 2
		self.text_2 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=120, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_2.insert("end", self.import_text("1_overview2.txt"))
		self.text_2.configure(state="disabled") 

		# Images
		self.img_1 = ctk.CTkLabel(self.scroll_frame, text="", image=self.overview1)
		self.img_2 = ctk.CTkLabel(self.scroll_frame, text="", image=self.overview2)
		self.img_3 = ctk.CTkLabel(self.scroll_frame, text="", image=self.overview3)
		
		# Positioning of widgets
		self.title.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nw")
		self.text_1.grid(row=1, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_1.grid(row=2, column=0,  padx=30, pady=0, sticky="nw")
		self.text_2.grid(row=3, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_2.grid(row=4, column=0,  padx=30, pady=0, sticky="nw")
		self.img_3.grid(row=5, column=0,  padx=30, pady=(5,30), sticky="nw")

	def import_text(self, file_name):
		with open(os.path.join(TEXTS, file_name), 'r', encoding='utf-8') as text_file:
			contents = text_file.read()
		return contents

class gettingSt_frame(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		# Config of Frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
		self.scroll_frame.grid(row=0, column=0, sticky="nsew")
		self.scroll_frame.grid_rowconfigure(5, weight=1)
		self.scroll_frame.grid_columnconfigure(0, weight=1)

		# Import images
		self.gettingSt1 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "2_gettingSt1.png")), size=(600, 375))
		self.gettingSt2 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "2_gettingSt2.png")), size=(600, 404))

		# Title
		self.title = ctk.CTkLabel(self.scroll_frame, text="Getting Started", font=ctk.CTkFont(size=22, weight="bold"))

		# Text 1
		self.text_1 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=70, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_1.insert("end", self.import_text("2_gettingSt1.txt"))
		self.text_1.configure(state="disabled") 
		# Text 2
		self.text_2 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=135, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_2.insert("end", self.import_text("2_gettingSt2.txt"))
		self.text_2.configure(state="disabled") 

		# Images
		self.img_1 = ctk.CTkLabel(self.scroll_frame, text="", image=self.gettingSt1)
		self.img_2 = ctk.CTkLabel(self.scroll_frame, text="", image=self.gettingSt2)
		
		# Positioning of widgets
		self.title.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nw")
		self.text_1.grid(row=1, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_1.grid(row=2, column=0,  padx=30, pady=5, sticky="nw")
		self.text_2.grid(row=3, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_2.grid(row=4, column=0,  padx=30, pady=(5,30), sticky="nw")

	def import_text(self, file_name):
		with open(os.path.join(TEXTS, file_name), 'r', encoding='utf-8') as text_file:
			contents = text_file.read()
		return contents

class import_frame(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		# Config of Frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
		self.scroll_frame.grid(row=0, column=0, sticky="nsew")
		self.scroll_frame.grid_rowconfigure(3, weight=1)
		self.scroll_frame.grid_columnconfigure(0, weight=1)

		# Import images
		self.import1 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "3_import1.jpg")), size=(600, 375))

		# Title
		self.title = ctk.CTkLabel(self.scroll_frame, text="Importing data", font=ctk.CTkFont(size=22, weight="bold"))

		# Text 1
		self.text_1 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=180, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_1.insert("end", self.import_text("3_import.txt"))
		self.text_1.configure(state="disabled") 
		
		# Images
		self.img_1 = ctk.CTkLabel(self.scroll_frame, text="", image=self.import1)
		
		# Positioning of widgets
		self.title.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nw")
		self.text_1.grid(row=1, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_1.grid(row=2, column=0,  padx=30, pady=(5,30), sticky="nw")

	def import_text(self, file_name):
		with open(os.path.join(TEXTS, file_name), 'r', encoding='utf-8') as text_file:
			contents = text_file.read()
		return contents

class dataA_frame(ctk.CTkFrame):
	def __init__(self, master, app_instance, **kwargs):
		super().__init__(master, **kwargs)
		
		self.app = app_instance
		
		# Config of Frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
		self.scroll_frame.grid(row=0, column=0, sticky="nsew")
		self.scroll_frame.grid_rowconfigure(5, weight=1)
		self.scroll_frame.grid_columnconfigure(0, weight=1)

		# Import images
		self.changeover_img = ctk.CTkImage(Image.open(os.path.join(ICONS, "changeover_dark.png")), size=(20, 20))
		self.search_img = ctk.CTkImage(Image.open(os.path.join(ICONS, "search_dark.png")), size=(20, 20))
		self.custom_img = ctk.CTkImage(Image.open(os.path.join(ICONS, "custom_dark.png")), size=(20, 20))

		# Title
		self.title = ctk.CTkLabel(self.scroll_frame, text="Data Analysis", font=ctk.CTkFont(size=22, weight="bold"))

		# Text 1
		self.text_1 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=30, font=ctk.CTkFont(size=16), corner_radius=0,
					activate_scrollbars=False, wrap="word")
		self.text_1.insert("end", self.import_text("4_dataA.txt"))
		self.text_1.configure(state="disabled") 

		# Button 1
		self.btn_1 = ctk.CTkButton(self.scroll_frame, text="Changeover", image=self.changeover_img, font=ctk.CTkFont(size=18), height=40,
									anchor="w", command=lambda: self.app.change_frame("changeover"))
		# Button 2
		self.btn_2 = ctk.CTkButton(self.scroll_frame, text="Search Alarm/Event", image=self.search_img, font=ctk.CTkFont(size=18),height=40,
									anchor="w", command=lambda: self.app.change_frame("search"))
		# Button 3
		self.btn_3 = ctk.CTkButton(self.scroll_frame, text="Personalized Analysis", image=self.custom_img, font=ctk.CTkFont(size=18),height=40,
									anchor="w", command=lambda: self.app.change_frame("custom"))
		
		# Positioning of widgets
		self.title.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nw")
		self.text_1.grid(row=1, column=0,  padx=30, pady=5, sticky="nsew")
		self.btn_1.grid(row=2, column=0,  padx=30, pady=10)
		self.btn_2.grid(row=3, column=0,  padx=30, pady=10)
		self.btn_3.grid(row=4, column=0,  padx=30, pady=(10,30))

	def import_text(self, file_name):
		with open(os.path.join(TEXTS, file_name), 'r', encoding='utf-8') as text_file:
			contents = text_file.read()
		return contents

class changeover_frame(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		# Config of Frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
		self.scroll_frame.grid(row=0, column=0, sticky="nsew")
		self.scroll_frame.grid_rowconfigure(5, weight=1)
		self.scroll_frame.grid_columnconfigure(0, weight=1)

		# Import images
		self.changeover1 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "4-1_changeover1.png")), size=(600, 354))
		self.changeover2 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "4-1_changeover2.jpg")), size=(520, 158))

		# Title
		self.title = ctk.CTkLabel(self.scroll_frame, text="Change Over", font=ctk.CTkFont(size=22, weight="bold"))

		# Text 1
		self.text_1 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=70, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_1.insert("end", self.import_text("4-1_changeover1.txt"))
		self.text_1.configure(state="disabled") 
		# Text 2
		self.text_2 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=70, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_2.insert("end", self.import_text("4-1_changeover2.txt"))
		self.text_2.configure(state="disabled") 

		# Images
		self.img_1 = ctk.CTkLabel(self.scroll_frame, text="", image=self.changeover1)
		self.img_2 = ctk.CTkLabel(self.scroll_frame, text="", image=self.changeover2)
		
		# Positioning of widgets
		self.title.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nw")
		self.text_1.grid(row=1, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_1.grid(row=2, column=0,  padx=30, pady=5, sticky="nw")
		self.text_2.grid(row=3, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_2.grid(row=4, column=0,  padx=30, pady=(5,30), sticky="nw")

	def import_text(self, file_name):
		with open(os.path.join(TEXTS, file_name), 'r', encoding='utf-8') as text_file:
			contents = text_file.read()
		return contents

class search_frame(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		# Config of Frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
		self.scroll_frame.grid(row=0, column=0, sticky="nsew")
		self.scroll_frame.grid_rowconfigure(3, weight=1)
		self.scroll_frame.grid_columnconfigure(0, weight=1)

		# Import images
		self.search1 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "4-2_search1.png")), size=(600, 392))

		# Title
		self.title = ctk.CTkLabel(self.scroll_frame, text="Search for an Alarm or Event", font=ctk.CTkFont(size=22, weight="bold"))

		# Text 1
		self.text_1 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=260, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_1.insert("end", self.import_text("4-2_search.txt"))
		self.text_1.configure(state="disabled") 

		# Images
		self.img_1 = ctk.CTkLabel(self.scroll_frame, text="", image=self.search1)
		
		# Positioning of widgets
		self.title.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nw")
		self.text_1.grid(row=1, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_1.grid(row=2, column=0,  padx=30, pady=(5,30), sticky="nw")

	def import_text(self, file_name):
		with open(os.path.join(TEXTS, file_name), 'r', encoding='utf-8') as text_file:
			contents = text_file.read()
		return contents

class custom_frame(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		# Config of Frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
		self.scroll_frame.grid(row=0, column=0, sticky="nsew")
		self.scroll_frame.grid_rowconfigure(5, weight=1)
		self.scroll_frame.grid_columnconfigure(0, weight=1)

		# Import images
		self.custom1 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "4-3_custom1.png")), size=(600, 433))
		self.custom2 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "4-3_custom2.png")), size=(600, 404))

		# Title
		self.title = ctk.CTkLabel(self.scroll_frame, text="Personalized Analysis", font=ctk.CTkFont(size=22, weight="bold"))

		# Text 1
		self.text_1 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=90, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_1.insert("end", self.import_text("4-3_custom1.txt"))
		self.text_1.configure(state="disabled") 
		# Text 2
		self.text_2 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=60, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_2.insert("end", self.import_text("4-3_custom2.txt"))
		self.text_2.configure(state="disabled") 

		# Images
		self.img_1 = ctk.CTkLabel(self.scroll_frame, text="", image=self.custom1)
		self.img_2 = ctk.CTkLabel(self.scroll_frame, text="", image=self.custom2)
		
		# Positioning of widgets
		self.title.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nw")
		self.text_1.grid(row=1, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_1.grid(row=2, column=0,  padx=30, pady=5, sticky="nw")
		self.text_2.grid(row=3, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_2.grid(row=4, column=0,  padx=30, pady=(5,30), sticky="nw")

	def import_text(self, file_name):
		with open(os.path.join(TEXTS, file_name), 'r', encoding='utf-8') as text_file:
			contents = text_file.read()
		return contents

class output_frame(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		# Config of Frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
		self.scroll_frame.grid(row=0, column=0, sticky="nsew")
		self.scroll_frame.grid_rowconfigure(4, weight=1)
		self.scroll_frame.grid_columnconfigure(0, weight=1)

		# Import images
		self.output1 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "5_output1.jpg")), size=(377, 69))
		self.output2 = ctk.CTkImage(Image.open(os.path.join(SCREEN, "5_output2.jpg")), size=(377, 355))

		# Title
		self.title = ctk.CTkLabel(self.scroll_frame, text="Output files", font=ctk.CTkFont(size=22, weight="bold"))

		# Text 1
		self.text_1 = ctk.CTkTextbox(self.scroll_frame, fg_color="transparent", height=180, font=ctk.CTkFont(size=16), corner_radius=0, 
					activate_scrollbars=False, wrap="word")
		self.text_1.insert("end", self.import_text("5_output.txt"))
		self.text_1.configure(state="disabled")

		# Images
		self.img_1 = ctk.CTkLabel(self.scroll_frame, text="", image=self.output1)
		self.img_2 = ctk.CTkLabel(self.scroll_frame, text="", image=self.output2)
		
		# Positioning of widgets
		self.title.grid(row=0, column=0, padx=30, pady=(30,10), sticky="nw")
		self.text_1.grid(row=1, column=0,  padx=30, pady=5, sticky="nsew")
		self.img_1.grid(row=2, column=0,  padx=30, pady=0, sticky="nw")
		self.img_2.grid(row=3, column=0,  padx=30, pady=(0,30), sticky="nw")

	def import_text(self, file_name):
		with open(os.path.join(TEXTS, file_name), 'r', encoding='utf-8') as text_file:
			contents = text_file.read()
		return contents

class App(ctk.CTkToplevel):
	# Version
	version = VERSION

	# GUI management
	frames = {} #dictionary containing frames
	current = None #class ctkFrame of current frame selected

	def __init__(self):
		super().__init__()

		logger.info("help_app init")

		self.title("Help")
		self.geometry("900x720")
		self.iconbitmap(APP_ICON)

		# set grid layout 1x2
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		# load images with light and dark mode image
		self.logo_image = ctk.CTkImage(Image.open(os.path.join(ICONS, "CustomTkinter_logo_single.png")), size=(26, 26))
		self.overview_img = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS, "overview_light.png")),
											 dark_image=Image.open(os.path.join(ICONS, "overview_dark.png")), size=(20, 20))
		self.gettingSt_img = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS, "gettingSt_light.png")),
											dark_image=Image.open(os.path.join(ICONS, "gettingSt_dark.png")), size=(20, 20))
		self.import_img = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS, "import_light.png")),
											 dark_image=Image.open(os.path.join(ICONS, "import_dark.png")), size=(20, 20))
		self.dataA_img = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS, "data_light.png")),
											 dark_image=Image.open(os.path.join(ICONS, "data_dark.png")), size=(20, 20))
		self.changeover_img = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS, "changeover_light.png")),
											 dark_image=Image.open(os.path.join(ICONS, "changeover_dark.png")), size=(20, 20))
		self.search_img = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS, "search_light.png")),
											 dark_image=Image.open(os.path.join(ICONS, "search_dark.png")), size=(20, 20))
		self.custom_img = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS, "custom_light.png")),
											 dark_image=Image.open(os.path.join(ICONS, "custom_dark.png")), size=(20, 20))
		self.output_img = ctk.CTkImage(light_image=Image.open(os.path.join(ICONS, "output_light.png")),
											 dark_image=Image.open(os.path.join(ICONS, "output_dark.png")), size=(20, 20))

		# create navigation frame
		self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
		self.navigation_frame.grid(row=0, column=0, sticky="nsew")
		self.navigation_frame.grid_rowconfigure(10, weight=1)

		self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  VisuaLite Help", image=self.logo_image,
													compound="left", font=ctk.CTkFont(size=18, weight="bold"))
		self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=(20,5))
		self.version_label = ctk.CTkLabel(self.navigation_frame, text= App.version,
													compound="left", font=ctk.CTkFont(size=11))
		self.version_label.grid(row=1, column=0, padx=20, pady=(0,10))

		self.overview_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="1. Overview", 
											fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.overview_img, anchor="w", 
											command=lambda: self.change_frame("overview"), font=ctk.CTkFont(size=14, weight="bold"))
		self.overview_button.grid(row=2, column=0, sticky="ew")
					   
		self.gettingSt_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="2. Getting started", 
											fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.gettingSt_img, anchor="w", 
											command=lambda: self.change_frame("gettingSt"), font=ctk.CTkFont(size=14, weight="bold"))
		self.gettingSt_button.grid(row=3, column=0, sticky="ew")
					   
		self.import_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="3. Import data", 
											fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.import_img, anchor="w", 
											command=lambda: self.change_frame("import"), font=ctk.CTkFont(size=14, weight="bold"))
		self.import_button.grid(row=4, column=0, sticky="ew")
					   
		self.dataA_button  = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="4. Data analysis", 
											fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.dataA_img, anchor="w", 
											command=lambda: self.change_frame("dataA"), font=ctk.CTkFont(size=14, weight="bold"))
		self.dataA_button.grid(row=5, column=0, sticky="ew")
					   
		self.changeover_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="4.1. Change Over", 
											fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.changeover_img, anchor="w", 
											command=lambda: self.change_frame("changeover"), font=ctk.CTkFont(size=14))
		self.changeover_button.grid(row=6, column=0, sticky="ew")
						
		self.search_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="4.2. Search alarm/event", 
											fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.search_img, anchor="w", 
											command=lambda: self.change_frame("search"), font=ctk.CTkFont(size=14))
		self.search_button.grid(row=7, column=0, sticky="ew")
					   
		self.custom_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="4.3. Personalized analysis", 
											fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.custom_img, anchor="w", 
											command=lambda: self.change_frame("custom"), font=ctk.CTkFont(size=14))
		self.custom_button.grid(row=8, column=0, sticky="ew")
					   
		self.output_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="5. Output files", 
											fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.output_img, anchor="w", 
											command=lambda: self.change_frame("output"), font=ctk.CTkFont(size=14, weight="bold"))
		self.output_button.grid(row=9, column=0, sticky="ew")

		# Help contents
		App.frames['overview'] = overview_frame(self)
		App.frames['gettingSt'] = gettingSt_frame(self)
		App.frames['import'] = import_frame(self)
		App.frames['dataA'] = dataA_frame(self, self)
		App.frames['changeover'] = changeover_frame(self)
		App.frames['search'] = search_frame(self)
		App.frames['custom'] = custom_frame(self)
		App.frames['output'] = output_frame(self)

		App.frames['overview'].grid(row=0, column=1, sticky="nsew")
		App.current = 'overview'

		# Window appearance
		self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light"],command=self.change_appearance_mode_event)
		self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=10, sticky="s")
		self.scaling_optionemenu = ctk.CTkOptionMenu(self.navigation_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
		self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10,20), sticky="s")
		self.scaling_optionemenu.set("100%")


	def change_frame(self, frame_id):
		logger.info("button pressed")
		logger.info(f"{frame_id=}")

		if App.current is not None:
			App.frames[App.current].grid_forget() # Hide the current frame

		App.frames[frame_id].grid(row=0, column=1, sticky="nsew") # Show the selected frame
		App.current = frame_id

	def change_appearance_mode_event(self, new_appearance_mode):
		ctk.set_appearance_mode(new_appearance_mode)
	
	def change_scaling_event(self, new_scaling: str):
		new_scaling_float = int(new_scaling.replace("%", "")) / 100
		ctk.set_widget_scaling(new_scaling_float)
