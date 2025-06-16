class DataMaster():
    def __init__(self):
        self.sync = "#?#\n"
        self.startStream = "#s#\n"
        self.stopStream = "#A#\n"
        self.sync_ok = "!"
        self.syncChannels = 0
        self.xData = []
        self.yData = []
    
    def DecodeMsg(self):
        temp = self.RowMsg.decode('utf8')
        if len(temp) > 0 :
            if '#' in temp:
                self.message = temp.split('#')
                del self.message[0]
                # print(self.message)
                print(self.message)
    def genChannels(self):
        self.channels = [f"Ch{ch}" for ch in range(1,int(self.syncChannels)+1)]

    def buildData(self):
        for _ in range(self.syncChannels):
            self.yData.append([])

    def clearData(self):
        self.xData.clear()
        self.yData.clear()
        self.RowMsg = ""
        self.message = []
        