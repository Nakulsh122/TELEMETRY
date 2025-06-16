import serial
import serial.tools.list_ports
import time

class SerialCtrl():
    def __init__(self):
        self.comList = []
        self.ser = serial.Serial()
        self.ser.status = False  # Custom attribute
        self.sync_cnt = 200
        self.threading = False

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

    def serialSync(self, conn_gui):
        print("Starting serialSync thread...")
        self.threading = True
        cnt = 0
        
        while self.threading:
            try:
                # Send sync command
                sync_command = conn_gui.data.sync.encode()
                self.ser.write(sync_command)
                print(f"Sent sync command: {sync_command}")
                
                # Update GUI status
                conn_gui.sync_status.config(text="syncing...", fg="orange")
                
                # Read response
                raw_msg = self.ser.readline()
                if raw_msg:
                    conn_gui.data.RowMsg = raw_msg
                    conn_gui.data.DecodeMsg()
                    if conn_gui.data.sync_ok in conn_gui.data.message[0]:
                        conn_gui.sync_status.config(text="Synced!", fg="green")
                        conn_gui.btn_start_stream["state"] = "normal"
                        conn_gui.save_check["state"] = "normal"
                        conn_gui.btn_add_chart["state"] = "normal"
                        conn_gui.btn_kill_chart["state"] = "normal"
                        conn_gui.ch_status["text"] = conn_gui.data.message[1]
                        conn_gui.data.syncChannels = int(conn_gui.data.message[1])
                        conn_gui.data.genChannels()
                        conn_gui.data.buildData()
                        print(conn_gui.data.channels ,conn_gui.data.yData)
                        self.threading = False
                        break
                        if self.threading == False:
                            break
                        # print("Sync successful!")
                    else:
                        print(f"Unexpected response: {conn_gui.data.message[0]}")
                # Check if threading should stop
                if not self.threading:
                    break
                    
                time.sleep(0.01)
                
            except Exception as e:
                print(f"Error in serialSync: {e}")
                conn_gui.sync_status.config(text="Error", fg="red")
                break
                
            cnt += 1
            if cnt > self.sync_cnt:
                cnt = 0
                conn_gui.sync_status.config(text="Sync timeout", fg="red")
                print("Sync timeout - no response from device")
                time.sleep(0.5)
        
        print("serialSync thread ended")

if __name__ == "__main__":
    SerialCtrl()