from gui_master import RootGUI ,ComGUI
from serial_master import SerialCtrl
Serial = SerialCtrl()
RootMaster = RootGUI()
ComMaster = ComGUI(RootMaster.root,Serial) #pass the main root to the ComGui 