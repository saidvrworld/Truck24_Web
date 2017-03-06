#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot


class BotManager:


    balance = {"баланс":"*100#","последняя оплата":"*171*1*2#","мой расход":"*171*1*3#","мой номер":"*150#","все мои номера":"*151#"}
    internet_paket ={"300 Mb 👉👉👉 5💲":"*171*019*1*010100342*1#","500 Mb 👉👉👉 7💲":"*171*019*7*010100342*1#",
                     "1000 Mb 👉👉👉 10💲":"*171*019*2*010100342*1#","2000 Mb 👉👉👉 18💲":"*171*019*5*010100342*1#","3000 Mb 👉👉👉 25💲":"*171*019*3*010100342*1#",
                     "5000 Mb 👉👉👉 35💲": "*171*019*4*010100342*1#","10000 Mb 👉👉👉 55💲": "*171*019*6*010100342*1#",
                     "ОСТАТОК ТРАФИКА":"*171*019#"}

    nochnoy_internet_paket = {"ночь 1000 Mb 👉2💲":"*171*203*1000*010100342*1#","ночь 2000 Mb 👉3,5💲":"*171*203*2000*010100342*1#","ночь 3000 Mb 👉5💲":"*171*203*3000*010100342*1#","ночь 5000 Mb 👉7💲":"*171*203*5000*010100342*1#",
                              "ночь 10000 Mb 👉10💲":"*171*203*10000*010100342*1#","ночь 20000 Mb 👉15💲":"*171*203*20000*010100342*1#","ночь 50000 Mb 👉20💲":"*171*203*50000*010100342*1#","ОСТАТОК НОЧНОГО ТРАФИКА":"*203#"}

    nochnoy_drive = {"1 сутка 👉3💲":"*171*200*1*010100342*1#","7 суток 👉15💲":"*171*200*7*010100342*1#","30 суток 👉40💲":"*171*200*30*010100342*1#"}

    mini_internet_paket = {"50 Mb 👉1,5💲":"*171*204*50*010100342*1#","100 Mb 👉2,5💲":"*171*204*100*010100342*1#"}

    tarif_price ={"TERMINAL👉$3/месяц":"*171*112*010100342*1#","OPTIMA 333👉$6/месяц":"*171*333*010100342*1#","555👉$8/месяц":"*171*555*010100342*1#","777👉$10/месяц":"*171*777*010100342*1#","MAXI NEW👉$15/месяц":"*171*105*010100342*1#",
                  "ULTRA👉$25/месяц":"*171*103*010100342*1#","Perfect👉$35/месяц":"*171*111*010100342*1#","Baraka👉$0,20/день":"*171*109*010100342*1#"}

    paket_minut = {"120 минут👉$1,8":"*171*103*120*1*010100342*1#","180 минут👉$2,5":"*171*103*180*1*010100342*1#","300 минут👉$4,0":"*171*103*300*1*010100342*1#","ПРОВЕРИТЬ ОСТАТОК ПАКЕТА":"*103#"}

    paket_sms = {"SMS 100👉$1":"*111*018*1#","SMS 300👉$2,4":"*111*018*2#","ПРОВЕРИТЬ ОСТАТОК CМС ПАКЕТА":"*111*018#",}

    uslugi_info = {"МОБИЛЬНЫЙ ИНТЕРНЕТ ВКЛЮЧЕНИЕ":"*111*0011#","МОБИЛНЫЙ ИНТЕРНЕТ ОТКЛЮЧЕНИЕ":"*111*0010#","МЕЖДУНАРОДНЫЕ ЗВОНКИ ВКЛЮЧИТЬ":"*111*0021#","МЕЖДУНАРОДНЫЕ ЗВОНКИ ОТКЛЮЧИТЬ":"*111*0020#",
                   "FAMILY включить":"*111*0031#","FAMILY отключить":"*111*0030#","ЗАПРЕТ РАССЫЛОК ВКЛЮЧИТЬ":"*111*0271#","ЗАПРЕТ РАССЫЛОК ОТКЛЮЧИТЬ":"*111*0271#","SUPER 0":"*166#"}

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
            elif(call_data=="ночной drive"):
                self.NochnoyDrive(message)
            elif (call_data == "мини интернет пакеты"):
                self.MiniInternetPaketMenu(message)
            elif (call_data == "тарифы"):
                self.Tarif(message)
            elif (call_data == "пакеты минут"):
                self.PaketMinut(message)
            elif (call_data == "смс пакеты"):
                self.SMSPaket(message)
            elif (call_data == "услуги"):
                self.Uslugi(message)

            elif(call_data in self.internet_paket.keys()):
                self.SendContact(call,self.internet_paket)

            elif (call_data in self.balance.keys()):
                self.SendContact(call, self.balance)

            elif (call_data in self.nochnoy_internet_paket.keys()):
                self.SendContact(call, self.nochnoy_internet_paket)

            elif (call_data in self.nochnoy_drive.keys()):
                self.SendContact(call, self.nochnoy_drive)

            elif (call_data in self.mini_internet_paket.keys()):
                self.SendContact(call, self.mini_internet_paket)

            elif (call_data in self.tarif_price.keys()):
                self.SendContact(call, self.tarif_price)

            elif (call_data in self.paket_minut.keys()):
                self.SendContact(call, self.paket_minut)

            elif (call_data in self.paket_sms.keys()):
                self.SendContact(call, self.paket_sms)

            elif (call_data in self.uslugi_info.keys()):
                self.SendContact(call, self.uslugi_info)







    def Start(self,message):
        current_chat_id = message["chat"]["id"]
        keyboard = telebot.types.InlineKeyboardMarkup()
        callback_button = telebot.types.InlineKeyboardButton(text="Показать", callback_data="start")
        keyboard.add(callback_button)
        self.bot.send_message(current_chat_id, "Меню услуг", reply_markup=keyboard)

    # вызов меню выбора поездки
    def ShowMainMenu(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="МОЙ БАЛАНС", callback_data="мой баланс")
        button2 = telebot.types.InlineKeyboardButton(text="ИНТЕРНЕТ-ПАКЕТЫ", callback_data="интернет-пакеты")
        button3 = telebot.types.InlineKeyboardButton(text="НОЧНОЙ ИНТЕРНЕТ ПАКЕТ", callback_data="ночной интернет пакет")
        button4 = telebot.types.InlineKeyboardButton(text="НОЧНОЙ DRIVE", callback_data="ночной drive")
        button5 = telebot.types.InlineKeyboardButton(text="МИНИ ИНТЕРНЕТ ПАКЕТЫ", callback_data="мини интернет пакеты")
        button6 = telebot.types.InlineKeyboardButton(text="ТАРИФЫ", callback_data="тарифы")
        button7 = telebot.types.InlineKeyboardButton(text="ОПЦИЯ 'Пакеты Минут!'", callback_data="пакеты минут")
        button8 = telebot.types.InlineKeyboardButton(text="СМС Пакеты", callback_data="смс пакеты")
        button9 = telebot.types.InlineKeyboardButton(text="УСЛУГИ", callback_data="услуги")




        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)
        keyboard.add(button6)
        keyboard.add(button7)
        keyboard.add(button8)
        keyboard.add(button9)


        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Главное Меню\n\n\n",reply_markup=keyboard)


    def BalanceMenu(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]


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

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Вы выбрали МОЙ БАЛАНС\n\n\n",reply_markup=keyboard)

    def InternetPaketMenu(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]


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

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Вы выбрали ИНТЕРНЕТ ПАКЕТЫ\n\n\n",reply_markup=keyboard)

    def NochnoyInternetPaketMenu(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]


        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="ночь 1000 Mb 👉2💲", callback_data="ночь 1000 Mb 👉2💲")
        button2 = telebot.types.InlineKeyboardButton(text="ночь 2000 Mb 👉3,5💲", callback_data="ночь 2000 Mb 👉3,5💲")
        button3 = telebot.types.InlineKeyboardButton(text="ночь 3000 Mb 👉5💲", callback_data="ночь 3000 Mb 👉5💲")
        button4 = telebot.types.InlineKeyboardButton(text="ночь 5000 Mb 👉7💲", callback_data="ночь 5000 Mb 👉7💲")
        button5 = telebot.types.InlineKeyboardButton(text="ночь 10000 Mb 👉10💲", callback_data="ночь 10000 Mb 👉10💲")
        button6 = telebot.types.InlineKeyboardButton(text="ночь 20000 Mb 👉15💲", callback_data="ночь 20000 Mb 👉15💲")
        button7 = telebot.types.InlineKeyboardButton(text="ночь 50000 Mb 👉20💲", callback_data="ночь 50000 Mb 👉20💲")
        button8 = telebot.types.InlineKeyboardButton(text="ОСТАТОК НОЧНОГО ТРАФИКА", callback_data="ОСТАТОК НОЧНОГО ТРАФИКА")

        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)
        keyboard.add(button6)
        keyboard.add(button7)
        keyboard.add(button8)

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Вы выбрали НОЧНОЙ ИНТЕРНЕТ ПАКЕТ\n 🕚Время с 00:00 до 08:00\n\n",reply_markup=keyboard)

    def NochnoyDrive(self, message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="1 сутка 👉3💲", callback_data="1 сутка 👉3💲")
        button2 = telebot.types.InlineKeyboardButton(text="7 суток 👉15💲", callback_data="7 суток 👉15💲")
        button3 = telebot.types.InlineKeyboardButton(text="30 суток 👉40💲", callback_data="30 суток 👉40💲")


        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)


        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id,
                                   text="Вы выбрали НОЧНОЙ DRIVE\n 🕚Время с 00:00 до 08:00\n\n",
                                   reply_markup=keyboard)


    def MiniInternetPaketMenu(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]


        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="50 Mb 👉1,5💲", callback_data="50 Mb 👉1,5💲")
        button2 = telebot.types.InlineKeyboardButton(text="100 Mb 👉2,5💲", callback_data="100 Mb 👉2,5💲")


        keyboard.add(button1)
        keyboard.add(button2)


        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="Вы выбрали МИНИ ИНТЕРНЕТ ПАКЕТЫ\n 🕚Срок действия всех мини интернет пакетов 1 сутки\n\n",reply_markup=keyboard)


    def Tarif(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]


        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="TERMINAL👉$3/месяц", callback_data="TERMINAL👉$3/месяц")
        button2 = telebot.types.InlineKeyboardButton(text="OPTIMA 333👉$6/месяц", callback_data="OPTIMA 333👉$6/месяц")
        button3 = telebot.types.InlineKeyboardButton(text="555👉$8/месяц", callback_data="555👉$8/месяц")
        button4 = telebot.types.InlineKeyboardButton(text="777👉$10/месяц", callback_data="777👉$10/месяц")
        button5 = telebot.types.InlineKeyboardButton(text="MAXI NEW👉$15/месяц", callback_data="MAXI NEW👉$15/месяц")
        button6 = telebot.types.InlineKeyboardButton(text="ULTRA👉$25/месяц", callback_data="ULTRA👉$25/месяц")
        button7 = telebot.types.InlineKeyboardButton(text="Perfect👉$35/месяц", callback_data="Perfect👉$35/месяц")
        button8 = telebot.types.InlineKeyboardButton(text="Baraka👉$0,20/день", callback_data="Baraka👉$0,20/день")

        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)
        keyboard.add(button6)
        keyboard.add(button7)
        keyboard.add(button8)

        perfect = "Рекомендуем смену тарифа в начале месяца так как Первоначальный авансовый платеж при подключении на тарифный план «Perfect» $35 (размер абонентской платы в полном объеме); не зависимо от того, какого числа месяца производится подключение на тарифный план"
        baraka = "Для новых и существующих абонентов Андижанской, Наманганской, Ферганской, Хорезмской, Кашкадарьинской, Бухарской, Сырдарьинской, Джизакской, Навоийской, Сурхандарьинская областей, г. Чирчик, г. Янгиюль и Республики Каракалпакстан.\n Ежедневная абонентская плата – всего $0,20 в день!\n20 минут ежедневно на исходящие звонки по Узбекистану\n20 SMS ежедневно по Узбекистану·\nВходящие звонки $0\nБонус за пополнение - 20 Мегабайт при разовом пополнении баланса на сумму от$ 2\n"

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="👉на тарифном плане ОПТИМА 333 за «Super 0» есть абон плата $ 1 \n👉на трифном плане 555 за «Super 0» есть абон плата $ 1\n👉абон плата снимается за каждые 30 дней.\n 👇ТАРИФ Perfect👇\n "+perfect+"\n 👇Тариф Baraka👇\n"+baraka,reply_markup=keyboard)


    def PaketMinut(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]


        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="120 минут👉$1,8", callback_data="120 минут👉$1,8")
        button2 = telebot.types.InlineKeyboardButton(text="180 минут👉$2,5", callback_data="180 минут👉$2,5")
        button3 = telebot.types.InlineKeyboardButton(text="300 минут👉$4,0", callback_data="300 минут👉$4,0")
        button4 = telebot.types.InlineKeyboardButton(text="ПРОВЕРИТЬ ОСТАТОК ПАКЕТА", callback_data="ПРОВЕРИТЬ ОСТАТОК ПАКЕТА")


        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="'Пакет 120 минут', 'Пакет 180 минут' и 'Пакет 300 минут' исходящих вызовов внутри сети, на номера других мобильных операторов и на городские номера по очень выгодной цене.\nМинуты по Узбекистану на все компании. Срок действия пакета - 30 календарных дней с момента активации\n\n",reply_markup=keyboard)


    def SMSPaket(self,message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]


        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="SMS 100👉$1", callback_data="SMS 100👉$1")
        button2 = telebot.types.InlineKeyboardButton(text="SMS 300👉$2,4", callback_data="SMS 300👉$2,4")
        button3 = telebot.types.InlineKeyboardButton(text="ПРОВЕРИТЬ ОСТАТОК CМС ПАКЕТА", callback_data="ПРОВЕРИТЬ ОСТАТОК CМС ПАКЕТА")


        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)

        sms_info = "Услуга «SMS-пакеты» позволяет абонентам подключать на свои номера пакеты SMS-сообщений по выгодным ценам. «SMS-пакеты» включают в себя различное количество SMS-сообщений, которое можно использовать для отправки сообщений абонентам компаний мобильной связи Узбекистана."

        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id, text="\n"+sms_info+"\nСтоимость пакета снимается при активации.\nСрок действия пакета - 30 календарных дней с момента активации",reply_markup=keyboard)

    def Uslugi(self, message):
        current_chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="МОБИЛЬНЫЙ ИНТЕРНЕТ ВКЛЮЧЕНИЕ", callback_data="МОБИЛЬНЫЙ ИНТЕРНЕТ ВКЛЮЧЕНИЕ")
        button2 = telebot.types.InlineKeyboardButton(text="МОБИЛНЫЙ ИНТЕРНЕТ ОТКЛЮЧЕНИЕ", callback_data="МОБИЛНЫЙ ИНТЕРНЕТ ОТКЛЮЧЕНИЕ")
        button3 = telebot.types.InlineKeyboardButton(text="МЕЖДУНАРОДНЫЕ ЗВОНКИ ВКЛЮЧИТЬ", callback_data="МЕЖДУНАРОДНЫЕ ЗВОНКИ ВКЛЮЧИТЬ")
        button4 = telebot.types.InlineKeyboardButton(text="МЕЖДУНАРОДНЫЕ ЗВОНКИ ОТКЛЮЧИТЬ", callback_data="МЕЖДУНАРОДНЫЕ ЗВОНКИ ОТКЛЮЧИТЬ")
        button5 = telebot.types.InlineKeyboardButton(text="FAMILY включить", callback_data="FAMILY включить")
        button6 = telebot.types.InlineKeyboardButton(text="FAMILY отключить", callback_data="FAMILY отключить")
        button7 = telebot.types.InlineKeyboardButton(text="ЗАПРЕТ РАССЫЛОК ВКЛЮЧИТЬ", callback_data="ЗАПРЕТ РАССЫЛОК ВКЛЮЧИТЬ")
        button8 = telebot.types.InlineKeyboardButton(text="ЗАПРЕТ РАССЫЛОК ОТКЛЮЧИТЬ", callback_data="ЗАПРЕТ РАССЫЛОК ОТКЛЮЧИТЬ")
        button9 = telebot.types.InlineKeyboardButton(text="SUPER 0", callback_data="SUPER 0")


        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)
        keyboard.add(button5)
        keyboard.add(button6)
        keyboard.add(button7)
        keyboard.add(button8)
        keyboard.add(button9)



        self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id,
                                   text="Вы выбрали Услуги",
                                   reply_markup=keyboard)

    def SendContact(self,call,dict):
        message = call["message"]
        message_id = message["message_id"]


        if message:
            current_chat_id = call["message"]["chat"]["id"]
            call_data = call["data"]
            self.bot.edit_message_text(chat_id=current_chat_id, message_id=message_id,
                                       text="код для выполнения действия\n call_data\ndict[call_data]\n")

            self.bot.send_contact(current_chat_id, dict[call_data], call_data)




