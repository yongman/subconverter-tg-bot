#!/usr/bin/env python
# pylint: disable=unused-argument, import-error
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import subprocess

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_msg = """
    echo: echo you input
    help: print this message
    add: add a new DOMAIN-SUFFIX rules to {Name}.list and call clash http api to reload. eg. /add google.com Google
    del: del the rule matched the input. eg. /del youtube.com YouTube
    """
    await update.message.reply_text(help_msg)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

FILE_NAME = os.environ.get('FILE_NAME')
POST_CMD = os.environ.get('POST_CMD')

async def add_rule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a DOMAIN-SUFFIX rule to {Proxy}.list"""
    # Default to Proxy.list if not specified in command
    file_name = FILE_NAME
    rule_and_file = update.message.text.lstrip('/add').strip().split()
    if len(rule_and_file) == 2:
        file_name = '{}.list'.format(rule_and_file[1])

    # check file if exists
    if not os.path.exists(file_name):
        resp = 'Rule file {} not exists'.format(file_name)
        await update.message.reply_text(resp)
        return

    rule = rule_and_file[0].strip()
    with open(file_name, 'a') as f:
        f.write('DOMAIN-SUFFIX,{}\n'.format(rule))
    resp = 'Add {} to {} done!'.format(rule, file_name)
    if POST_CMD is not None:
        result = subprocess.run(POST_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            resp = '{}\nPost command done!'.format(resp)
        else:
            resp = '{}\nPost command failed! {}'.format(resp, result.stderr)
    await update.message.reply_text(resp)

async def del_rule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Delete a rule matched the input domain"""
    # Default to Proxy.list if not specified in command
    file_name = FILE_NAME
    rule_and_file = update.message.text.lstrip('/del').strip().split()
    if len(rule_and_file) == 2:
        file_name = '{}.list'.format(rule_and_file[1])

    # check file if exists
    if not os.path.exists(file_name):
        resp = 'Rule file {} not exists'.format(file_name)
        await update.message.reply_text(resp)
        return

    rule = rule_and_file[0].strip()
    lines=[]
    with open(file_name, 'r') as f:
        lines = f.readlines()
    with open(file_name + '.tmp', 'w') as f:
        for line in lines:
            parts = line.split(',')
            if len(parts) != 2:
                continue
            if parts[1].strip() == rule:
                continue
            print(parts[1].strip())
            print(rule)
            print(line)
            f.write(line)
    os.rename(file_name + '.tmp', file_name)
    resp = 'Delete {} from {} done!'.format(rule, file_name)
    if POST_CMD is not None:
        result = subprocess.run(POST_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            resp = '{}\nPost command done!'.format(resp)
        else:
            resp = '{}\nPost command failed! {}'.format(resp, result.stderr)
    await update.message.reply_text(resp)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    token = os.environ.get('TOKEN')
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add_rule))
    application.add_handler(CommandHandler("del", del_rule))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
