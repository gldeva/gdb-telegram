import sqlite3
import openai
import requests
import telegram
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackContext

# Set up OpenAI API
openai.api_key = "YOUR_OPENAI_API"

# Set up Telegram bot
bot = telegram.Bot(token="YOUR_TELEGRAM_BOT_API")
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher

#When /start send Hello! How can I help you?
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! How can I help you?")

#Generate text or code
def generate_text(update, context):
    # Get user input
    prompt = update.message.text

    # Generate text with OpenAI's GPT-3 model
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Send generated text back to user
    text = completions.choices[0].text
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

#Generate image
def generate_image(update, context):
    # Get user input
    prompt = update.message.text

    # Generate image with OpenAI's DALL-E model
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }
    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 4,
        "size": "1024x1024",
        "response_format": "url",
    }
    response = requests.post(url, headers=headers, json=data)

    # Send generated image back to user
    image_url = response.json()["data"][0]["url"]
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)

# Set up message handlers
start_handler = CommandHandler('start', start)
dalle_handler = CommandHandler("dalle", generate_image)
text_handler = CommandHandler("chat", generate_text)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(dalle_handler)
dispatcher.add_handler(text_handler)

# Start the bot
updater.start_polling()
