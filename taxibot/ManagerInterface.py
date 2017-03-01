class AbstractManager:
    _callList = []

    def AddCall(self,chat_id): pass
    def GetCall(self,chat_id): pass
    def ResetCall(self,chat_id): pass
    def UpdateCall(self,chat_id): pass
    def RemoveCall(self,char_id): pass


class AbstractCall:
    chat_id = None

    def __init__(self,chat_id):
        self.chat_id = chat_id

    def ResetData(self): pass

    def UpdateData(self): pass

