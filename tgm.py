Narnia='https://web.telegram.org/#/im?p=s1369370434_13651978792243988289'
TOKEN = '686961167:AAFqI7OZ3scrm8Qp-XxO0sN_242aHBnzCmM'

import urllib.request
import time
import telebot   # pip3.6 install --user pyTelegramBotAPI
bot = telebot.TeleBot(TOKEN)


import requests # pip install requests
url = "https://api.telegram.org/bot<686961167:AAFqI7OZ3scrm8Qp-XxO0sN_242aHBnzCmM>/"
 
 
def get_updates_json(request):  
    response = requests.get(request + 'getUpdates')
    return response.json()
 
 
def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id
 
def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response
 
chat_id = get_chat_id(last_update(get_updates_json(url)))
send_mess(chat_id, 'I received your message')



#@bot.message_handler(commands=['start'])
#def start_message(message):
#    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

#@bot.message_handler(content_types=['text'])
#def send_text(message):
#    msg=message.text.upper()
#    comand=msg[0:3] # first 3 letters
#    sym=msg[-6:]   # last 6 letters
#    if comand == 'ASK':
#        bot.send_message(message.chat.id, sym)
#    elif message.text.lower() == 'пока':
#        bot.send_message(message.chat.id, 'Прощай, создатель')
#    else:
#        bot.send_message(message.chat.id, "Я тебя не понимаю.")
#print('ok')
#bot.polling(none_stop=True, interval=1)


#keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
#keyboard1.row('Привет', 'Пока')
#@bot.message_handler(commands=['start'])
#def start_message(message):
#    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
#bot.polling(none_stop=True)


#@bot.message_handler(func=lambda message: True, content_types=['text'])
#def echo_msg(message):
#    bot.send_message(message.chat.id, message.text)
#if __name__ == '__main__':
#    bot.polling(none_stop=True)


#@bot.message_handler(commands=['start', 'help'])    # нужно писать /start
#def send_welcome(message):
#	bot.reply_to(message, "Howdy, how are you doing?")
#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#	bot.reply_to(message, message.text)
#bot.polling()



#@bot.message_handler(content_types=['text'])
#def get_text_messages(message):
#    if message.text.lower() == "привет":
#        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#    elif message.text.lower() == "/help":
#        bot.send_message(message.from_user.id, "Напиши привет")
#    else:
#        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
#bot.polling(none_stop=True, interval=1)







