from sqlalchemy import create_engine, MetaData, Table, select, Column, Integer, DECIMAL, Text, String, ForeignKey, \
    update, BIGINT, Date, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, Session, sessionmaker, registry, relationship
from sqlalchemy.sql import func
from random import randint
from coin_market import get_data_from_cmc
from datetime import date
from config import mysql_connect


engine = create_engine(mysql_connect)
metadata = MetaData()
session = Session(bind=engine)
Base = declarative_base()
mapper_registry = registry()
anime_main = Table('animedeclarativeversion', metadata, autoload=True, autoload_with=engine)


class Anime(object):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_from_telegram = Column(Integer)
    full_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    balance = Column(Integer)


class Operation(Base):
    __tablename__ = 'operations_telegram'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer)
    move = Column(Integer)
    transaction_id = Column(String(255))
    game_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    bet_id = Column(Integer, ForeignKey('bet_types.id', ondelete='CASCADE'))
    value = Column(Integer)
    dt = Column(TIMESTAMP)

    user = relationship('User', backref='operations_telegram')
    bet = relationship('BetType', backref='bet_types')


class CryptoCurrency(Base):
    __tablename__ = 'crypto_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_from_cmc = Column(Integer)
    crypto_name = Column(String(255))
    symbol = Column(String(255))
    cmc_rank = Column(Integer)
    price = Column(DECIMAL(15, 2))
    volume = Column(BIGINT)
    date_update = Column(Date, default=func.current_date())


class BetType(Base):
    __tablename__ = 'bet_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bet_name = Column(String(255))



mapper_registry.map_imperatively(Anime, anime_main)
































def random_select_anime():
    number = randint(1, 200)
    for my_tuple in session.query(Anime.name, Anime.year, Anime.rating, Anime.pic, Anime.description).filter(Anime.id == number):
        return my_tuple

def select_all_anime_titles():
    stmt = select(Anime.name)
    result = session.execute(stmt).fetchall()
    return result

def concrect_select(num):
    for my_tuple in session.query(Anime.name, Anime.year, Anime.rating, Anime.pic, Anime.description).filter(Anime.id == num):
        return my_tuple

def insert_into_table(entity):
    for key in entity:
        name, year, mean_rate, pic, desc = entity[key].values()
        new_object = Anime(name=name, year=year, rating=mean_rate, pic=pic, description=desc)
        session.add(new_object)
    session.commit()
    return 'Success'

def get_user_balance(telegram_id):
    stmt = select(User.balance).filter(User.id_from_telegram == telegram_id)
    user = session.execute(stmt).fetchone()[0]
    return user

def reg_user(telegram_id, full_name, username):
    user = User(id_from_telegram=telegram_id, full_name=full_name, username=username, balance='2500')
    session.add(user)
    session.commit()
    stmt = select(User.balance).filter(User.id_from_telegram == telegram_id)
    user_bal = session.execute(stmt).fetchone()
    return user_bal

def balance_update(telegram_id, new_balance):
    session.query(User).filter(User.id_from_telegram == telegram_id).update({'balance': new_balance})
    session.commit()
    user_balance = session.execute(select(User.balance).filter(User.id_from_telegram == telegram_id)).fetchone()[0]
    return user_balance

def films_filter(year, action):
    action_dict = {
        'inThisYear': select(Anime.name).filter(Anime.year == year),
        'afterThisYear': select(Anime.name).filter(Anime.year >= year),
        'beforeThisYear': select(Anime.name).filter(Anime.year <= year)
    }
    stmt = action_dict[action]
    my_list = session.execute(stmt).fetchall()
    return my_list

def crypto_des():
    current_update = session.execute(select(func.max(CryptoCurrency.date_update))).fetchone()[0]
    current_date = date.today()
    if not current_update or current_date > current_update:
        data = get_data_from_cmc()
        return crypto_price_everyday(data)
    else:
        return 'Цена за текущий день уже добавлена в БД'

def crypto_price_everyday(data):
    for monet in data['data']:
        new_monet = CryptoCurrency(id_from_cmc=monet['id'], crypto_name=monet['name'], symbol=monet['symbol'],
                                    cmc_rank=monet['cmc_rank'], price=monet['quote']['USD']['price'],
                                   volume=monet['quote']['USD']['volume_24h'] / 10 ** 6)
        session.add(new_monet)
    session.commit()
    return 'Success'

def dice_payInOut(amount, move, transaction_id, game_id, telegram_user_id, bet_id, value=None):
    user_id = session.execute(select(User.id).filter(User.id_from_telegram==telegram_user_id)).fetchone()[0]
    operation = Operation(amount=amount, move=move, transaction_id=transaction_id, game_id=game_id,
                     user_id=user_id, bet_id=bet_id, value=value)
    session.add(operation)
    session.commit()
    return 'Success'


