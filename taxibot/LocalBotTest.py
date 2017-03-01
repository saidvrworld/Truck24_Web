


############################################################################################################
#telegram bot
############################################################################################################



import telebot
from .CallManager import CallManager

token = "309803225:AAEfkOtjUfLCTSHicJD05uy7AvilTCkzOYs"

types_of_tour = {"trip": "поездка", "ship": "перегон", "delivery": "доставка","advance":"Предварительный Заказ"}
price_list = "💲  (Кобальт, Ласетти): 1000 сум/км, минимум 8000 сум (5 км. включительно).\n\n💲  Доставка: 1000 сум/км, минимум 7000 сум (5 км. включительно).\n\n💲  Перегон: 2000 сум/км, минимум 20000 сум (5 км. включительно).\n\n💲 Ожидание: 300 сум/минуту. 5 минут бесплатно."

bot = telebot.TeleBot(token)
call_manager = CallManager()

# вызывает команду старт
@bot.message_handler(commands=['start'])
def Start_command(message):
    Start(message)

# вызывает окно помощи
@bot.message_handler(commands=['help'])
def Help(message):
    bot.send_message(message.chat.id, "Обратитесь в наш центр поддержки\n ")
    bot.send_contact(message.chat.id, "998977377055", "Служба поддержки")



# перехватывает все сообщения
@bot.message_handler(content_types=["text"])
def textManager(message):
    current_call = call_manager.GetCall(chat_id=message.chat.id)
    if (current_call):
        if (current_call.HasNumber()):

            if (current_call.waiting_for == "number"):
                call_manager.UpdateCall(chat_id=message.chat.id, new_number=message.text)
            elif (current_call.waiting_for == "comments"):
                if(current_call.type != "advance"):
                    call_manager.UpdateCall(chat_id=message.chat.id, new_details=message.text)
                else:
                    advanced_time = current_call.details
                    call_manager.UpdateCall(chat_id=message.chat.id, new_details=advanced_time + "//" + message.text)

            prepare_for_Send(message)
        elif (current_call.HasAddress() or current_call.HasCoordinates()):
            call_manager.UpdateCall(chat_id=message.chat.id, new_details=message.text)
        elif (current_call.HasType):
            if(current_call.waiting_for == "time"):
                call_manager.UpdateCall(chat_id=message.chat.id,new_details=message.text,new_waiting_for=None)
                call_manager.UpdateCall(chat_id=message.chat.id,new_waiting_for="None")
                RequireLocation(message)
            else:
               call_manager.UpdateCall(chat_id=message.chat.id, new_address=message.text)
               getPhone(message)
        else:
            Start(message)
    else:
        Start(message)




# Ждет и обрабатывает сообщения
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "start":
            ChooseTypeOfTour(call.message)

        elif call.data in ["trip", "ship", "delivery"]:
            call_manager.AddCall(new_chat_id=call.message.chat.id)
            call_manager.UpdateCall(chat_id=call.message.chat.id, new_type=call.data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="\n\n\nВы выбрали " + types_of_tour[call.data])
            RequireLocation(call.message)

        elif call.data == "advance":
            AdvanceCall(call)

        elif call.data == "cancel":
             Cancel(call.message)
        elif call.data == "price_list":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=price_list)
            ChooseTypeOfTour(call.message)

        elif call.data == "change_number":
            ChangeNumber(call.message)

        elif call.data == "comments":
            AddComment(call.message)
        elif call.data == "send":
            SendCall(call.message)
        elif call.data == "accept_cancel":
            AcceptCancel(message = call.message)
        elif call.data == "accept":
            Accept(message=call.message)
        elif call.data == "cancelCall":
            CancelCall(call.message)


@bot.message_handler()
def Start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    callback_button = telebot.types.InlineKeyboardButton(text=" 🏁  Начать", callback_data="start")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Нажмите начать чтобы заказать такси", reply_markup=keyboard)


# вызов меню выбора поездки
@bot.message_handler()
def ChooseTypeOfTour(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    trip_button = telebot.types.InlineKeyboardButton(text="🚖 Поездка", callback_data="trip")
    ship_button = telebot.types.InlineKeyboardButton(text="🍺 Перегон", callback_data="ship")
    delivery_button = telebot.types.InlineKeyboardButton(text=" 🚛  Доставка", callback_data="delivery")
    advance_button = telebot.types.InlineKeyboardButton(text=" 🚛  Предварительный Заказ", callback_data="advance")
    info_button = telebot.types.InlineKeyboardButton(text="💲 Тарифы", callback_data="price_list")

    keyboard.add(trip_button)
    keyboard.add(ship_button)
    keyboard.add(delivery_button)
    keyboard.add(advance_button)
    keyboard.add(info_button)

    bot.send_message(message.chat.id, "Выберите тип заказа", reply_markup=keyboard)


# запрашивает время для предварительного вызова
@bot.message_handler()
def AdvanceCall(call):
    call_manager.AddCall(new_chat_id=call.message.chat.id)
    call_manager.UpdateCall(chat_id=call.message.chat.id, new_type=call.data)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="\n\n\nВы выбрали " + types_of_tour[call.data])
    bot.send_message(call.message.chat.id, "\n Напишите время приезда")
    call_manager.UpdateCall(chat_id=call.message.chat.id,new_waiting_for="time")



