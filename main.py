#!/usr/bin/python3


###
### https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
###
import telebot
from datetime import datetime
from secrets_1 import bot_token, img_link, chat_id
import requests
import shutil
from dataclasses import dataclass

if bot_token == "" or img_link == "" or chat_id == "":
    print("please provide all secrets")
    exit()

bot = telebot.TeleBot(bot_token, parse_mode=None)


@dataclass
class photo_class:
    timestamp: datetime
    photo_path: str = "photo.jpg"


img_file = "photo.jpg"


def get_photo():
    res = requests.get(img_link, stream=True)
    if res.status_code == 200:
        photo = photo_class(datetime.now())
        with open(photo.photo_path, "wb") as f:
            shutil.copyfileobj(res.raw, f)
    return photo


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "{} > This is only for debbuging".format(datetime.now()))


@bot.message_handler(commands=["photo"])
def send_photo(message):
    photo = get_photo()
    try:
        with open(photo.photo_path, "rb") as f:
            bot.send_photo(
                chat_id,
                f,
                "Sended @{}\nPhoto time taken @{}\n".format(
                    datetime.now(), photo.timestamp
                ),
            )
    except OSError as e:
        bot.reply_to(message, "No photo found")


bot.infinity_polling()
