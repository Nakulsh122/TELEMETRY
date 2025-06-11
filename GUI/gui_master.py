# # General Gui management logic 
# # Using tkinter 

# # We will have root element that will be used to host all the other elements 
# # on the root we will have frames that are a local continer for widgets 
# we can nest frames inside frames.

from tkinter import *

class RootGUI:
    def __init__(self):
        self.root = Tk() #initialising the root element.
        self.root.title("Serial Communication GUI")
        self.root.geometry("800x200")
        self.root.resizable(True, True)
        self.root.config(bg="black")

class ComGUI():
    def __init__(self,root): #initialise the comGUI frame
        self.root = root
        self.frame = LabelFrame(self.root , text = "Com Manager", bg="black",fg="white",padx=10,pady=10)
        self.label_com = Label(self.frame, text="Available Port(s):",bg="black",fg="white",width=15,anchor='w')
        self.label_bodR = Label(self.frame, text="Bode Rate",bg="black",fg="white",width=15,anchor='w')
        self.ComOptMenu()
        self.BodeRateMenu()
        self.btn_refresh = Button(self.frame,text="Refresh",bg="black",fg="white",width=10)
        self.btn_connect = Button(self.frame,text="Connect",bg="black",fg="white",width=10,state="disabled")
        self.Publish()
        pass
    def ComOptMenu(self):
        #dropdow for the com options 
        self.com_ports = ["-", "COM3","COM2", "COM1"]
        self.clicked_com = StringVar() #store the clicked Options
        self.clicked_com.set(self.com_ports[0])
        self.drop_com = OptionMenu(self.frame,self.clicked_com, *self.com_ports)
        self.drop_com.config(width=10,bg="white",fg="black")
    def BodeRateMenu(self):
        #dropdow for the Bode options 
        self.Bode_rates = ["-", "COM3","COM2", "COM1"]
        self.clicked_Bode = StringVar() #store the clicked Options
        self.clicked_Bode.set(self.com_ports[0])
        self.drop_Bode = OptionMenu(self.frame,self.clicked_Bode, *self.Bode_rates)
        self.drop_Bode.config(width=10,bg="white",fg="black")
    def Publish(self):
        #will publish the component on the root
        self.frame.grid(row = 0 , column= 0 , rowspan=3 ,columnspan=3 , padx=5, pady=5) # we add a grid to the frame so that it can be placed
        self.label_com.grid(column=1 , row=2)
        self.drop_com.grid(column=2,row=2)
        self.label_bodR.grid(column=1,row = 3)
        self.drop_Bode.grid(column=2,row=3)
        self.btn_refresh.grid(column=3,row=2)
        self.btn_connect.grid(column=3,row=3)
        pass
if __name__ == "__main__" :
    RootGUI() 