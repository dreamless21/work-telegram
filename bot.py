import telebot
import re
import time
import requests
import json
import uuid

from telebot import types, util
from config import TOKEN, ADMIN_CHAT_ID
from botfunction import insert_proc, report_for_date_mysql
from random import shuffle, randint, choice
from lists import list_of_films, list_of_anime, list_gifts, dic_commands, card_values
from DBconnect import random_select_anime, concrect_select, select_all_anime_titles, get_user_balance, reg_user, \
    balance_update, films_filter, crypto_price_everyday, crypto_des, dice_payInOut
from APIs_testing import get_something, search_anime


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['api'])
def send_gif(msg):
    url = get_something()
    bot.send_video(msg.chat.id, url['results'][0]['url'])

@bot.message_handler(content_types=['photo'])
def save_photo(msg):
    file_id = bot.get_file(msg.photo[0].file_id)
    download_file = bot.download_file(file_id.file_path)
    my_path = f'./tmp/find_anime/{msg.from_user.username}+{msg.id}.jpg'
    with open(my_path, 'wb') as new_file:
        new_file.write(download_file)
    bot.send_message(msg.chat.id, 'Кажется все окей..начинаю поиск..')
    res = ' '.join(search_anime(my_path))
    bot.send_message(msg.chat.id, f'Скорее всего ваше изображение из {res}')

# region Greetings

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_sticker(msg.chat.id, 'CAACAgIAAx0CYG_RBAACASdiWUmPC8cIGuIVLlr6e6GtYqtziAACmQwAAj9UAUrPkwx5a8EilCME')
    bot.send_message(msg.chat.id, f'Привет {msg.from_user.first_name} {msg.from_user.last_name}, тебя приветствует бот - lizadegu \U0001F43F\n\n'
                                  f'На данный момент я нахожусь на этапе разработки, если у вас есть пожелания или идеи,'
                                  f'отправьте тэг /ideas и напишите мне сообщение, я обязательно передам его своему хозяину\n\n'
                                  f'С уже имеющимися функциями вы можете познакомиться нажав /commands')
# endregion

# region Ideas
@bot.message_handler(commands=['ideas'])
def send_idea_for_admin(msg):
    bot.send_message(msg.chat.id, 'Отлично, теперь напиши сообщение с идеей или пожеланием и я сразу передам его в нужное место, жду \U0001F642')
    bot.register_next_step_handler(msg, callback=send_idea)
# endregion

# region Commands
@bot.message_handler(commands=['commands'])
def send_commands(msg):
    for command, description in dic_commands.items():
        bot.send_message(msg.chat.id, f'{command} - {description}')
# endregion

# region Watch
@bot.message_handler(commands=['watch'])
def choose_watch(msg):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='Полнометражные фильмы', callback_data='film'),
               types.InlineKeyboardButton(text='Сериалы', callback_data='serial'),
               types.InlineKeyboardButton(text='Аниме', callback_data='anime'),
               types.InlineKeyboardButton(text='Выход', callback_data='exit'))
    bot.send_message(msg.chat.id, 'Выберите категорию:', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in
                                             ['film', 'anime', 'serial', 'exit'])
def choose_watch(callback):
    if callback.data == 'exit':
        bot.delete_message(callback.message.chat.id, callback.message.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        choose_dic = {
            'film': ['случайный фильм', 'фильмы', 'list_of_films'],
            'anime': ['случайное аниме', 'аниме', 'random_select_anime'],
            'serial': ['случайный сериал', 'сериалы', 'list_of_serial']
        }
        choose_one, choose_two, choose_where = choose_dic[callback.data][0], choose_dic[callback.data][1], \
                                               choose_dic[callback.data][2]
        markup.add(types.InlineKeyboardButton(text=f'Выбрать {choose_one}', callback_data=f'{choose_where}'),
                   types.InlineKeyboardButton(text=f'Отфильтровать {choose_two} по дате', callback_data='filter'),
                   types.InlineKeyboardButton(text=f'Найти {choose_two} по названию', callback_data='find'),
                   types.InlineKeyboardButton(text='Выход', callback_data='exit'))
        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выбирайте далее', reply_markup=markup,
                              message_id=callback.message.id)
