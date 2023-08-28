#app.grid_columnconfigure(1, minsize=300)

from tkinter import *

from PIL import Image, ImageTk

root = Tk()
root.title("Title")
root.geometry("600x600")
root.configure(background="black")



class Example(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        self.image = Image.open("resources/co_preview.png")
        self.img_copy= self.image.copy()

        self.frame1 = Frame(self)
        self.frame1.grid(row=0,column=0)

        self.frame2 = Frame(self)
        self.frame2.grid(row=0,column=1)

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self.frame1, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)



e = Example(root)
e.pack(fill=BOTH, expand=YES)


root.mainloop()
