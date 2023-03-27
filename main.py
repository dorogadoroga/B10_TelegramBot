import telebot
from config import TOKEN, currency
from extensions import APIException, ConvertTest

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_message(message: telebot.types.Message):
    text = 'Добро пожаловать в Бот конвертации валют. ' \
           '\n\nВведите информацию в следующем формате: <конвертируемая валюта> <в какую валюту перевести> <количество переводимой валюты>' \
           '\n\nДоступные команды:' \
           '\n/start, /help - список доступных функций ' \
           '\n/values - список доступных для конвертации валют'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for key in currency.keys():
        text += f'\n{key}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Введено неверное количество параметров')
        base, quote, amount = values
        result = ConvertTest.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {base} = {result} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()
