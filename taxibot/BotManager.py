#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .CallManager import CallManager
import telebot


class BotManager:

    price_list = "💲  (Кобальт, Ласетти): 1000 сум/км, минимум 8000 сум (5 км. включительно).\n\n💲  Доставка: 1000 сум/км, минимум 7000 сум (5 км. включительно).\n\n💲  Перегон: 2000 сум/км, минимум 20000 сум (5 км. включительно).\n\n💲 Ожидание: 300 сум/минуту. 5 минут бесплатно."

    bot = None
    call_manager = None

    def __init__(self,bot):
        self.bot = bot
        self.call_manager = CallManager()

    # перехватывает все сообщения
    def textManager(self,message):
        current_chat_id = message["chat"]["id"]
        message_text = message["text"]
        current_call = self.call_manager.GetCall(chat_id=current_chat_id)

        if (current_call):
            if (self.call_manager.HasNumber(chat_id=current_chat_id)):

                if (current_call.waiting_for == "number"):
                    self.call_manager.UpdateCall(chat_id=current_chat_id, new_number=message_text)

                elif (current_call.waiting_for == "comments"):

                    if (current_call.type != "Предварительный Заказ"):
                        self.call_manager.UpdateCall(chat_id=current_chat_id, new_details=message_text)
                    else:
                        advanced_time = current_call.details
                        self.call_manager.UpdateCall(chat_id=current_chat_id,
                                                new_details=advanced_time + "//" + message_text)

                self.prepare_for_Send(message)
            elif (self.call_manager.HasAddress(chat_id=current_chat_id) or self.call_manager.HasCoordinates(
                    chat_id=current_chat_id)):

                self.call_manager.UpdateCall(chat_id=current_chat_id, new_details=message_text)
            elif (self.call_manager.HasType(chat_id=current_chat_id)):

                if (current_call.waiting_for == "time"):
                    self.call_manager.UpdateCall(chat_id=current_chat_id, new_details=message_text, new_waiting_for="None")
                    self.RequireLocation(message)
                else:
                    self.call_manager.UpdateCall(chat_id=current_chat_id, new_address=message_text)
                    self.requestPhone(message)
            else:
                self.Start(message)
        else:
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
                self.ChooseTypeOfTour(message)

            elif call_data in ["поездка","перегон","доставка"]:
                self.call_manager.AddCall(new_chat_id=current_chat_id)
                self.call_manager.UpdateCall(chat_id=current_chat_id, new_type=call_data)
                self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id,
                                      text="\n\n\nВы выбрали " + call_data)
                self.RequireLocation(message)

            elif call_data == "Предварительный Заказ":
                self.AdvanceCall(call)

            elif call_data == "cancel":
                self.Cancel(message)
            elif call_data == "price_list":
                self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text=self.price_list)
                self.ChooseTypeOfTour(message)

            elif call_data == "change_number":
                self.ChangeNumber(message)

            elif call_data == "comments":
                self.AddComment(message)
            elif call_data == "send":
                self.SendCall(message)
            elif call_data == "accept_cancel":
                self.AcceptCancel(message=message)
            elif call_data == "accept":
                self.Accept(message=message)
            elif call_data == "cancelCall":
                self.CancelCall(message)

    def Start(self,message):
        current_chat_id = message["chat"]["id"]
        keyboard = telebot.types.InlineKeyboardMarkup()
        callback_button = telebot.types.InlineKeyboardButton(text=" 🏁  Начать", callback_data="start")
        keyboard.add(callback_button)
        self.bot.send_message(current_chat_id, "Нажмите начать чтобы заказать такси", reply_markup=keyboard)

    # вызов меню выбора поездки
    def ChooseTypeOfTour(self,message):
        current_chat_id = message["chat"]["id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        trip_button = telebot.types.InlineKeyboardButton(text="🚖 Поездка", callback_data="поездка")
        ship_button = telebot.types.InlineKeyboardButton(text="🍺 Перегон", callback_data="перегон")
        delivery_button = telebot.types.InlineKeyboardButton(text=" 🚛  Доставка", callback_data="доставка")
        advance_button = telebot.types.InlineKeyboardButton(text=" 🚛  Предварительный Заказ", callback_data="Предварительный Заказ")
        info_button = telebot.types.InlineKeyboardButton(text="💲 Тарифы", callback_data="price_list")

        keyboard.add(trip_button)
        keyboard.add(ship_button)
        keyboard.add(delivery_button)
        keyboard.add(advance_button)
        keyboard.add(info_button)

        self.bot.send_message(current_chat_id, "Выберите тип заказа", reply_markup=keyboard)

    # запрашивает время для предварительного вызова
    def AdvanceCall(self,call):

        current_chat_id = call["message"]["chat"]["id"]
        message_id = call["message"]["message_id"]
        call_data = call["data"]

        self.call_manager.AddCall(new_chat_id=current_chat_id)
        self.call_manager.UpdateCall(chat_id=current_chat_id, new_type=call_data)
        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id,
                              text="\n\n\nВы выбрали " + call_data)
        self.bot.send_message(current_chat_id, "\n Напишите время приезда")
        self.call_manager.UpdateCall(chat_id=current_chat_id, new_waiting_for="time")

    # запрашивет местоположения
    def RequireLocation(self,message):
        current_chat_id = message["chat"]["id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        cancel_button = telebot.types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")

        keyboard.add(cancel_button)

        self.bot.send_message(current_chat_id, "👉 Где вы? \n\n👉 Введите свой адрес или отправте местоположение",
                         reply_markup=keyboard)

    # принимает координаты местоположения
    def get_location(self,message):

        current_chat_id = message["chat"]["id"]
        latitude = message["location"]["latitude"]
        longitude = message["location"]["longitude"]

        self.call_manager.UpdateCall(chat_id=current_chat_id, new_coordinates=(longitude, latitude))
        self.requestPhone(message)

    # показывает кнопку отправки контакта
    def requestPhone(self,message):
        current_chat_id = message["chat"]["id"]

        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = telebot.types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        keyboard.add(button_phone)
        self.bot.send_message(current_chat_id, "Нам нужен ваш номер телефона", reply_markup=keyboard)

    # получает контакт
    def GetContact(self,message):
        current_chat_id = message["chat"]["id"]
        number = message["contact"]["phone_number"]

        self.call_manager.UpdateCall(chat_id=current_chat_id, new_number=number)
        self.prepare_for_Send(message)

    # выводит все данне о заказе с просьбой потверждения отправки
    def prepare_for_Send(self,message):
        current_chat_id = message["chat"]["id"]

        self.bot.send_message(current_chat_id, "Ваш номер " + self.call_manager.GetCall(chat_id=current_chat_id).number,
                         reply_markup=telebot.types.ReplyKeyboardRemove())

        keyboard = telebot.types.InlineKeyboardMarkup()
        send_button = telebot.types.InlineKeyboardButton(text="✔️ Отправить заказ", callback_data="send")
        details_button = telebot.types.InlineKeyboardButton(text="💬 Коментарии", callback_data="comments")
        change_number_button = telebot.types.InlineKeyboardButton(text="📞  Изменить номер",
                                                                  callback_data="change_number")
        cancel_button = telebot.types.InlineKeyboardButton(text="❌  Отменить", callback_data="cancel")

        keyboard.add(send_button)
        keyboard.add(details_button)
        keyboard.add(change_number_button)
        keyboard.add(cancel_button)

        self.bot.send_message(current_chat_id, "Заказ готов к отправке", reply_markup=keyboard)

    # просит пользователя ввести коментарии
    def AddComment(self,message):
        current_chat_id = message["chat"]["id"]

        self.call_manager.SetComments(chat_id=current_chat_id)
        self.bot.send_message(current_chat_id, "Наберите комментарии")

    # просит пользователя ввести новый номер
    def ChangeNumber(self,message):
        current_chat_id = message["chat"]["id"]

        self.call_manager.SetNumber(chat_id=current_chat_id)
        self.bot.send_message(current_chat_id, "Наберите новый номер")

    # меняет статус вызова  в базе данных чтобы он был виден диспетчеру
    def SendCall(self,message):
        current_chat_id = message["chat"]["id"]

        ready_call = self.call_manager.GetCall(chat_id=current_chat_id)
        if self.call_manager.HasAddress(chat_id=current_chat_id):
            self.call_manager.UpdateCall(chat_id=current_chat_id, new_status="new")
        else:
            self.call_manager.UpdateCall(chat_id=current_chat_id, new_status="new", new_isMap="True")

        self.bot.send_message(current_chat_id, "\n Ваш заказ принят,ждите предложений... ⏱")

    # отправляет предложение пользователю
    def SendOffer(self,chat_id, car_type, car_number, arrival_time=None):

        keyboard = telebot.types.InlineKeyboardMarkup()
        accept_button = telebot.types.InlineKeyboardButton(text="✔️ Принять", callback_data="accept")
        cancel_button = telebot.types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancelCall")

        keyboard.add(accept_button)
        keyboard.add(cancel_button)

        if (arrival_time):
            self.bot.send_message(chat_id, "\n🚙 " + car_type + ", " + car_number + "\n 🕚" + arrival_time + " минут",
                             reply_markup=keyboard)
        else:
            self.bot.send_message(chat_id, "\n🚙 " + car_type + ", " + car_number, reply_markup=keyboard)

    # уведомляет пользователя о приезде такси
    def SendArrived(self,chat_id):
        info = self.DriverInfo(chat_id)
        if (info):
            self.bot.send_message(chat_id,
                             "\n\n\n Машина приехала\n 🚙" + info["car_type"] + "\n➡️ номер машины " + info[
                                 "car_number"])
            self.bot.send_contact(chat_id, info["driver_number"], "наш номер")

    # дпные о водителе из бд по chat_id
    def DriverInfo(self,chat_id):
        current_call = self.call_manager.GetCall(chat_id)
        if (current_call):
            driver = current_call.car_set.all()[0]
            return {"car_number": driver.car_number, "car_type": driver.car_type, "time": driver.car_time,
                    "driver_number": driver.driver_number}
        else:
            return None

    # отмена на начальном этапе
    def Cancel(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="отменено ")
        self.call_manager.ResetCall(chat_id=current_chat_id)
        self.ChooseTypeOfTour(message)

    # Отмена после предложения машины
    def CancelCall(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        self.call_manager.RemoveCall(current_chat_id)
        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Ваш заказ отменен!")
        self.ChooseTypeOfTour(message)

    # отмена после принятия вызова(когда машина в пути ) сбрасывает id на 0, но сам заказ остается в бд
    def AcceptCancel(self,message):
        current_chat_id = message["chat"]["id"]

        current_call = self.call_manager.GetCall(chat_id=current_chat_id)
        current_call.status = "accepted_cancel"
        current_call.chat_id = 0
        current_call.save()
        self.bot.send_message(current_chat_id, "Ваш заказ отменен!")


    # последнее потверждение пользователем вызова, машина выезжает за клиентом
    def Accept(self,message):
        current_chat_id = message["chat"]["id"]

        current_call = self.call_manager.GetCall(current_chat_id)
        current_call.status = "accepted"
        current_call.save()

        keyboard = telebot.types.InlineKeyboardMarkup()
        info = self.DriverInfo(current_chat_id)

        cancel_button = telebot.types.InlineKeyboardButton(text="❌ Отменить", callback_data="accept_cancel")
        keyboard.add(cancel_button)
        if (info["time"] == 0):
            self.bot.send_message(message.chat.id,
                             "\n\n\n Ваш заказ принят,машина выехала\n 🚙" + info["car_type"] + "\n➡️ номер машины " +
                             info[
                                 "car_number"])
            self.bot.send_contact(message.chat.id, info["driver_number"], "наш номер", reply_markup=keyboard)
        else:
            self.bot.send_message(message.chat.id,
                             "\n\n\n Ваш заказ принят,машина выехала\n 🚙" + info["car_type"] + "\n➡️ номер машины " +
                             info[
                                 "car_number"] + "\n машина прибудет через " + str(info["time"]) + " минут \n")
            self.bot.send_contact(message.chat.id, info["driver_number"], "номер водителя", reply_markup=keyboard)

    def Help(self,message):
        current_chat_id = message["chat"]["id"]

        self.bot.send_message(current_chat_id, "Обратитесь в наш центр поддержки\n ")
        self.bot.send_contact(current_chat_id, "998977377055", "Служба поддержки")