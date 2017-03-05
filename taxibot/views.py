#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.views import generic
from .models import TaxiCall
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .BotManager import BotManager
import telebot
import json



token = "309803225:AAEfkOtjUfLCTSHicJD05uy7AvilTCkzOYs"

bot = telebot.TeleBot(token)
botManager = BotManager(bot)


class CallListView(generic.ListView):  #FIRST SECTION, CALLS JUST COME AND HASN'T  ACCEPTED BY MANAGER YED
    template_name = "index.html"
    context_object_name = "call_list"
    def get_queryset(self):
        call_list = TaxiCall.objects.filter(status="new").order_by("-call_time")
        return call_list

class calls_with_car_ListView(generic.ListView):   #SECOND SECTION, CALLS ACCEPTED AND HAVE BEEN ATTACHED CAR, NOW MANAGER WAIT FOR USER TO AGREE WITH OFFERED CAR

    template_name = "waiting_calls.html"
    context_object_name = "call_list"
    def get_queryset(self):
        call_list = TaxiCall.objects.filter(status="waiting").order_by("-call_time")
        return call_list

class acceptedCalls(generic.ListView):    # USERS ALREADY AGREE WITH CAR AND CAR ON THE WAY TO USER

    template_name = "accepted.html"
    context_object_name = "call_list"
    def get_queryset(self):
        call_list = TaxiCall.objects.filter(status__in=["accepted","accepted_cancel","arrived"]).order_by("-call_time")
        return call_list

def setDriver(request):     #ATACHING CAR TO USERS CALL
     CallCenterNumber = "+998977377055"
     callId,carType,carNumber,carTime = [None for i in range(4)]
     try:
         callId = request.POST["calls[]"]
         carType = request.POST["car[]"]
         carNumber = request.POST["car_number"]
         carTime = request.POST["time_for_coming"]
     except :
         print("there are no selected calls")
     if(callId):
         call_list = TaxiCall.objects.filter(call_id=callId)

         if(call_list):
               current_call = call_list[0]
               current_call.status = "waiting"
               current_call.car_set.create(car_type=carType,car_number=carNumber,car_time=carTime,driver_number=CallCenterNumber)
               current_call.save()

               if(carTime!="0"):

                   botManager.SendOffer(chat_id=current_call.chat_id,car_type=carType,car_number=carNumber,arrival_time=carTime)
               else:

                   botManager.SendOffer(chat_id=current_call.chat_id,car_type=carType,car_number=carNumber)


     return HttpResponseRedirect(reverse("taxibot:callList"))


# отправляет клиенту данные о прибытие машины и сбрасывает данные о машине
def EndCall(request):
    callId =None
    try:
        callId = request.POST["calls[]"]

    except:
        print("there are no selected calls")
    if (callId):
        current_call = TaxiCall.objects.get(call_id=callId)
        current_call.status = "arrived"
        chat_id = current_call.chat_id
        botManager.SendArrived(chat_id=chat_id)
        current_call.chat_id = 0
        current_call.save()


    return HttpResponseRedirect(reverse("taxibot:accepted"))





def clearDB(request):  # delete all calls

    TaxiCall.objects.all().delete()
    return HttpResponseRedirect(reverse("taxibot:callList"))






####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
# TELEBOT


def webhook(request):
    bot.remove_webhook()
    bot.set_webhook(url="https://favorittaxi.herokuapp.com/taxibot/309803225:AAEfkOtjUfLCTSHicJD05uy7AvilTCkzOYs/")
    return HttpResponseRedirect(reverse("taxibot:callList"))


def getUpdate(request):

    UpdateObj = json.loads(request.body.decode("utf-8"))
    UpdateManager(UpdateObj)

    return JsonResponse({'ok': True})



def UpdateManager(Update):
    keysOfUpdate = Update.keys()
    if("message" in keysOfUpdate):
        message = Update["message"]
        keys = message.keys()

        if("text" in keys):
            botManager.textManager(message=message)
        elif("location" in keys):
            botManager.get_location(message)
        elif("contact" in keys):
            botManager.GetContact(message)

    elif("callback_query" in keysOfUpdate):
        botManager.inlineManager(Update["callback_query"])