# endregion

# region Random selection
@bot.callback_query_handler(func=lambda callback: callback.data in ['random_select_anime'])
def random_selection(callback):
    chooses_dic = {
        'random_select_anime': random_select_anime,
    }
    selection_func = chooses_dic[callback.data]
    mytuple = selection_func()
    name, year, rating, pic, desc = mytuple
    bot.send_photo(callback.message.chat.id, pic)
    bot.send_message(callback.message.chat.id,
                     f'\nНазвание аниме:\n{name}\n\nГод выпуска:\n{year}\n\nРейтинг:\n{rating}\n\nОписание аниме:\n{desc}')
    bot.delete_message(callback.message.chat.id, callback.message.id)
# endregion

# region Filtering
@bot.callback_query_handler(func=lambda callback: callback.data == 'filter')
def year_filter(callback):
    bot.send_message(callback.message.chat.id, 'Введите год')
    bot.register_next_step_handler(callback.message, callback=filtering)


def filtering(msg):
    global year
    year = int(msg.text)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text=f'Фильмы выпущенные в {year} году', callback_data='inThisYear'),
               types.InlineKeyboardButton(text=f'Фильмы выпущенные раньше {year} года', callback_data='beforeThisYear'),
               types.InlineKeyboardButton(text=f'Фильмы выпущенные позже {year} года', callback_data='afterThisYear'))
    bot.send_message(msg.chat.id, 'Выберите тип фильтра:', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ['inThisYear', 'beforeThisYear', 'afterThisYear'])
def send_filtered_films(callback):
    my_list = films_filter(year, callback.data)
    for film in my_list:
        bot.send_message(callback.message.chat.id, film)
# endregion

# region regular expression find
@bot.callback_query_handler(func=lambda callback: callback.data in ['find'])
def regexp_find(callback):
    bot.send_message(callback.message.chat.id, 'Введите часть названия аниме')
    bot.register_next_step_handler(callback.message, callback=regxp)

def regxp(msg):
    list_titles = select_all_anime_titles()
    pattern = msg.text
    for title in list_titles:
        if re.search(r'w*'+pattern+r'\w*', title[0], re.IGNORECASE):
            bot.send_message(msg.chat.id, title[0])
# endregion

# region Free APIs
@bot.message_handler(commands=['getInfoRandomDate'])
def get_date(msg):
    request = requests.get('http://numbersapi.com/random/date?json')
    pydic = json.loads(request.text)
    bot.send_message(msg.chat.id, pydic['text'])


"""
Случайная картинка лисы, совет и лечение от скуки
"""
@bot.message_handler(commands=['random'])
def random(msg):
    image = json.loads(requests.get('https://randomfox.ca/floof/').text)
    activity = json.loads(requests.get('https://www.boredapi.com/api/activity/').text)
    advice = json.loads(requests.get('https://api.adviceslip.com/advice').text)
    bot.send_photo(msg.chat.id, image['image'], f'\n\nIf you bored do this: {activity["activity"]}\n\n'
                                                f'Good advice to you: {advice["slip"]["advice"]}')
# endregion

# region Evaluations
"""
Решение квадратных уравнений
"""
@bot.message_handler(commands=['equation'])
def solution(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(text='Solve equation'))
    bot.send_message(msg.chat.id, 'Что тебя интересует?', reply_markup=markup)
    bot.register_next_step_handler(msg, callback=solve)


def solve(msg):
    bot.reply_to(msg, 'Enter the coefficients a, b, c like: 1 2 3')
    bot.register_next_step_handler(msg, callback=solve1)


def solve1(msg):
    bot.send_message(msg.chat.id, 'Coefficients received, starting equation..')
    a, b, c = map(int, msg.text.split())
    dis = b ** 2 - 4 * a * c
    bot.send_message(msg.chat.id, f'Discriminant is {dis}')
    if dis >= 0:
        x1 = (-b + dis ** 0.5) / (2 * a)
        x2 = (-b - dis ** 0.5) / (2 * a)
        bot.send_message(msg.chat.id, f'Our roots is:\n{x1}, {x2}')
    else:
        bot.send_message(msg.chat.id, 'Equation has no roots')