# запрашивет местоположения
@bot.message_handler()
def RequireLocation(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    cancel_button = telebot.types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")

    keyboard.add(cancel_button)

    bot.send_message(message.chat.id, "👉 Где вы? \n\n👉 Введите свой адрес или отправте местоположение",
                     reply_markup=keyboard)


# принимает координаты местоположения
@bot.message_handler(content_types=["location"])
def get_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    call_manager.UpdateCall(chat_id=message.chat.id, new_coordinates=(longitude, latitude))
    getPhone(message)


# показывает кнопку отправки контакта
@bot.message_handler()
def getPhone(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = telebot.types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, "Нам нужен ваш номер телефона", reply_markup=keyboard)

# получает контакт
@bot.message_handler(content_types=["contact"])
def GetContact(message):
    call_manager.UpdateCall(chat_id=message.chat.id, new_number=message.contact.phone_number)
    prepare_for_Send(message)

# выводит все данне о заказе с просьбой потверждения отправки
@bot.message_handler()
def prepare_for_Send(message):
    bot.send_message(message.chat.id, "Ваш номер " + call_manager.GetCall(chat_id=message.chat.id).number,
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    keyboard = telebot.types.InlineKeyboardMarkup()
    send_button = telebot.types.InlineKeyboardButton(text="✔️ Отправить заказ", callback_data="send")
    details_button = telebot.types.InlineKeyboardButton(text="💬 Коментарии", callback_data="comments")
    change_number_button = telebot.types.InlineKeyboardButton(text="📞  Изменить номер", callback_data="change_number")
    cancel_button = telebot.types.InlineKeyboardButton(text="❌  Отменить", callback_data="cancel")

    keyboard.add(send_button)
    keyboard.add(details_button)
    keyboard.add(change_number_button)
    keyboard.add(cancel_button)

    ready_call = call_manager.GetCall(chat_id=message.chat.id)
    bot.send_message(message.chat.id, "Заказ готов к отправке", reply_markup=keyboard)

# просит пользователя ввести коментарии
@bot.message_handler()
def AddComment(message):
    call_manager.SetComments(chat_id=message.chat.id)
    bot.send_message(message.chat.id, "Наберите комментарии")

# просит пользователя ввести новый номер
@bot.message_handler()
def ChangeNumber(message):
    call_manager.SetNumber(chat_id=message.chat.id)
    bot.send_message(message.chat.id, "Наберите новый номер")

# добавьляет вызов в базу данных
@bot.message_handler()
def SendCall(message):
    ready_call = call_manager.GetCall(chat_id=message.chat.id)
    if ready_call.HasAddress():
        AddCall(user_chat_id=message.chat.id, user_address=ready_call.address, user_number=ready_call.number,
                      journey_type=types_of_tour[ready_call.type], comments=ready_call.details)
    else:
        AddCall(user_chat_id=message.chat.id, user_coordinates=(ready_call.longitude, ready_call.latitude),
                      user_number=ready_call.number, journey_type=types_of_tour[ready_call.type],
                      comments=ready_call.details)

    call_manager.RemoveCall(chat_id=message.chat.id)
    bot.send_message(message.chat.id, "\n Ваш заказ принят,ждите предложений... ⏱")

# отправляет предложение пользователю
@bot.message_handler()
def SendOffer(chat_id,car_type,car_number,arrival_time=None):
    keyboard = telebot.types.InlineKeyboardMarkup()
    accept_button = telebot.types.InlineKeyboardButton(text="✔️ Принять", callback_data="accept")
    cancel_button = telebot.types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancelCall")


    keyboard.add(accept_button)
    keyboard.add(cancel_button)


    if(arrival_time):
         bot.send_message(chat_id, "\n🚙 "+car_type+", "+car_number+"\n 🕚"+arrival_time+" минут",reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "\n🚙 " + car_type + ", " + car_number,reply_markup=keyboard)

# уведомляет пользователя о приезде такси
@bot.message_handler()
def SendArrived(chat_id):
    info = DriverInfo(chat_id)
    if(info):
          bot.send_message(chat_id,
                     "\n\n\n Машина приехала\n 🚙" + info["car_type"] + "\n➡️ номер машины " + info["car_number"])
          bot.send_contact(chat_id, info["driver_number"], "наш номер")

# отмена на начальном этапе
@bot.message_handler()
def Cancel(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="отменено ")
    call_manager.RemoveCall(chat_id=message.chat.id)
    ChooseTypeOfTour(message)


# Отмена после предложения машины
@bot.message_handler()
def CancelCall(message):
    RemoveCall(message.chat.id)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Ваш заказ отменен")
    ChooseTypeOfTour(message)

# Отмена после потверждения вызова и когда водитель уже в пути
@bot.message_handler()
def AcceptCancel(message):
    AcceptCancelCall(message.chat.id)
    bot.send_message(message.chat.id,"Ваш заказ отменен!")

# последнее потверждение пользователем вызова, машина выезжает за клиентом
@bot.message_handler()
def Accept(message):
    AcceptCall(message.chat.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    info = DriverInfo(message.chat.id)

    cancel_button = telebot.types.InlineKeyboardButton(text="❌ Отменить", callback_data="accept_cancel")
    keyboard.add(cancel_button)
    if(info["time"]==0):
          bot.send_message(message.chat.id, "\n\n\n Ваш заказ принят,машина выехала\n 🚙"+info["car_type"]+"\n➡️ номер машины "+info[
              "car_number"])
          bot.send_contact(message.chat.id, info["driver_number"], "наш номер", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "\n\n\n Ваш заказ принят,машина выехала\n 🚙" + info["car_type"] + "\n➡️ номер машины " + info[
            "car_number"] + "\n машина прибудет через "+str(info["time"])+" минут \n")
        bot.send_contact(message.chat.id, info["driver_number"], "номер водителя", reply_markup=keyboard)



def StartBot():
        p = multiprocessing.Process(target=BotRun())
        p.start()

def BotRun():
    bot.polling(none_stop=True)

############################################################################################################


