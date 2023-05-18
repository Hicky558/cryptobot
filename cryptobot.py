import datetime
import telebot
import requests
import json
print(datetime.datetime.now())
TOKEN = ""
bot = telebot.TeleBot(TOKEN)

keys = {
    "Доллар": 'USD',
    "Евро": 'EUR',
    "Биткоин": 'BTC',
    "Эфириум": 'ETH',
    "Рубль": 'RUB'

}


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:<имя валюты><в какую валюту перевести> \
         <количество переводимой валюты> Увидеть список доступных валют : /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    if len(message.text.split(' ')) == 3:
        quote, base, amount = message.text.split(' ')
        if not (quote in keys):
            bot.send_message(message.chat.id, f'Неверный запрос')
            return
        if not (base in keys):
            bot.send_message(message.chat.id, f'Неверный запрос')
            return
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        print(r.content)
        total_base = json.loads(r.content)[keys[base]]
        text = f'цена{amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, f'Неверный запрос')
        return


bot.polling()
