import time

from dotenv import load_dotenv
from giza_actions.action import action, Action
from giza_actions.task import task
import asyncio
import io
import logging
import os
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, \
    Updater
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from verifiable_tg_bot.bot_helpers import start, help_command, echo

load_dotenv()


async def sleep_return(s):
    time.sleep(s)
    return 420

async def process_updates():
    pass


def async_to_sync(awaitable):
    #loop = asyncio.get_event_loop()
    loop = None
    if not loop:
        print ('no loop')
        loop = asyncio.new_event_loop()
    return loop.run_until_complete(awaitable)

@task(name="answer user")
def reply_to_messages():
    print(f"Starting echo")
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ["BOT_TOKEN"]).get_updates_pool_timeout(3).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    #application.add_handler(CommandHandler("eth_prediction", get_ETH_price_prediction_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    async_to_sync(application.run_polling(allowed_updates=Update.ALL_TYPES))



@action(name="Action: dummy action", log_prints=True)
def execution():
    print("Starting action")
    #reply_to_messages()
    #result = async_to_sync(sleep_return(.69))
    #print (f'result {result}')
    reply_to_messages()
    print("Finishing action")


if __name__ == "__main__":
    # action_deploy = Action(entrypoint=execution, name="pytorch-mnist-action")
    #action_deploy = Action(entrypoint=execution, name="telegram-bot-dummy")
    #action_deploy.serve(name="telegram-bot-dummy")
    execution()