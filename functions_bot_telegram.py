from telegram import ParseMode
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import logging

import functions_config
from classes import Home, Search, MoneyStuff, MoneyStuffCase

updater = Updater(functions_config.get_telegram_confing().bot.api_token, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("ciao Denise")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Your Message")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


def send_text(msg, chat_telegram_id):
    updater.bot.send_message(chat_id=chat_telegram_id, text=msg)


def send_as_html(chat_telegram_id, text, disable_notification):
    updater.bot.send_message(chat_id=chat_telegram_id, parse_mode=ParseMode.HTML, text=text,
                             disable_notification=disable_notification)


# no callback functions:

def send_home(chat_telegram_id, disable_notification, home: Home, search: Search):
    hashtags = ""
    try:
        for hashtag in search.keywords:
            hashtags = hashtags + " " + "#" + hashtag
    except AttributeError:
        # todo fixme find the way to avoid : AttributeError: 'types.SimpleNamespace' object has no attribute 'keywords'
        pass
    send_as_html(chat_telegram_id, disable_notification=disable_notification,
                 text=("<b>da: </b> {origin_site} | <b>ricerca:</b> {search_title} \n \n" +
                       "<b>{title}</b> \n" +
                       "<b>Descrizione: breve </b> {description_short} \n" +
                       "<b>prezzo:</b> {price} \n" +
                       "<b>mt2:</b> {mt2} | <b>zona:</b> {zone} \n" +
                       "<b>piano:</b> {floor} | <b>locali:</b> {n_rooms} \n" +
                       "<b>bagni:</b> {n_bath_rooms} | <b>data annuncio:</b> {date} \n" +
                       "\n" +
                       " {description}" +
                       "\n" +
                       "dati monetari:" +
                       "\n" +
                       "<b>contanti posseduti:</b> {cash_held} \n" +
                       get_money_stuff_as_html(home.money_stuff.cases) +
                       "\n" +
                       "<a href='{link_detail}'> vai a vederlo!</a>" +
                       "\n" +
                       "- \n" +
                       hashtags +
                       "\n" +
                       "- \n" +
                       "- \n")
                 .format(origin_site=home.origin_site,
                         search_title=search.title,
                         title=home.title,
                         description_short=home.description_short,
                         price=home.price,
                         mt2=home.mt2,
                         zone=home.zone,
                         floor=home.floor,
                         n_rooms=home.n_rooms,
                         n_bath_rooms=home.n_bath_rooms,
                         date=home.date,
                         description=home.description,
                         cash_held=home.money_stuff.cash_held,
                         link_detail=home.link_detail))


def get_money_stuff_as_html(money_stuff_cases: [MoneyStuffCase()], mortgage_cash_needed=None) -> str:
    to_return: str = ""
    for money_stuff_case in money_stuff_cases:
        to_return = to_return + to_return.format("<b>Descrizione:  </b> {money_stuff_case_description} \n" +
                                                 "commissione agenzia 4%: </b> {mortgage_cash_needed} \n"
                                                 "percentuale mutuo: </b> {mortgage_percentage} \n" +
                                                 "soldi da richiedere:</b> {mortgage_money_to_be_requested} \n" +
                                                 "contanti necessari per mutuo: </b> {mortgage_cash_needed} \n" +
                                                 "costi fissi forfettari: </b> {fixed_costs} \n" +
                                                 "contanti necessari in totale: </b> {total_cash_needed} \n"
                                                 "contanti che rimangono: </b> {total_cash_left} \n"
                                                 ).format(
            description=money_stuff_case.description,
            description= mortgage_cash_needed #tbd!!


        )
    return to_return


# updater.dispatcher.add_handler(CommandHandler('start', start))


# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
# Filters out unknown commands
# updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
# Filters out unknown messages.
# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


def start_bot():
    updater.start_polling()
