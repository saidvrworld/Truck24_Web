
import telebot
from flask import Flask, request


token = "309803225:AAEfkOtjUfLCTSHicJD05uy7AvilTCkzOYs"

bot = telebot.TeleBot(token)

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

#@server.route("/bot", methods=['POST'])
def getMessage(request1=None):
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/bot/hook")
def webhook(request):
    bot.remove_webhook()
    bot.set_webhook(url="https://favorittaxi.herokuapp.com/bot")
    return "!", 200



#server.run(debug=True,use_reloader=True)