# endregion

# region decision
"""
Решатель всех вопросов
"""
@bot.message_handler(commands=['decision'])
def get_decider(msg):
    sticker_id = 'CAACAgIAAxkBAAIDy2JVdKDo6qvwEq6kdjDfL0-QsBF3AALTAANWnb0K9TKPl9US-T0jBA'
    bot.send_sticker(msg.chat.id, sticker_id)
    bot.send_message(msg.chat.id, '<b>Вас приветствует Великий Решатель, '
                                  'тайная сущность призванная помогать вам в решениях своих вопросов, '
                                  'для того чтобы задать мне вопрос, напишите его в чат</b>\U0001F9E0', parse_mode='HTML')
    bot.register_next_step_handler(msg, callback=my_decision)
# endregion

# region Playzone
"""
Play
"""
@bot.message_handler(commands=['play'])
def play(msg):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    dice = types.KeyboardButton(text='Dice 🎲')
    # darts = types.KeyboardButton(text='Darts 🎯')
    # slots = types.KeyboardButton(text='Slots 🎰')
    # basket = types.KeyboardButton(text='Basket 🏀')
    # football = types.KeyboardButton(text='Football ⚽')
    # bouling = types.KeyboardButton(text='Bouling 🎳')
    markup.add(dice)
    bot.send_message(msg.chat.id, 'Choose a game', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text in ['Dice 🎲', 'Darts 🎯', 'Slots 🎰', 'Basket 🏀', 'Football ⚽', 'Bouling 🎳', 'Сыграть ещё', 'Выход'])
def start_play(msg):
    if msg.text == 'Выход':
        bot.delete_message(msg.chat.id, msg.id - 1)
    else:
        global balance, telegram_id, balance_message
        play_dic = {
            'Dice 🎲': '🎲',
            'Darts 🎯': '🎯',
            'Slots 🎰': '🎰',
            'Basket 🏀': '🏀',
            'Football ⚽': '⚽',
            'Bouling 🎳': '🎳'
        }
        balance = get_user_balance(msg.from_user.id)
        telegram_id = msg.from_user.id
        if balance is None:
            full_name = f'{msg.from_user.first_name} {msg.from_user.last_name}'
            user_name = msg.from_user.username
            balance = reg_user(telegram_id, full_name, user_name)[0]
        balance_message = bot.send_message(msg.chat.id, f'Твой баланс {balance}')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='10', callback_data='10'),
                   types.InlineKeyboardButton(text='50', callback_data='50'),
                   types.InlineKeyboardButton(text='100', callback_data='100'))
        bot.send_message(msg.chat.id, 'Выбери ставку:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data in ['10', '50', '100', 'moreAndFour', 'lessFour'])
def betting(callback):
    global bet, balance
    if callback.data in ['10', '50', '100']:
        bet = int(callback.data)
        balance = balance - bet
        if balance >= 0:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton(text='Выпадет значение 4 или больше', callback_data='moreAndFour'),
                       types.InlineKeyboardButton(text='Выпадет значение меньше 4', callback_data='lessFour'))
            bot.edit_message_text('Выбери исход:', callback.message.chat.id, callback.message.id, reply_markup=markup)
        else:
            bot.send_message(callback.message.chat.id, 'У вас недостаточно денег для совершения ставки')
    else:
        bet_type_dict = {
            'moreAndFour': 1,
            'lessFour': 2
        }
        trans_id = uuid.uuid4()
        bet_type = bet_type_dict[callback.data]
        dice_payInOut(bet, -1, f'{trans_id}_in', 1, telegram_id, bet_type)
        bot.delete_message(callback.message.chat.id, callback.message.id)
        bot.delete_message(balance_message.chat.id, balance_message.id)
        throw = bot.send_dice(callback.message.chat.id, '🎲')
        value = throw.json['dice']['value']
        time.sleep(5)
        if (callback.data == 'moreAndFour' and value >= 4) or (callback.data == 'lessFour' and value < 4):
            message = 'Ты выиграл'
            balance += 2 * bet
            dice_payInOut(2* bet, 1, f'{trans_id}_out', 1, telegram_id, bet_type, value)
        else:
            message = 'Ты проиграл'

        balance = balance_update(telegram_id, balance)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(text='Сыграть ещё'),
                   types.KeyboardButton(text='Выход'))
        bot.send_message(callback.message.chat.id, f'{message}\n\n'
                                                   f'Твой баланс - {balance}', reply_markup=markup)
