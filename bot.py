import telebot
from telebot import types, util
from config import TOKEN, ADMIN_CHAT_ID
from botfunction import insert_proc, report_for_date
from random import shuffle, randint, choice
import requests
import json
from lists import list_of_films, list_of_anime, list_gifts, dic_commands, card_values

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_sticker(msg.chat.id, 'CAACAgIAAx0CYG_RBAACASdiWUmPC8cIGuIVLlr6e6GtYqtziAACmQwAAj9UAUrPkwx5a8EilCME')
    bot.send_message(msg.chat.id, f'Привет {msg.from_user.first_name} {msg.from_user.last_name}, тебя приветствует бот - lizadegu \U0001F43F\n\n'
                                  f'На данный момент я нахожусь на этапе разработки, если у вас есть пожелания или идеи,'
                                  f'отправьте тэг /ideas и напишите мне сообщение, я обязательно передам его своему хозяину\n\n'
                                  f'С уже имеющимися функциями вы можете познакомиться нажав /commands')

@bot.message_handler(commands=['ideas'])
def send_idea_for_admin(msg):
    bot.send_message(msg.chat.id, 'Отлично, теперь напиши сообщение с идеей или пожеланием и я сразу передам его в нужное место, жду \U0001F642')
    bot.register_next_step_handler(msg, callback=send_idea)


@bot.message_handler(commands=['commands'])
def send_commands(msg):
    for command, description in dic_commands.items():
        bot.send_message(msg.chat.id, f'{command} - {description}')

@bot.message_handler(commands=['watch'])
def choose_watch(msg):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='Полнометражные фильмы', callback_data='film'),
               types.InlineKeyboardButton(text='Сериалы', callback_data='serial'),
               types.InlineKeyboardButton(text='Аниме', callback_data='anime'),
               types.InlineKeyboardButton(text='Выход', callback_data='exit'))
    bot.send_message(msg.chat.id, 'Выберите категорию', reply_markup=markup)


@bot.callback_query_handler(func=lambda msg: msg.data in
                                             ['film', 'anime', 'serial', 'filter', 'random list_of_films',
                                              'random list_of_anime', 'exit'])
def choose_watch(callback):
    if callback.data in ['random list_of_films', 'random list_of_anime']:
        chooses_dic = {
            'random list_of_films': list_of_films,
            'random list_of_anime': list_of_anime
        }
        where = chooses_dic[callback.data]
        number = randint(1, 200)
        film = where.get(number)
        bot.send_photo(callback.message.chat.id, photo=film["pic"]
                                                   , caption=f'Название фильма - {film["name"]}\n\n'
                                                   f'Год выпуска фильма - {film["year"]}\n\n'
                                                   f'Рейтинг фильма - {film["mean_rate"]}')
    elif callback.data == 'exit':
        bot.delete_message(callback.message.chat.id, callback.message.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        choose_dic = {
            'film': ['случайный фильм', 'фильмы', 'list_of_films'],
            'anime': ['случайное аниме', 'аниме', 'list_of_anime'],
            'serial': ['случайный сериал', 'сериалы', 'list_of_serial']
        }
        choose_one, choose_two, choose_where = choose_dic[callback.data][0], choose_dic[callback.data][1], \
                                               choose_dic[callback.data][2]
        markup.add(types.InlineKeyboardButton(text=f'Выбрать {choose_one}', callback_data=f'random {choose_where}'),
                   types.InlineKeyboardButton(text=f'Отфильтровать {choose_two} по дате', callback_data='filter'),
                   types.InlineKeyboardButton(text='Выход', callback_data='exit'))
        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выбирайте далее', reply_markup=markup,
                              message_id=callback.message.id)



@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, 'Hello, for get fact of random date, send me /getInfoRandomDate')

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




"""
Play
"""
@bot.message_handler(commands=['play'])
def play(msg):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    dice = types.KeyboardButton(text='Dice 🎲')
    darts = types.KeyboardButton(text='Darts 🎯')
    slots = types.KeyboardButton(text='Slots 🎰')
    basket = types.KeyboardButton(text='Basket 🏀')
    football = types.KeyboardButton(text='Football ⚽')
    bouling = types.KeyboardButton(text='Bouling 🎳')
    markup.add(darts, dice, slots, basket, football, bouling)
    bot.send_message(msg.chat.id, 'Choose a game', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text in ['Dice 🎲', 'Darts 🎯', 'Slots 🎰', 'Basket 🏀', 'Football ⚽', 'Bouling 🎳'])
def start_play(msg):
    play_dic = {
        'Dice 🎲': '🎲',
        'Darts 🎯': '🎯',
        'Slots 🎰': '🎰',
        'Basket 🏀': '🏀',
        'Football ⚽': '⚽',
        'Bouling 🎳': '🎳'
    }
    bot.send_dice(msg.chat.id, play_dic[msg.text])


