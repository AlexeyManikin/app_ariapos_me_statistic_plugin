__author__ = 'Alexey Y Manikin'

import telebot
import config.config
import re
import classes.llm_parser

botTelegram = telebot.TeleBot(config.config.TELEGRAM_BOT_KEY)

@botTelegram.message_handler(commands=['start'])
def start_bot(message: telebot.types.Message):
    botTelegram.reply_to(message, config.config.TELEGRAM_BOT_HELP)

@botTelegram.message_handler(commands=['print_group'])
def print_group(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    result = ""
    for item in model.get_list_of_category():
        result += " - " + str(model.get_list_of_category()[item]) + "\n"
    botTelegram.reply_to(message, result)

@botTelegram.message_handler(commands=['summary'])
def summary(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    result = "Суммарные траты за последние 30 дней - %i" % model.get_summary_row(30)
    botTelegram.reply_to(message, result)

@botTelegram.message_handler(commands=['last'])
def last(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    result =  model.get_list_spending(30)
    str_result = ""
    for item in result:
        str_result += " - " + str(item['date'])[0:10] + " - " + str(model.get_list_of_category()[item['group_type']]) + " - " + str(item['description']) + " - " + str(item['summ']) + "\n"

    botTelegram.reply_to(message, str_result)

@botTelegram.message_handler(content_types=['text'])
def parce_message(message: telebot.types.Message):
    if not re.findall(r'\d+', message.text):
        return

    model = classes.llm_parser.LLMParser()
    result = model.parse_date(message.text, message.date, message.from_user.full_name)

    if result != {}:
        d = model.get_list_of_category()
        return_text = "Данные добавлены: \n" + \
               "  - сумма: %s\n" % result['summ'] + \
               "  - группа: %s\n" % d[result['group']] + \
               "  - описание: %s\n" % result['description'] + \
               "  - дата: %s" % result['date']
        botTelegram.reply_to(message, return_text)

def run():
    botTelegram.infinity_polling()