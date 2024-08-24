import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValueCovector
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Чтобы начать работу введите команду боту в слудеющем формате:\n"
                                      f"<Имя валюты>\n"
                                      f"<В какую валюту перевести>\n"
                                      f"<Количество переводимой валюты>\n"
                                      f"Увидеть список доступных валют: /values"
                     )


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    message.text = message.text.lower()

    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException(f'Неверное количество параметров!\nПомощь /help')

        quote, baze, amount = values
        total_baze = ValueCovector.convert(quote, baze, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {baze} равна {total_baze}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
