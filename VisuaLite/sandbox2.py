import customtkinter
import tkinter

customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.geometry("400x300")


def button_click_event():
    global progress
    progress = customtkinter.CTkToplevel(app)
    # Disable the close button (X button)
    progress.protocol("WM_DELETE_WINDOW", lambda: None)
    progress.resizable(width=False, height=False)
    progress.title("Working on it!")
    progress.wm_transient(app)
    progress_wdgt = customtkinter.CTkProgressBar(progress)
    progress_wdgt.grid(row=0, column=0, padx=20, pady=50, sticky="ew") 
    progress_wdgt.configure(mode="indeterminate")
    progress_wdgt.start()
    print("showed!")
    #progress.destroy()

def button_click_event2():

    progress.destroy()

button1 = customtkinter.CTkButton(app, text="Open Dialog", command=button_click_event)
button1.grid(row=0, column=0, padx=20, pady=50, sticky="ew") 
button2 = customtkinter.CTkButton(app, text="close Dialog", command=button_click_event2)
button2.grid(row=1, column=0, padx=20, pady=50, sticky="ew") 

app.mainloop()
