
import os
import random
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
bot = telebot.TeleBot(TOKEN)

def search_no_api(limit=5):
    results = []
    try:
        r = requests.get("https://api.imgflip.com/get_memes", timeout=15).json()
        memes = r["data"]["memes"]
        for m in random.sample(memes, limit):
            results.append({"title": m["name"], "url": m["url"], "source": "Imgflip"})
    except Exception as e:
        print("Imgflip fail:", e)
    try:
        r = requests.get("https://meme-api.com/gimme/5", timeout=15).json()
        for m in r.get("memes", []):
            results.append({"title": m["title"][:40], "url": m["url"], "source": "Meme-API"})
    except Exception as e:
        print("Meme-API fail:", e)
    random.shuffle(results)
    return results[:limit]

@bot.message_handler(commands=["start", "help"])
def start(m):
    bot.reply_to(m, "JAGRUK BOT ON HAI! Commands: /search - Naye memes, /status - Status")

@bot.message_handler(commands=["search"])
def handle_search(m):
    bot.reply_to(m, "Search kar raha hu...")
    results = search_no_api(5)
    if not results:
        bot.reply_to(m, "Search fail, dobara try karo")
        return
    for meme in results:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Reel Banao", callback_data="make"))
        try:
            bot.send_photo(m.chat.id, meme["url"], caption=meme["title"] + " - " + meme["source"], reply_markup=markup)
        except Exception as e:
            bot.reply_to(m, "Photo fail: " + meme["url"])

@bot.message_handler(commands=["status"])
def status(m):
    bot.reply_to(m, "Bot zinda hai! Har 7 ghante me auto-search chal raha hai.")

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    bot.answer_callback_query(c.id, "Selected! Reel ban rahi hai.")

if __name__ == "__main__":
    print("Telegram Bot ON")
    bot.infinity_polling()
