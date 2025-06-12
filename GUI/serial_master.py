import serial
import serial.tools.list_ports

class SerialCtrl():
    def __init__(self):
        self.comList = []
        self.ser = serial.Serial()
        self.ser.status = False  # Custom attribute

    def getComList(self):
        ports = serial.tools.list_ports.comports()
        self.comList = ['-'] + [com[0] for com in ports]

    def serialConnect(self, gui):
        PORT = gui.clicked_com.get()
        BAUD = gui.clicked_Bode.get()

        if not self.ser.is_open:
            try:
                self.ser.port = PORT
                self.ser.baudrate = int(BAUD)
                self.ser.timeout = 0.1
                self.ser.open()
                self.ser.status = True
                print(f"Connected to {PORT} at {BAUD} baud.")
            except Exception as e:
                self.ser.status = False
                print(f"Some Error Occurred: {e}")

    def serialClose(self):
        try:
            if self.ser.is_open:
                self.ser.close()
                self.ser.status = False
                print("port closed")
        except Exception as e:
            self.ser.status = False
            print(f"Error closing port: {e}")

if __name__ == "__main__":
    SerialCtrl()
