import serial.tools.list_ports

class SerialCtrl():
    def __init__(self):
        self.comList=[]
        pass
    def getComList (self):
        ports = serial.tools.list_ports.comports() #will be a objects with the com ports 
        self.comList = [com[0] for com in ports] #get the list of the objects of ports
        self.comList.insert(0,'-')
        pass
    def serialConnect(self,gui):
        #connect to a serial port 
        try:
            self.ser.is_open
        except:
            PORT = gui.clicked_com.get()
            BAUD = gui.clicked_Bode.get()
            self.ser = serial.Serial()
            self.ser.baudrate = BAUD
            self.ser.port = PORT
            self.ser.timeout = 0.1
        
        try : 
            if self.ser.is_open:
                self.ser.status = True
            else:
                PORT = gui.clicked_com.get()
                BAUD = gui.clicked_Bode.get()
                self.ser = serial.Serial()
                self.ser.baudrate = int(BAUD)
                self.ser.port = PORT
                self.ser.timeout = 0.1
                self.ser.open()
                self.ser.status = True
        except:
            self.ser.status = False
            print("Some Error Occured")
    def serialClose(self):
        try:
            if self.ser.is_open:
                self.ser.status = False
                print("port closed")
            self.ser.close()
        except:
            self.ser.status = False
if __name__ == "__main__":
    SerialCtrl()