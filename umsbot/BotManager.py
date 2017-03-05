#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot


class BotManager:

    price_list = "💲  (Кобальт, Ласетти): 1000 сум/км, минимум 8000 сум (5 км. включительно).\n\n💲  Доставка: 1000 сум/км, минимум 7000 сум (5 км. включительно).\n\n💲  Перегон: 2000 сум/км, минимум 20000 сум (5 км. включительно).\n\n💲 Ожидание: 300 сум/минуту. 5 минут бесплатно."

    balance = {"баланс":"*100#","последняя оплата":"*171*1*2#","мой расход":"*171*1*3#","мой номер":"*150#","все мои номера":"*151#"}

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
            elif(call_data in self.balance.keys()):
                self.bot.send_contact(current_chat_id, self.balance[call_data], call_data)




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

        self.bot.send_message(current_chat_id, "Главное Меню", reply_markup=keyboard)


    def Balance(self,message):
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

        self.bot.send_message(current_chat_id, "Вы выбрали МОЙ БАЛАНС", reply_markup=keyboard)


