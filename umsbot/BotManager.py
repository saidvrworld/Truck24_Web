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
            elif call_data == "Наш Гимн":
                self.sendSong(message)
            elif call_data == "Магазин":
                self.ShopMenu(message)
            elif call_data == "Про нас":
                self.About(message)
            elif call_data == "Галерея":
                self.Gallery(message)
            elif call_data == "сумки":
                self.BagsMenu(message)
            elif call_data in ["Женская сумка","Мужской рюгзак","чемодан"]:
                self.sendInfo(message)
            else:
                self.bot.send_message(current_chat_id, "Эта кнопка пока не работает)\nШирин нужно добавить описание товаров")

    def Start(self,message):

        current_chat_id = message["chat"]["id"]
        keyboard = telebot.types.InlineKeyboardMarkup()
        callback_button = telebot.types.InlineKeyboardButton(text="Показать", callback_data="start")
        keyboard.add(callback_button)
        self.bot.send_message(current_chat_id, "Главная", reply_markup=keyboard)

    # вызов меню выбора поездки
    def ShowMainMenu(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="🖼Галерея", callback_data="Галерея")
        button3 = telebot.types.InlineKeyboardButton(text="🎵Наш Гимн", callback_data="Наш Гимн")
        button4 = telebot.types.InlineKeyboardButton(text="🛒Магазин", callback_data="Магазин")
        button5 = telebot.types.InlineKeyboardButton(text="🏢Про нас", callback_data="Про нас")


        keyboard.add(button1)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)


        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Главное Меню\n\n\n",reply_markup=keyboard)

    def ShopMenu(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="🛍Сумки", callback_data="сумки")
        button3 = telebot.types.InlineKeyboardButton(text="👕Одежда", callback_data="одежда")
        button4 = telebot.types.InlineKeyboardButton(text="🔗Акксесуары", callback_data="Акксесуары")

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

    def About(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]
        about_text ="\nThe central mission of Inha University in Tashkent is to achieve excellence in the undergraduate and graduate education. IUT provides superior and comprehensive educational opportunities at various levels to students and professionals. IUT contributes to the advancement of society and nation through creative activity, scholarly development of new knowledge, research, and public service.The core objective is to educate leaders of the future in technology, industry, and business and other professions, who will contribute to the development of the nation and human society.  \n"
        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text=about_text)

    def sendImage(self,message):
        current_chat_id = message["chat"]["id"]
        for i in ["1.jpg","2.jpg"]:
            file_path = os.path.join(settings.STATIC_ROOT, i)
            file = open(file_path, "rb")
            self.bot.send_photo(current_chat_id, file)

    def Gallery(self,message):
        current_chat_id = message["chat"]["id"]
        for i in range(1,6):
            file_path = os.path.join(settings.STATIC_ROOT, "IUT/inha_"+str(i)+".jpg")
            file = open(file_path, "rb")
            self.bot.send_photo(current_chat_id, file)

    def sendSong(self,message):
        current_chat_id = message["chat"]["id"]
        file_path = os.path.join(settings.STATIC_ROOT, "gimn_inha_by_shirin.mp3")
        file = open(file_path, "rb")
        self.bot.send_voice(current_chat_id, file)





