#!/usr/bin/python

import telebot
from DailyFilm import DailyFilm
from Database import Database
from env import *


def main():
    bot = telebot.TeleBot(TG_BOT_KEY)
    Database.db_setup()
    df = DailyFilm()
    m = df.get_daily_film()

    bot.send_message(TG_CHAT_ID, m, parse_mode="markdown")


if __name__ == '__main__':
    main()
