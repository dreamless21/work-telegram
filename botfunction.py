from mysql.connector import connect, Error
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


def insert_proc(msg):
    try:
        with connect(host='192.168.159.62',
                     user='python',
                     password='pythonmysql') as connection:

            values = msg.text.split(';')
            db_insert = """
            call foodv2.main_obed_proc(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(db_insert, values)
                connection.commit()
                bot.send_message(msg.chat.id, cursor.fetchone())

    except Error as r:
        print(r)


def report_for_date(msg):
    try:
        with connect(host='192.168.159.62',
                     user='python',
                     password='pythonmysql') as connection:
            date_from, date_to = map(int, msg.text.split())
            db_select = """
                    call foodv2.show_menu({}, {})""".format(date_from, date_to)
            with connection.cursor() as cursor:
                cursor.execute(db_select)
                for row in cursor.fetchall():
                    bot.send_message(msg.chat.id, '\n'.join(map(str, row)))

    except Error as r:
        print(r)

