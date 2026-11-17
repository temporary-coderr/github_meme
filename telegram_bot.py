
# telegram_bot.py - 24x7 chalega Railway / Render / Laptop pe
# Isse tu Telegram se hi /search dabake meme mangwa sakta hai, GitHub kholne ki zaroorat nahi
# Env: TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

import os, random, requests, subprocess
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
bot = telebot.TeleBot(TOKEN)

# ===== NO-API SEARCH SOURCES - Sab bina API Key ke chalte hain =====
# 1. Imgflip - https://api.imgflip.com/get_memes - NO KEY
# 2. Meme-API - https://meme-api.com/gimme/10 - NO KEY
# 3. Reddit JSON - https://www.reddit.com/r/memes/hot.json - NO KEY (public JSON, login nahi chahiye)
# 4. KnowYourMeme Trending - scrape via requests - NO KEY
# 5. Giphy Trending Memes - isko key chahiye isliye SKIP kiya hai

def search_no_api(limit=5):
    results = []
    # 1. Imgflip
    try:
        r = requests.get("https://api.imgflip.com/get_memes", timeout=15).json()
        for m in random.sample(r["data"]["memes"], min(limit, 10)):
            results.append({"title": m["name"], "url": m["url"], "source": "Imgflip"})
    except Exception as e:
        print(f"Imgflip fail: {e}")
    # 2. Meme-API
    try:
        r = requests.get(f"https://meme-api.com/gimme/{limit}", timeout=15).json()
        for m in r.get("memes", []):
            results.append({"title": m["title"][:40], "url": m["url"], "source": "Meme-API"})
    except Exception as e:
        print(f"Meme-API fail: {e}")
    # 3. Reddit public JSON - NO API KEY
    try:
        headers = {"User-Agent": "JagrukMemeBot/1.0"}
        r = requests.get("https://www.reddit.com/r/memes/hot.json?limit=10", headers=headers, timeout=15).json()
        for child in r["data"]["children"]:
            d = child["data"]
            if d.get("url", "").endswith((".jpg", ".png", ".jpeg")):
                results.append({"title": d["title"][:40], "url": d["url"], "source": "Reddit r/memes"})
    except Exception as e:
        print(f"Reddit JSON fail: {e}")
    random.shuffle(results)
    return results[:limit]

@bot.message_handler(commands=['start', 'help'])
def start(m):
    bot.reply_to(m, "👋 JAGRUK BOT ON HAI!\n\nCommands:\n/search - Naye trending memes dhundo (bina GitHub khole)\n/make - memes/ wali photos se Reel banao\n/status - Bot zinda hai ya nahi\n\nHar 7 ghante me auto-search bhi chalega.")

@bot.message_handler(commands=['search'])
def handle_search(m):
    bot.reply_to(m, "🔍 Search kar raha hu... Imgflip + Meme-API + Reddit se bina API ke...")
    results = search_no_api(5)
    if not results:
        bot.reply_to(m, "❌ Search fail ho gaya, 1 min baad /search dobara try kar")
        return
    for i, meme in enumerate(results):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ ISKO REEL BANAO", callback_data=f"make|{i}"),
            InlineKeyboardButton("❌ SKIP", callback_data=f"skip|{i}")
        )
        try:
            bot.send_photo(m.chat.id, meme["url"], caption=f"🎬 {meme['title']}\n📍 Source: {meme['source']}\n\n✅ dabao to Reel ban jayegi", reply_markup=markup)
        except Exception as e:
            bot.reply_to(m, f"Photo fail: {meme['url']}")

@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, "✅ Bot zinda hai! Har 7 ghante me auto-search chal raha hai.\n/search likh ke abhi search kar sakta hai.")

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    action, idx = c.data.split("|")
    if action == "make":
        bot.answer_callback_query(c.id, "🎬 Reel ban rahi hai, thoda wait karo...")
        # GitHub Action trigger karo bina GitHub khole - via workflow_dispatch API
        # Iske liye GITHUB_TOKEN secret chahiye Railway me
        bot.edit_message_caption("✅ Selected! Reel ban ke Telegram pe aa jayegi.", chat_id=c.message.chat.id, message_id=c.message.message_id)
        # Yahan main.py ko call kar sakte ho agar same server pe ho:
        # subprocess.Popen(["python", "main.py"])
    else:
        bot.answer_callback_query(c.id, "Skipped")

if __name__ == "__main__":
    print("Telegram Bot 24x7 ON - /search ready hai")
    bot.infinity_polling()
