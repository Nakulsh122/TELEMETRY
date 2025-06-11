# # General Gui management logic
# # Using tkinter

# # We will have root element that will be used to host all the other elements
# # on the root we will have frames that are a local continer for widgets
# we can nest frames inside frames.

from tkinter import *
from tkinter import messagebox


class RootGUI:
    def __init__(self):
        self.root = Tk()  # initialising the root element.
        self.root.title("Serial Communication GUI")
        self.root.geometry("800x200")
        self.root.resizable(True, True)
        self.root.config(bg="black")


class ComGUI:
    def __init__(self, root, serial):  # initialise the comGUI frame
        self.root = root
        self.serial = serial  # include the serial controller in the gui
        self.frame = LabelFrame(
            self.root, text="Com Manager", bg="black", fg="white", padx=10, pady=10
        )
        self.label_com = Label(
            self.frame,
            text="Available Port(s):",
            bg="black",
            fg="white",
            width=15,
            anchor="w",
        )
        self.label_bodR = Label(
            self.frame, text="Bode Rate", bg="black", fg="white", width=15, anchor="w"
        )
        self.ComOptMenu()
        self.BodeRateMenu()
        self.btn_refresh = Button(
            self.frame,
            text="Refresh",
            bg="black",
            fg="white",
            width=10,
            command=self.refresh_menu,
        )
        self.btn_connect = Button(
            self.frame,
            text="Connect",
            bg="black",
            fg="white",
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
        self.drop_com.config(width=10, bg="white", fg="black")

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
        self.drop_Bode.config(width=10, bg="white", fg="black")

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
                messagebox.showinfo("Connection Status",InfoMsg)
            else:
                ErrorMsg = f"Error connecting to {self.clicked_com.get()} at {self.clicked_Bode.get()}"

            pass
        else:
            self.serial.serialClose()
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_com["state"] = "active"
            self.drop_Bode["state"] = "active"
            # start closing the connection
            pass


if __name__ == "__main__":
    RootGUI()
    ComGUI()
