# # General Gui management logic
# # Using tkinter

# # We will have root element that will be used to host all the other elements
# # on the root we will have frames that are a local continer for widgets
# we can nest frames inside frames.

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading    
black = "#000000"
white = "#FFFFFF"
class RootGUI:
    def __init__(self,serial,data):
        self.root = Tk()  # initialising the root element.
        self.root.title("Serial Communication GUI")
        self.root.geometry("400x120")
        self.root.resizable(True, True)
        self.root.config(bg=black)
        self.serial = serial 
        self.data = data 
        self.root.protocol("WM_DELETE_WINDOW", self.closeWindow)
    
    def closeWindow(self):
        print("Closing the Window")
        self.root.destroy()
        self.serial.serialClose()
        self.serial.threading = False

class ComGUI:
    def __init__(self, root, serial,data):  # initialise the comGUI frame
        self.root = root
        self.serial = serial  # include the serial controller in the gui
        self.data = data
        self.conn_menu = None  # Initialize connection menu reference
        self.frame = LabelFrame(
            self.root, text="Com Manager", bg=black, fg=white, padx=10, pady=10
        )
        self.label_com = Label(
            self.frame,
            text="Available Port(s):",
            bg=black,
            fg=white,
            width=15,
            anchor="w",
        )
        self.label_bodR = Label(
            self.frame, text="Bode Rate", bg=black, fg=white, width=15, anchor="w"
        )
        self.ComOptMenu()
        self.BodeRateMenu()
        self.btn_refresh = Button(
            self.frame,
            text="Refresh",
            bg=black,
            fg=white,
            width=10,
            command=self.refresh_menu,
        )
        self.btn_connect = Button(
            self.frame,
            text="Connect",
            bg=black,
            fg=white,
            width=10,
            state="disabled",
            command=self.serialConnect,
        )
        self.Publish()
        pass

    def ComOptMenu(self):
        # dropdow for the com options
        self.serial.getComList()
        self.clicked_com = StringVar()  # store the clicked Options
        self.clicked_com.set(self.serial.comList[0])
        self.drop_com = OptionMenu(
            self.frame,
            self.clicked_com,
            *self.serial.comList,
            command=self.Connect_ctrl,
        )
        self.drop_com.config(width=10, bg=white, fg = black)

    def BodeRateMenu(self):
        # dropdow for the Bode options
        self.Bode_rates = [
            110,
            300,
            600,
            1200,
            2400,
            4800,
            9600,
            14400,
            19200,
            28800,
            38400,
            57600,
            115200,
            128000,
            256000,
        ]
        self.clicked_Bode = StringVar()  # store the clicked Options
        self.clicked_Bode.set(self.Bode_rates[0])
        self.drop_Bode = OptionMenu(
            self.frame, self.clicked_Bode, *self.Bode_rates, command=self.Connect_ctrl
        )
        self.drop_Bode.config(width=10, bg=white, fg = black)

    def Publish(self):
        # will publish the component on the root
        self.frame.grid(
            row=0, column=0, rowspan=3, columnspan=3, padx=5, pady=5
        )  # we add a grid to the frame so that it can be placed
        self.label_com.grid(column=1, row=2)
        self.drop_com.grid(column=2, row=2)
        self.label_bodR.grid(column=1, row=3)
        self.drop_Bode.grid(column=2, row=3)
        self.btn_refresh.grid(column=3, row=2)
        self.btn_connect.grid(column=3, row=3)
        pass

    def Connect_ctrl(self, other):
        # this will be used to control the connect button
        if self.clicked_com.get() == "-" or self.clicked_Bode.get() == "-":
            self.btn_connect.config(state="disabled")
        else:
            self.btn_connect.config(state="normal")
        pass

    def refresh_menu(self):
        self.serial.getComList()
        self.clicked_com.set("-")
        self.clicked_Bode.set("-")

    def serialConnect(self):
        if self.btn_connect["text"] in "Connect":
            self.serial.serialConnect(self)
            if self.serial.ser.status:
                self.btn_connect["text"] = "Disconnect"
                self.btn_refresh["state"] = "disabled"
                self.drop_com["state"] = "disabled"
                self.drop_Bode["state"] = "disabled"
                InfoMsg = f"Connected to {self.clicked_com.get() } at {self.clicked_Bode.get()}"
                messagebox.showinfo("Connection Status", InfoMsg)
                
                # Display the connection menu
                self.conn_menu = ConnGUI(self.root, self.serial, self.data)
                
                # Start the sync thread - FIXED: Pass conn_menu instead of self
                self.serial.t1 = threading.Thread(
                    target=self.serial.serialSync,
                    args=(self.conn_menu,),  # Pass ConnGUI instance
                    daemon=True,
                )
                self.serial.t1.start()
            else:
                ErrorMsg = f"Error connecting to {self.clicked_com.get()} at {self.clicked_Bode.get()}"
                messagebox.showerror("Connection Error", ErrorMsg)
        else:
            self.serial.threading = False
            if self.conn_menu:
                self.conn_menu.ConnGUIClose()
                self.conn_menu.data.clearData()
            self.serial.serialClose()
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_com["state"] = "active"
            self.drop_Bode["state"] = "active"
            # start closing the connection
            pass


