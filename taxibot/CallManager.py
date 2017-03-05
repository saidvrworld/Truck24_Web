from .models import *



class CallManager:


    #public methods

    """create and add new call with new chat_id"""
    def AddCall(self,new_chat_id):
        TaxiCall.objects.create(chat_id=new_chat_id, type="None", number="None", details="None",
                                address="None",status = "building")


    """ return call is it exist and None is it does not"""
    def GetCall(self,chat_id):
        if self._IsCall(chat_id) :
            return self._GetCallByID(chat_id)
        else:
            return None

    """destroy call is it exist"""
    def RemoveCall(self,chat_id):
        cur_call = self.GetCall(chat_id)
        if(cur_call):
            cur_call.delete()





    """ update atributes of call , change value if you sign it in params"""
    def UpdateCall(self, chat_id, new_type=None, new_coordinates = None, new_address = None, new_number = None, new_details = None,new_waiting_for = None,new_status=None,new_isMap=0,new_chat_id=None):

        if(self._IsCall(chat_id)):
             self._UpdateData(chat_id=chat_id,type=new_type,coordinates=new_coordinates,address=new_address,number=new_number,
                                                   details= new_details,waiting_for = new_waiting_for,status=new_status,isMap=new_isMap,new_chat_id=new_chat_id)
        else:
            print("No object")

    def SetNumber(self,chat_id):
        self.UpdateCall(chat_id=chat_id,new_waiting_for="number")

    def SetComments(self,chat_id):
        self.UpdateCall(chat_id=chat_id,new_waiting_for="comments")


    """ reset all atributes of call to None, exept chat_id"""
    def ResetCall(self, chat_id):
        cur_call = self.GetCall(chat_id)
        if (cur_call):
            cur_call.type = "None"
            cur_call.longitude = 0.0
            cur_call.latitude =0.0
            cur_call.address = "None"
            cur_call.number = "None"
            cur_call.waiting_for = "None"
            cur_call.details = "None"
            cur_call.save()


    def HasType(self,chat_id):
        cur_call = self.GetCall(chat_id)
        if(cur_call):
            if (cur_call.type != "None"):
                 return True
            else:
                 return False
        else:
            self.AddCall(chat_id)
            return False

    def HasAddress(self,chat_id):
        cur_call = self.GetCall(chat_id)
        if (cur_call):
            if (cur_call.address != "None"):
                return True
            else:
                return False
        else:
            self.AddCall(chat_id)
            return False

    def HasCoordinates(self,chat_id):
        cur_call = self.GetCall(chat_id)
        if (cur_call):
            if (cur_call.longitude and cur_call.latitude):
                return True
            else:
                return False
        else:
            self.AddCall(chat_id)
            return False

    def HasNumber(self,chat_id):
        cur_call = self.GetCall(chat_id)
        if (cur_call):
            if (cur_call.number != "None"):
                return True
            else:
                return False
        else:
            self.AddCall(chat_id)
            return False


    #private methods


    def _UpdateData(self,chat_id, type = None, coordinates = None, address = None, number = None, details = None,waiting_for = None,status=None,isMap=None,new_chat_id=None):
        cur_call =self.GetCall(chat_id)
        if(cur_call):
            if (type):
               cur_call.type = type

            if (coordinates):
               cur_call.longitude = coordinates[0]
               cur_call.latitude = coordinates[1]

            elif (address):
               cur_call.address = address

            if (number):
                cur_call.number = number

            if(waiting_for):
                cur_call.waiting_for = waiting_for

            if(details):
                cur_call.details = details

            if (status):
                cur_call.status = status

            if(isMap):
                cur_call.update(isMap=True)

            if(new_chat_id):
                cur_call.chat_id=new_chat_id

            cur_call.save()

    """return call by chat_id """
    def _GetCallByID(self,chat_id):
        try:
            return TaxiCall.objects.get(chat_id=chat_id)
        except TaxiCall.MultipleObjectsReturned:
            return TaxiCall.objects.filter(chat_id=chat_id)[0]

    """check if list contain call with this id """
    def _IsCall(self,i_chat_id):
        try:
            if(TaxiCall.objects.get(chat_id=i_chat_id)):
                return True

        except TaxiCall.DoesNotExist:
            return False
        except TaxiCall.MultipleObjectsReturned:
            return True




