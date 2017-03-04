#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import generic
from .models import TaxiCall
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
import multiprocessing
import requests
import os



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
                   pass
                   # SendOffer(chat_id=current_call.chat_id,car_type=carType,car_number=carNumber,arrival_time=carTime)
               else:
                   pass
                   # SendOffer(chat_id=current_call.chat_id,car_type=carType,car_number=carNumber)


     return HttpResponseRedirect(reverse("taxibot:callList"))


# отправляет клиенту данные о прибытие машины и сбрасывает данные о машине
def EndCall(request):
    callId =None
    try:
        callId = request.POST["calls[]"]

    except:
        print("there are no selected calls")
    if (callId):
        current_call = TaxiCall.objects.filter(call_id=callId)[0]
        current_call.status = "arrived"
        chat_id = current_call.chat_id
        #SendArrived(chat_id=chat_id)
        current_call.chat_id = 0
        current_call.save()


    return HttpResponseRedirect(reverse("taxibot:accepted"))

# запуск бота
def CreateBot(request):
    #StartBot()
    return HttpResponseRedirect(reverse("taxibot:callList"))



def clearDB(request):  # delete all calls

    TaxiCall.objects.all().delete()
    return HttpResponseRedirect(reverse("taxibot:callList"))

# создание нового заказа в бд
def AddCall(user_chat_id,journey_type,user_number,user_coordinates=None,user_address=None,comments="нет"):
    if(user_coordinates):
        TaxiCall.objects.create(chat_id = user_chat_id,type=journey_type,number=user_number,details=comments,IsMap=True,longitude=user_coordinates[0],latitude=user_coordinates[1])

    else:
        TaxiCall.objects.create(chat_id = user_chat_id, type=journey_type, number=user_number, details=comments, address=user_address)

# удаляет заказ из бд
def RemoveCall(chat_id):
    TaxiCall.objects.filter(chat_id=chat_id).delete()

# принятие вызова (машина выезжает)
def AcceptCall(chat_id):
    current_call = TaxiCall.objects.filter(chat_id=chat_id)[0]
    current_call.status = "accepted"
    current_call.save()

# отмена после принятия вызова(когда машина в пути ) сбрасывает id на 0, но сам заказ остается в бд
def AcceptCancelCall(chat_id):
    current_call = TaxiCall.objects.filter(chat_id=chat_id)[0]
    current_call.status = "accepted_cancel"
    current_call.chat_id = 0
    current_call.save()

# дпные о водителе из бд по chat_id
def DriverInfo(chat_id):
    current_call = TaxiCall.objects.filter(chat_id=chat_id)[0]
    if(current_call):
         driver = current_call.car_set.all()[0]
         return {"car_number":driver.car_number,"car_type":driver.car_type,"time":driver.car_time,"driver_number":driver.driver_number}
    else:
        return None


import telebot
import json
#from flask import Flask, request


token = "309803225:AAEfkOtjUfLCTSHicJD05uy7AvilTCkzOYs"

bot = telebot.TeleBot(token)


def webhook(request):
    bot.remove_webhook()
    bot.set_webhook(url="https://favorittaxi.herokuapp.com/taxibot/getUpdate")
    return HttpResponseRedirect(reverse("taxibot:callList"))



def test(request):


    if(True):

       return HttpResponse(True)

    else:
        return  HttpResponse("failed")




def getUpdate(request):
    UpdateObj = json.loads(request.body.decode("utf-8"))

    TaxiCall.objects.create(chat_id=12, type="HAH2", number="2324", details="sfcsaf",
                            address="sadasf")

    return JsonResponse({'ok': True})