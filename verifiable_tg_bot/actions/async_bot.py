import asyncio
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

bot = AsyncTeleBot(os.environ["BOT_TOKEN"])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Hi there, I am EchoBot.!\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    print ("entered echo async")
    await bot.reply_to(message, message.text)

async def run():
    await bot.polling(non_stop=False,interval=3, timeout=3, request_timeout=3)

# start the asyncio program
#asyncio.run(run())

#asyncio.run(bot.polling())
# loop = asyncio.get_event_loop()
#task = loop.create_task(bot.polling())
#await asyncio.sleep(3)
#task.cancel()
# loop.run_forever()