# endregion

# region Contact us
"""
Contact us
"""
@bot.message_handler(commands=['contact'])
def contact_us(msg):
    bot.send_message(msg.chat.id, 'Contact with us')
    bot.send_location(msg.chat.id, 59.913749, 30.350741)
    bot.send_contact(msg.chat.id, first_name='Nikita', last_name='Fokin', phone_number='89313062923')
# endregion

# region Polling
"""
Make poll
"""
@bot.message_handler(commands=['poll'])
def create_poll(msg):
    bot.send_message(msg.chat.id, 'For start poll, send me question and choices like: "Who will win \n\nelections in Russia in 2024? '
                                  'Putin, Medvedev, Navalny, Kirkorov')
    bot.register_next_step_handler(msg, callback=make_poll)


def make_poll(msg):
    question = msg.text[:msg.text.index('?') + 1]
    answers = msg.text[msg.text.index('?') + 2:].split(', ')
    bot.send_poll(msg.chat.id, question=question, options=answers, is_anonymous=True, allows_multiple_answers=False)
# endregion

# region BlackJack
#blackjack start--------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['blackjack'])
def blackjack(msg):
    global deck_id, user_scores, deck_chat_id
    bot.send_message(ADMIN_CHAT_ID, msg.from_user.username)
    deck_chat_id = msg.chat.id
    user_scores = dict()
    deck_id = json.loads(requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='Зарегистрироваться в игру', callback_data='registr'),
               types.InlineKeyboardButton(text='Выход', callback_data='quit'))
    bot.send_message(deck_chat_id, 'Для того, чтобы сыграть в BlackJack \U0001F0CF, нажмите "Зарегистрироваться в игру" и '
                                   'следуйте дальнейшим указаниям', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == 'Принять участие в игре')
def in_game(msg):
    user = msg.from_user.username
    user_chat = msg.from_user.id
    user_scores[user] = user_scores.get(user, [0])
    user_scores.get(user).append(user_chat)
    bot.send_message(deck_chat_id, f'{user} в игре!')
    if len(user_scores) > 1:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
                   types.InlineKeyboardButton(text='Начать игру', callback_data='startgame'))
        bot.send_message(msg.chat.id, 'Игра', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ['registr', 'startgame', 'quit'])
def player_registration(callback):
    global user, users
    if callback.data == 'registr':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('Принять участие в игре'))
        bot.send_message(deck_chat_id, 'Нажми на "Принять участие в игре для регистрации"\n\n'
                                       'После того, как все игроки зарегистрируются, нажмите "Начать игру"', reply_markup=markup)
    elif callback.data == 'startgame':
        bot.delete_message(deck_chat_id, callback.message.id)
        users = iter(user_scores.keys())
        user = next(users)
        start_game(callback.message, user)
    else:
        bot.delete_message(deck_chat_id, callback.message.id)


def start_game(msg, user):
    global user_chat
    bot.send_message(deck_chat_id, f'Сейчас ходит - {user}')
    url = f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2'
    cards = json.loads(requests.get(url).text)['cards']
    user_chat = user_scores[user][1]
    for card in cards:
        card_value = get_card_value(card)
        bot.send_photo(user_chat, photo=card['image'], caption=f'Ценность твоей карты - {card_value}')
        user_scores[user][0] += card_value
    if user_scores[user] == 22:
        bot.send_message(deck_chat_id, f'Игрок {user} выиграл игру')
        end_game(msg)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton(text='Ещё одну карту'),
                   types.KeyboardButton(text='Мне хватит'))
        bot.send_message(user_chat, f'Твои очки - {user_scores[user][0]}\n\nВыберите действие', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text in ['Ещё одну карту', 'Мне хватит'])
