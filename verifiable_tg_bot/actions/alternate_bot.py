import asyncio
import os

import telebot
from dotenv import load_dotenv

load_dotenv()
# Create the Application and pass it your bot's token.
bot = telebot.TeleBot(os.environ["BOT_TOKEN"])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print(f"entered echo message {message}")
    bot.reply_to(message, message.text)


#print(bot.get_me())
print ('start')
#bot.process_new_updates()
#bot.infinity_polling(long_polling_timeout=2)
bot.polling(timeout=2, long_polling_timeout=2,
                             restart_on_change=False,
                             )
#updates = bot.get_updates(timeout=2)
#updates = bot.get_updates(timeout=2)
print ('before updates')
#bot.process_new_updates(updates)
#print (f'updates {updates}')
#bot.polling()
print ('finish')