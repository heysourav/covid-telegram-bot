#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://git.io/JOmFw.
"""
import logging
import requests
import json
import datetime
import urllib
from json import loads

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("18+", callback_data='1'),
            InlineKeyboardButton("45+", callback_data='2'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please Select Your Age Group :', reply_markup=reply_markup)


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data == '1':
        text = get_update(18)
        query.message.reply_text(text)
    elif query.data == '2':
        text = get_update(45)
        query.message.reply_text(text)
    else :
        query.message.reply_text(text=f"Selected option: {query.data}")


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")

def get_update(age) :
    date = str(f"{datetime.datetime.now():%d-%m-%Y}")
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=446&date={date}".format(date = date)
    response = requests.get(url)
    data = response.json()
    results = []
    print("*********************")
    for i in range(len(data['centers'])):
        for j in range(len(data['centers'][i]['sessions'])):
            if data['centers'][i]['sessions'][j]['min_age_limit'] == age :
                if  data['centers'][i]['sessions'][j]['available_capacity'] != 0 :
                    num_vcc = json.dumps(data['centers'][i]['sessions'][j]['available_capacity'])
                    center_name = json.dumps(data['centers'][i]['name'])
                    time_slot = json.dumps(data["centers"][i]["sessions"][j]["date"])
                    msg = "Number of Vaccines : "+num_vcc +"\n"+"Vaccines avaialble at : " + center_name +"\n"+ "For Time Slot : "+time_slot
                    results.append(msg)
    if len(results) == 0:
        return(["No Vaccines Available"])
    else :
        return(results)


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1793249807:AAHwe6HjQAFhBfcIbAqdgYUxtWdHsJYPX2U")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
