from telegram import InlineQueryResultArticle , ParseMode , InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown
from urllib.request import urlopen
from bs4 import BeautifulSoup
from uuid import uuid4
import urllib.request
import requests
import telegram
bot = telegram.Bot(token="TOKEN")

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
	update.message.reply_text("Hi, for getting a word's definition in Urban dictionary just send me the word or use the inline group mode by adding it to the group, for more info press /help")


def help(update, context):
	update.message.reply_text("Urban Dictionary is a crowdsourced online dictionary for slang words and phrases, operating under the motto 'Define Your World'. For searching a word's definition in Urban dictionary simply send the word or use it in your groups by typing '@ID + the word you're looking for' when it's added to the group. Hope you enjoy it.")

#A scrapping code for getting the "result" meta code on UrbanDictionaty.com and copying it				
def get_definition(word):
	word.replace(" ", "+")
	link = "http://www.urbandictionary.com" + "/define.php?term=" + word
	response = requests.get(link)
	soup = BeautifulSoup(response.text, "html.parser")
	if "og:description" in str(soup):
		for tag in soup.find_all("meta"):
			if tag.get("property", None) == "og: description":
				return (tag.get("content", None))
			if tag.get("property", None) == "og:description":
				return (tag.get("content", None))
	elif "Sorry, we couldn't find" in str(soup):
		return ("Sorry, we couldn't find: " + word)

#Reply the messages in private conversation
def definition(update, context):
	word = update.message.text
	definition = get_definition(word)
	update.message.reply_text(definition)
	
#Getting the definition of a word in groups in inline mode, while the bot is added to the group	
def inlinequery(update, context):
	query = update.inline_query.query
	get_definition(query)
	results =[ 
		InlineQueryResultArticle(
			id=uuid4(),
			title="Definition",
			input_message_content=InputTextMessageContent(
				query.lower())),
			]
	
	update.inline_query.answer(results)


def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

	updater = Updater("TOKEN", use_context=True)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(MessageHandler(Filters.text, definition))
	dp.add_handler(InlineQueryHandler(inlinequery))

	dp.add_error_handler(error)
	
	updater.start_polling()

	updater.idle()

if __name__ == '__main__':
	main()
