#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot
import os
from django.conf import settings


class BotManager:




    bot = None



    def __init__(self,bot):
        self.bot = bot


    # перехватывает все сообщения
    def textManager(self,message):

        self.Start(message)

    # Ждет и обрабатывает запросы с кнопок
    def inlineManager(self,call):
        # Если сообщение из чата с ботом
        message = call["message"]

        if message:
            current_chat_id = call["message"]["chat"]["id"]
            message_id = call["message"]["message_id"]
            call_data = call["data"]

            if call_data == "start":
                self.ShowMainMenu(message)
            elif call_data == "сумки":
                self.BagsMenu(message)
            elif call_data == "Женская сумка":
                self.sendInfo(message)
            else:
                self.bot.send_message(current_chat_id, "Эта кнопка пока не работает)\nШирин нужно добавить описание товаров")

    def Start(self,message):

        current_chat_id = message["chat"]["id"]
        keyboard = telebot.types.InlineKeyboardMarkup()
        callback_button = telebot.types.InlineKeyboardButton(text="Показать", callback_data="start")
        keyboard.add(callback_button)
        self.bot.send_message(current_chat_id, "Меню товаров", reply_markup=keyboard)

    # вызов меню выбора поездки
    def ShowMainMenu(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Сумки", callback_data="сумки")
        button3 = telebot.types.InlineKeyboardButton(text="Одежда", callback_data="одежда")
        button4 = telebot.types.InlineKeyboardButton(text="Акксесуары", callback_data="Акксесуары")

        keyboard.add(button1)
        keyboard.add(button3)
        keyboard.add(button4)

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Главное Меню\n\n\n",reply_markup=keyboard)

    def BagsMenu(self, message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Женская сумка", callback_data="Женская сумка")
        button3 = telebot.types.InlineKeyboardButton(text="Мужской рюгзак", callback_data="Мужской рюгзак")
        button4 = telebot.types.InlineKeyboardButton(text="чемодан", callback_data="чемодан")

        keyboard.add(button1)
        keyboard.add(button3)
        keyboard.add(button4)

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Выберите тип сумки\n\n\n",
                                   reply_markup=keyboard)


    def sendInfo(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]
        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Очень вместительная сумка в нее помещаются все учебники, даже калкулус\n ")
        self.sendImage(message)

    def sendImage(self,message):
        current_chat_id = message["chat"]["id"]
        import json
        file_path = os.path.join(settings.STATIC_ROOT, )
        file = open(file_path, "rb")
        print(self.bot.send_photo(current_chat_id, file))

        jsonFile= "{'photo': [<telebot.types.PhotoSize object at 0x7fe9fb9787f0>, <telebot.types.PhotoSize object at 0x7fea0bcba240>, <telebot.types.PhotoSize object at 0x7fe9fba81128>, <telebot.types.PhotoSize object at 0x7fe9fb715320>]}"
        list = json.loads(jsonFile)

        for file1 in list["photo"]:

            self.bot.send_message(current_chat_id,file1.file_id)

            self.bot.send_photo(current_chat_id, file1.file_id)





