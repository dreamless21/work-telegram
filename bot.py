import telebot
from telebot import types
from config import TOKEN, ADMIN_CHAT_ID
from botfunction import insert_proc, report_for_date


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello_message(msg):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    Catalog = types.KeyboardButton('Catalog \U0001F381')
    Profil = types.KeyboardButton('My profile \U0001F6B9')
    FAQ = types.KeyboardButton('FAQ')
    markup.add(Catalog, Profil, FAQ)
    if msg.chat.id == ADMIN_CHAT_ID:
        bot_info = types.KeyboardButton('Bot Info 🗿')
        mailing = types.KeyboardButton('Mailing 📢')
        markup.add(bot_info, mailing)
    bot.send_message(msg.chat.id, 'Hello \U0000270A', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == 'Buy \U0001F381')
def answer_to_buy(msg):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rock_with_eyes = types.KeyboardButton('Rock with eyes')
    back = types.KeyboardButton('Back')
    markup.add(rock_with_eyes, back)
    bot.send_message(msg.chat.id, 'What are you want to buy?', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == 'Rock with eyes')
def buy_rock(msg):
    bot.send_photo(msg.chat.id, 'https://ucarecdn.com/e3c749ec-5426-40f9-9060-20f7a236cb4b/', 'Good: Rock\nPrice: 1000$\nIn stock: 2')


@bot.message_handler(func=lambda msg: msg.text == 'Back')
def buy_return(msg):
    hello_message(msg)


@bot.message_handler(commands=['button'])
def button_message(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('current ethereum price')
    item2 = types.KeyboardButton('Лучше воздержись')
    item3 = types.KeyboardButton('Отчет меню по дням')
    item4 = types.KeyboardButton('Внести меню и оценки')
    markup.add(item1, item2, item3, item4)
    bot.send_message(msg.chat.id, 'Че хотите?', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(msg):
    if msg.text == 'current ethereum price':
        bot.send_message(msg.chat.id, 'binance.com')

    elif msg.text == 'Отчет меню по дням':
        bot.send_message(msg.chat.id, 'Введите даты для получения отчета через пробел')
        bot.register_next_step_handler(msg, callback=report_for_date)

    elif msg.text == 'Внести меню и оценки':
        bot.send_message(msg.chat.id, 'Введите позиции свое имя, названия блюд, их оценки и дату через пробел\n'
                                      'Например:\nNikita;2022-03-25;Борщ;4;Винегрет;3;Мясо;4;Пюре;5')
        bot.register_next_step_handler(msg, callback=insert_proc)

    else:
        with open(r'C:\Users\fokin.ni\PycharmProjects\work-telegram\tmp\aaa.jpg', 'rb') as file:
            bot.send_photo(msg.chat.id, file)


if __name__ == '__main__':
    bot.infinity_polling()
