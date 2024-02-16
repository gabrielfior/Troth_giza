import os

import telebot.types
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

from verifiable_tg_bot.actions.price_forecaster import PriceForecaster, build_fig_for_forecast

load_dotenv()

bot = AsyncTeleBot(os.environ["BOT_TOKEN"])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, "Hello from Giza's ETH prediction bot")


@bot.message_handler(commands=['eth_prediction'])
async def get_eth_price_prediction_command(message: telebot.types.Message):
    photo = build_fig_for_forecast()
    await bot.send_photo(message.chat.id, photo=photo, caption="ETH prices for next 5 days")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    print("entered echo async")
    await bot.reply_to(message, message.text)


async def run():
    await bot.polling(non_stop=False, interval=30, timeout=30, request_timeout=30)