def continue_play(msg):
    global user
    if msg.text == 'Ещё одну карту':
        url = f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1'
        card = json.loads(requests.get(url).text)['cards'][0]
        user_scores[user][0] += get_card_value(card)
        bot.send_photo(user_chat, photo=card['image'], caption=f'Твои очки - {user_scores[user][0]}')
        if user_scores[user][0] > 21:
            bot.send_message(user_chat, 'Ты перебрал, ход переходит к следующему игроку')
            try_next(msg)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(types.KeyboardButton('Ещё одну карту'),
                       types.KeyboardButton('Мне хватит'))
            bot.send_message(user_chat, 'Что дальше?', reply_markup=markup)
    elif msg.text == 'Мне хватит':
        try_next(msg)

def try_next(msg):
    global user
    bot.send_message(deck_chat_id, f'{user} закончил свой ход')
    try:
        user = next(users)
        return start_game(msg, user)
    except StopIteration as error:
        return end_game(msg)

def end_game(msg):
    global user_scores
    list_scores, list_winners = list(), list()
    for user in user_scores:
        user_score = user_scores[user][0]
        bot.send_message(deck_chat_id, f'{user} набрал - {user_score}')
        if  user_score <= 21:
            list_scores.append(user_score)
    for user in user_scores:
        if user_scores[user][0] <= 21 and user_scores[user][0] == max(list_scores):
            list_winners.append(user)
    if 0 < len(list_winners) < 2:
        bot.send_message(deck_chat_id, f'Итак, наш победитель - {list_winners[0]}')
    elif len(list_winners) == 0:
        bot.send_message(deck_chat_id, f'Кажется все игроки перебрали..\n\nНу что-ж, это ничья')
    else:
        bot.send_message(deck_chat_id, f'Ого! У нас несколько победителей с количеством очков {max(list_scores)}')
        for winner in list_winners:
            bot.send_message(deck_chat_id, f'Один из наших чемпионов - {winner}')
        bot.send_message(deck_chat_id, f'Спасибо за игру! Если хотите сыграть снова, напишите /blackjack')
#blackjack ended--------------------------------------------------------------------------------------------------------
# endregion

# region Admin
@bot.message_handler(commands=['admin'])
def adminka(msg):
    if msg.from_user.id == ADMIN_CHAT_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        markup.add(types.KeyboardButton(text='Загрузить сегодняшний отчет по крипте'),
                   types.KeyboardButton(text='Admin command2'),
                   types.KeyboardButton(text='Admin command3'))
        bot.send_message(msg.chat.id, 'Админ команды', reply_markup=markup)

    else:
        bot.send_message(msg.chat.id, 'У вас нет доступа к админ командам')


@bot.message_handler(func=lambda msg: msg.text == 'Загрузить сегодняшний отчет по крипте')
def crypto_sink(msg):
    message = crypto_des()
    bot.send_message(msg.chat.id, message)
# endregion

# region Non ended content
"""
Non ended content
"""
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

    #else:
        #with open(r'C:\Users\fokin.ni\PycharmProjects\work-telegram\tmp\aaa.jpg', 'rb') as file:
            #bot.send_photo(msg.chat.id, file)
# endregion

# region w8 user callback
def send_idea(msg):
    bot.send_message(ADMIN_CHAT_ID, f'Сообщение от {msg.from_user.first_name} {msg.from_user.last_name}\n\n'
                                    f'Идея:\n{msg.text}')
    bot.send_message(msg.chat.id, 'Спасибо большое за фидбек, сообщение передано! \U0001F44D')

def my_decision(msg):
    decision = json.loads(requests.get('https://yesno.wtf/api').text)
    bot.send_video(msg.chat.id, decision['image'])

def get_card_value(card):
    return card_values[card['value']] if card['value'] in card_values.keys() else int(card['value'])
# endregion

#-----------------------------------------------------
@bot.edited_message_handler(func=lambda msg: True)
def reply_to_edited(msg):
    bot.reply_to(msg, 'I see everything, you edited your message, LIAR!\U0001F440')

def report_for_date(msg):
    dates = str(msg.text)
    my_list = report_for_date_mysql(dates)
    for dish in my_list:
        bot.send_message(msg.chat.id, f'{dish}')





if __name__ == '__main__':
    bot.infinity_polling()
