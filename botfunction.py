from mysql.connector import connect, Error
from config import mysql_host, mysql_user, mysql_password


def insert_proc(msg):
    try:
        with connect(host=mysql_host,
                     user=mysql_user,
                     password=mysql_password) as connection:

            values = msg.text.split(';')
            db_insert = """
            call foodv2.main_obed_proc(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(db_insert, values)
                connection.commit()
                return cursor.fetchone()

    except Error as r:
        print(r)


def report_for_date_mysql(dates):
    try:
        with connect(host=mysql_host,
                     user=mysql_user,
                     password=mysql_password) as connection:
            date_from, date_to = map(int, dates.split())
            db_select = """
                    call foodv2.show_menu({}, {})""".format(date_from, date_to)
            with connection.cursor() as cursor:
                cursor.execute(db_select)
                my_list = cursor.fetchall()
                return my_list
    except Error as r:
        print(r)