class ConnGUI:
    def __init__(self, root, serial, data):
        self.padx = 10
        self.pady = 10
        self.root = root
        self.serial = serial
        self.data = data
        self.frame = LabelFrame(
            self.root,
            text="Connection Manager",
            bg=black,
            fg=white,
            padx=self.padx,
            pady=self.pady
        )

        self.sync_Label = Label(
            self.frame,
            text="sync status",
            bg=black,
            fg=white,
            width=15,
            anchor="w",
            padx=self.padx,
            pady=self.pady
        )

        self.sync_status = Label(
            self.frame,
            text="...Sync...",
            bg=black,
            fg="orange",
            width=15,
            anchor="w"
        )

        self.ch_label = Label(
            self.frame,
            text="Active Channels:",
            bg=black,
            fg=white,
            width=15,
            anchor="w"
        )

        self.ch_status = Label(
            self.frame,
            text="...",
            bg=black,
            fg=white,
            width=15,
            anchor="w"
        )

        self.btn_start_stream = Button(
            self.frame,
            text="Start",
            state="disabled",
            bg=black,
            fg=white,
            width=5,
            command=self.start_stream
        )

        self.btn_stop_stream = Button(
            self.frame,
            text="Stop",
            state="disabled",
            bg=black,
            fg=white,
            width=5,
            command=self.stop_stream
        )

        self.btn_add_chart = Button(
            self.frame,
            text="Add Chart",
            bg=black,
            fg=white,
            command=self.add_chart
        )

        self.btn_kill_chart = Button(
            self.frame,
            text="Kill Chart",
            bg=black,
            fg=white,
            command=self.kill_chart
        ) 

        self.save = False
        self.SaveVar = IntVar()
        self.save_check = Checkbutton(
            self.frame,
            text="Save Data",
            variable=self.SaveVar,
            onvalue=1,
            offvalue=0,
            bg="black",
            fg="green",  # high contrast check
            activeforeground="green",
            selectcolor="gray20",  # background of the checkbox box
            command=self.save_data
        )
        

        self.ConnGUIOpen()

    def ConnGUIOpen(self):
        self.root.geometry("800x120")
        self.frame.grid(
            row=0,
            column=4,
            rowspan=3,
            columnspan=3,
            padx=5,
            pady=5,
        )
        self.frame.config(
            width=60
        )
        self.sync_Label.grid(column=1, row=1)
        self.sync_status.grid(column=2, row=1)
        self.ch_label.grid(column=1, row=2)
        self.ch_status.grid(column=2, row=2)
        self.btn_start_stream.grid(column=3, row=1)
        self.btn_stop_stream.grid(column=3, row=2)
        self.btn_add_chart.grid(column=4, row=1)
        self.btn_kill_chart.grid(column=4, row=2)
        self.save_check.grid(column=5, row=1)
        
    def ConnGUIClose(self):
        for widget in self.frame.winfo_children():  # list of all children inside the frame 
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("800x120")

    def start_stream(self):
        print("starting Stream")
        pass

    def stop_stream(self):
        print("Stopping Stream")
        pass
    
    def add_chart(self):
        print("Add chart")
        pass

    def kill_chart(self):
        print("fill chart")
        pass
    
    def save_data(self):
        print(self.SaveVar.get())
        pass

if __name__ == "__main__":
    RootGUI()
    ComGUI()
    ConnGUI()