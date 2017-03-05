#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot


class BotManager:


    balance = {"баланс":"*100#","последняя оплата":"*171*1*2#","мой расход":"*171*1*3#","мой номер":"*150#","все мои номера":"*151#"}
    internet_paket ={"300 Mb 👉👉👉 5💲":"*171*019*1*010100342*1#","500 Mb 👉👉👉 7💲":"*171*019*7*010100342*1#",
                     "1000 Mb 👉👉👉 10💲":"*171*019*2*010100342*1#","2000 Mb 👉👉👉 18💲":"*171*019*5*010100342*1#","3000 Mb 👉👉👉 25💲":"*171*019*3*010100342*1#",
                     "5000 Mb 👉👉👉 35💲": "*171*019*4*010100342*1#","10000 Mb 👉👉👉 55💲": "*171*019*6*010100342*1#",
                     "ОСТАТОК ТРАФИКА":"*171*019#"}

    nochnoy_internet_paket = {"ночь 1000 Mb 👉👉👉 2💲":"*171*203*1000*010100342*1#","ночь 2000 Mb 👉👉👉 3,5💲":"*171*203*2000*010100342*1#","ночь 3000 Mb 👉👉👉 5💲":"*171*203*3000*010100342*1#","ночь 5000 Mb 👉👉👉 7💲":"*171*203*5000*010100342*1#",
                              "ночь 10000 Mb 👉👉👉 10💲":"*171*203*10000*010100342*1#","ночь 20000 Mb 👉👉👉 15💲":"*171*203*20000*010100342*1#","ночь 50000 Mb 👉👉👉 20💲":"*171*203*50000*010100342*1#","ОСТАТОК НОЧНОГО ТРАФИКА":"*203#"}

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
            elif(call_data == "мой баланс"):
                self.BalanceMenu(message)
            elif(call_data=="интернет-пакеты"):
                self.InternetPaketMenu(message)
            elif(call_data=="ночной интернет пакет"):
                self.NochnoyInternetPaketMenu(message)

            elif(call_data in self.internet_paket.keys()):
                self.SendContact(call,self.internet_paket)

            elif (call_data in self.balance.keys()):
                self.SendContact(call, self.balance)

            elif (call_data in self.nochnoy_internet_paket.keys()):
                self.SendContact(call, self.nochnoy_internet_paket)






    def Start(self,message):
        current_chat_id = message["chat"]["id"]
        keyboard = telebot.types.InlineKeyboardMarkup()
        callback_button = telebot.types.InlineKeyboardButton(text="Показать", callback_data="start")
        keyboard.add(callback_button)
        self.bot.send_message(current_chat_id, "Меню услуг", reply_markup=keyboard)

    # вызов меню выбора поездки
    def ShowMainMenu(self,message):
        current_chat_id = message["chat"]["id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="МОЙ БАЛАНС", callback_data="мой баланс")
        button2 = telebot.types.InlineKeyboardButton(text="ИНТЕРНЕТ-ПАКЕТЫ", callback_data="интернет-пакеты")
        button3 = telebot.types.InlineKeyboardButton(text="НОЧНОЙ ИНТЕРНЕТ ПАКЕТ", callback_data="ночной интернет пакет")
        button4 = telebot.types.InlineKeyboardButton(text="НОЧНОЙ DRIVE", callback_data="ночной drive")
        button5 = telebot.types.InlineKeyboardButton(text="МИНИ ИНТЕРНЕТ ПАКЕТЫ", callback_data="мини интернет пакеты")
        button6 = telebot.types.InlineKeyboardButton(text="ТАРИФЫ", callback_data="тарифы")
        button7 = telebot.types.InlineKeyboardButton(text="ОПЦИЯ 'Пакеты Минут!'", callback_data="пакеты минут")


        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)
        keyboard.add(button6)
        keyboard.add(button7)

        self.bot.send_message(current_chat_id, "Главное Меню\n\n\n", reply_markup=keyboard)


    def BalanceMenu(self,message):
        current_chat_id = message["chat"]["id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="БАЛАНС", callback_data="баланс")
        button2 = telebot.types.InlineKeyboardButton(text="ПОСЛЕДНЯЯ ОПЛАТА", callback_data="последняя оплата")
        button3 = telebot.types.InlineKeyboardButton(text="МОЙ РАСХОД", callback_data="мой расход")
        button4 = telebot.types.InlineKeyboardButton(text="МОЙ НОМЕР", callback_data="мой номер")
        button5 = telebot.types.InlineKeyboardButton(text="ВСЕ МОИ НОМЕРА", callback_data="все мои номера")


        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)

        self.bot.send_message(current_chat_id, "Вы выбрали МОЙ БАЛАНС\n\n\n", reply_markup=keyboard)

    def InternetPaketMenu(self,message):
        current_chat_id = message["chat"]["id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="300 Mb 👉👉👉 5💲", callback_data="300 Mb 👉👉👉 5💲")
        button2 = telebot.types.InlineKeyboardButton(text="500 Mb 👉👉👉 7💲", callback_data="500 Mb 👉👉👉 7💲")
        button3 = telebot.types.InlineKeyboardButton(text="1000 Mb 👉👉👉 10💲", callback_data="1000 Mb 👉👉👉 10💲")
        button4 = telebot.types.InlineKeyboardButton(text="2000 Mb 👉👉👉 18💲", callback_data="2000 Mb 👉👉👉 18💲")
        button5 = telebot.types.InlineKeyboardButton(text="3000 Mb 👉👉👉 25💲", callback_data="3000 Mb 👉👉👉 25💲")
        button6 = telebot.types.InlineKeyboardButton(text="5000 Mb 👉👉👉 35💲", callback_data="5000 Mb 👉👉👉 35💲")
        button7 = telebot.types.InlineKeyboardButton(text="10000 Mb 👉👉👉 55💲", callback_data="10000 Mb 👉👉👉 55💲")
        button8 = telebot.types.InlineKeyboardButton(text="ОСТАТОК ТРАФИКА", callback_data="ОСТАТОК ТРАФИКА")

        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)
        keyboard.add(button6)
        keyboard.add(button7)
        keyboard.add(button8)


        self.bot.send_message(current_chat_id, "Вы выбрали ИНТЕРНЕТ ПАКЕТЫ\n\n\n", reply_markup=keyboard)

    def NochnoyInternetPaketMenu(self,message):
        current_chat_id = message["chat"]["id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="ночь 1000 Mb 👉👉👉 2💲", callback_data="ночь 1000 Mb 👉👉👉 2💲")
        button2 = telebot.types.InlineKeyboardButton(text="ночь 2000 Mb 👉👉👉 3,5💲", callback_data="ночь 2000 Mb 👉👉👉 3,5💲")
        button3 = telebot.types.InlineKeyboardButton(text="ночь 3000 Mb 👉👉👉 5💲", callback_data="ночь 3000 Mb 👉👉👉 5💲")
        button4 = telebot.types.InlineKeyboardButton(text="ночь 5000 Mb 👉👉👉 7💲", callback_data="ночь 5000 Mb 👉👉👉 7💲")
        button5 = telebot.types.InlineKeyboardButton(text="ночь 10000 Mb 👉👉👉 10💲", callback_data="ночь 10000 Mb 👉👉👉 10💲")
        button6 = telebot.types.InlineKeyboardButton(text="ночь 20000 Mb 👉👉👉 15💲", callback_data="ночь 20000 Mb 👉👉👉 15💲")
        button7 = telebot.types.InlineKeyboardButton(text="ночь 50000 Mb 👉👉👉 20💲", callback_data="ночь 50000 Mb 👉👉👉 20💲")
        button8 = telebot.types.InlineKeyboardButton(text="ОСТАТОК НОЧНОГО ТРАФИКА", callback_data="ОСТАТОК НОЧНОГО ТРАФИКА")

        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)
        keyboard.add(button6)
        keyboard.add(button7)
        keyboard.add(button8)


        self.bot.send_message(current_chat_id, "Вы выбрали НОЧНОЙ ИНТЕРНЕТ ПАКЕТ\n 🕚Время с 00:00 до 08:00\n\n", reply_markup=keyboard)

    def SendContact(self,call,dict):
        message = call["message"]

        if message:
            current_chat_id = call["message"]["chat"]["id"]
            call_data = call["data"]

            self.bot.send_contact(current_chat_id, dict[call_data], call_data)




