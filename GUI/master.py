from gui_master import RootGUI ,ComGUI

RootMaster = RootGUI()
ComMaster = ComGUI(RootMaster.root) #pass the main root to the ComGui 
RootMaster.root.mainloop() #start the GUI event loop