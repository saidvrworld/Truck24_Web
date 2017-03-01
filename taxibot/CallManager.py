from .ManagerInterface import *


class TaxiCall(AbstractCall):
    chat_id = None
    type = None   # type of ride
    longitude = None   #float
    latitude = None    #float
    address = None     #str
    number = None     #int
    details = "нет"
    waiting_for = None


    def __init__(self,chat_id):
        self.chat_id = chat_id

    def ResetData(self):

        self.type = None
        self.longitude = None
        self.latitude = None
        self.address = None
        self.number =  None

    def UpdateData(self, type = None, coordinates = None, address = None, number = None, details = None,waiting_for = None):
        if (type):
            self.type = type

        elif (coordinates):
            self.longitude = coordinates[0]
            self.latitude = coordinates[1]

        elif (address):
           self.address = address

        elif (number):
           self.number = number

        elif(waiting_for):
            self.waiting_for = waiting_for

        elif(details):
            self.details = details


    def HasType(self):
        if(self.type):
            return True
        else:
            return False

    def HasAddress(self):
        if(self.address):
            return True
        else:
            return False

    def HasCoordinates(self):
        if(self.longitude and self.latitude):
            return True
        else:
            return False

    def HasNumber(self):
        if(self.number):
            return True
        else:
            return False

class CallManager(AbstractManager):
    _callList = []


    #public methods

    """create and add new call with new chat_id"""
    def AddCall(self,new_chat_id):
        newCall = TaxiCall(chat_id=new_chat_id)
        self._callList.append(newCall)

    """ return call is it exist and None is it does not"""
    def GetCall(self,chat_id):
        if self._IsCall(chat_id) :
            return self._GetCallByID(chat_id)
        else:
            return None

    """destroy call is it exist"""
    def RemoveCall(self,chat_id):
        call_to_delete = self.GetCall(chat_id=chat_id)
        if call_to_delete:
            self._callList.remove(call_to_delete)

    """ reset all atributes of call to None, exept chat_id"""
    def ResetCall(self,chat_id):
        if self._IsCall(chat_id) :
             self._GetCallByID(chat_id).ResetData()

    """ update atributes of call , change value if you sign it in params"""
    def UpdateCall(self, chat_id, new_type=None, new_coordinates = None, new_address = None, new_number = None, new_details = None,new_waiting_for = None):
        if(self._IsCall(chat_id=chat_id)):
             self._GetCallByID(chat_id).UpdateData(type=new_type,coordinates=new_coordinates,address=new_address,number=new_number,
                                                   details= new_details,waiting_for = new_waiting_for)
        else:
            print("No object")

    def SetNumber(self,chat_id):
        self.UpdateCall(chat_id=chat_id,new_waiting_for="number")

    def SetComments(self,chat_id):
        self.UpdateCall(chat_id=chat_id,new_waiting_for="comments")



    #private methods

    """return call by chat_id """
    def _GetCallByID(self,chat_id):
        for exact_call in self._callList:
            if(exact_call.chat_id == chat_id):
                return exact_call

    """check if list contain call with this id """
    def _IsCall(self,chat_id):
        if (chat_id in [call.chat_id for call in self._callList]):
            return True
        else:
            return False


