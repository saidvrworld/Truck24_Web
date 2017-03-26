#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.http import HttpResponse,JsonResponse
from .BotManager import BotManager
import telebot
import json



token = "350774649:AAG5JYhMCZ2rCi7gh6OWILTru37fdPQrqhg"

bot = telebot.TeleBot(token)
botManager = BotManager(bot)



def webhook(request):
    bot.remove_webhook()
    bot.set_webhook(url="https://umsdiller.herokuapp.com/umsbot/"+token+"/")
    return HttpResponse("ok")


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


    elif("callback_query" in keysOfUpdate):
        botManager.inlineManager(Update["callback_query"])