"""
Contact us
"""
@bot.message_handler(commands=['contact'])
def contact_us(msg):
    bot.send_message(msg.chat.id, 'Contact with us')
    bot.send_location(msg.chat.id, 59.913749, 30.350741)
    bot.send_contact(msg.chat.id, first_name='Nikita', last_name='Fokin', phone_number='89313062923')


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


"""Get user picture"""
@bot.message_handler(commands=['getUserPic'])
def send_user_pic(msg):
    photo = bot.get_user_profile_photos(msg.from_user.id)
    if photo.photos:
        bot.send_message(msg.chat.id, photo.photos[0][0].file_id)
    else:
        bot.send_message(msg.chat.id, 'User has no photo')

#blackjack start--------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['blackjack'])
def blackjack(msg):
    global deck_id, user_scores, deck_chat_id
    deck_chat_id = msg.chat.id
    user_scores = dict()
    deck_id = json.loads(requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='Зарегистрироваться в игру', callback_data='registr'),
               types.InlineKeyboardButton(text='Начать игру', callback_data='startgame'))
    bot.send_message(deck_chat_id, 'Для того, чтобы сыграть в BlackJack \U0001F0CF, нажмите "Зарегистрироваться в игру" и '
                                   'следуйте дальнейшим указаниям', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == 'Принять участие в игре')
def in_game(msg):
    user = msg.from_user.username
    user_chat = msg.from_user.id
    user_scores[user] = user_scores.get(user, [0])
    user_scores.get(user).append(user_chat)
    bot.send_message(deck_chat_id, f'{user} в игре!, {user_scores}')


@bot.callback_query_handler(func=lambda callback: callback.data in ['registr', 'startgame'])
def player_registration(callback):
    global user, users
    if callback.data == 'registr':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('Принять участие в игре'))
        bot.send_message(deck_chat_id, 'Нажми на "Принять участие в игре для регистрации"\n\n'
                                       'После того, как все игроки зарегистрируются, нажмите "Начать игру"', reply_markup=markup)
    else:
        bot.delete_message(deck_chat_id, callback.message.id)
        users = iter(user_scores.keys())
        user = next(users)
        start_game(callback.message, user)


def start_game(msg, user):
    global user_chat
    bot.send_message(msg.chat.id, f'Сейчас ходит - {user}')
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
            bot.send_message(deck_chat_id, f'{user} закончил свой ход')
            try:
                user = next(users)
                start_game(msg, user)
            except StopIteration as error:
                end_game(msg)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(types.KeyboardButton('Ещё одну карту'),
                       types.KeyboardButton('Мне хватит'))
            bot.send_message(user_chat, 'Что дальше?', reply_markup=markup)
    elif msg.text == 'Мне хватит':
        bot.send_message(deck_chat_id, f'{user} закончил свой ход')
        try:
            user = next(users)
            start_game(msg, user)
        except StopIteration as error:
            end_game(msg)


def end_game(msg):
    global user_scores
    flag = True
    for user in user_scores:
        bot.send_message(deck_chat_id, f'{user} набрал - {user_scores[user][0]}')

    for user in sorted(user_scores.items(), key=lambda x: x[1], reverse=True):
        if user_scores[user[0]][0] <= 21:
            bot.send_message(deck_chat_id, f'Итак, наш победитель - {user[0]}')
            flag = False
            break
    if flag:
        bot.send_message(deck_chat_id, f'Кажется оба игрока перебрали..\n\nНу что-ж, это ничья')
#blackjack ended--------------------------------------------------------------------------------------------------------


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
#Функции ожидания ответа юзера------------------------------------------------------------------------------------------
def send_idea(msg):
    bot.send_message(ADMIN_CHAT_ID, f'Сообщение от {msg.from_user.first_name} {msg.from_user.last_name}\n\n'
                                    f'{msg.text}')
    bot.send_message(msg.chat.id, 'Спасибо большое за фидбек, сообщение передано! \U0001F44D')

def my_decision(msg):
    decision = json.loads(requests.get('https://yesno.wtf/api').text)
    bot.send_video(msg.chat.id, decision['image'])

def get_card_value(card):
    return card_values[card['value']] if card['value'] in card_values.keys() else int(card['value'])




#-----------------------------------------------------
@bot.message_handler(content_types=['sticker'])
def identity_sticker(msg):
    list_gifts.append(msg.sticker.file_id)
    bot.send_sticker(msg.chat.id, choice(list_gifts))
    #bot.send_message(msg.chat.id, list_gifts)


@bot.edited_message_handler(func=lambda msg: True)
def reply_to_edited(msg):
    bot.reply_to(msg, 'I see everything, you edited your message, LIAR!\U0001F440')


if __name__ == '__main__':
    bot.infinity_polling()
