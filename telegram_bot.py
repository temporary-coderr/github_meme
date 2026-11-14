"""
STEP 2 - TELEGRAM BOT: Tumhare phone pe Approve dabate hi Instagram pe post karega
Isko Railway / Render / ya apne laptop pe chalana hai - 24x7 chalta rahega
"""
import os, requests, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
IG_TOKEN = os.getenv("INSTAGRAM_TOKEN")  # Meta se mila Long Lived Token
IG_USER_ID = os.getenv("INSTAGRAM_USER_ID")  # jagruk_aadmi ka IG Business ID

# GitHub raw URL - jaha meme pade hai
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/temporary-coderr/github_meme/main/"

def post_to_instagram(image_url, caption):
    """Instagram Graph API se post - Official, Ban nahi hoga"""
    print(f"Posting to Instagram: {image_url}")
    # 1. Container banao
    url1 = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    r1 = requests.post(url1, data={"image_url": image_url, "caption": caption, "access_token": IG_TOKEN})
    print("Container:", r1.text)
    if r1.status_code != 200:
        return False, r1.text
    creation_id = r1.json().get("id")
    # 2. Publish karo
    url2 = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    r2 = requests.post(url2, data={"creation_id": creation_id, "access_token": IG_TOKEN})
    print("Publish:", r2.text)
    return r2.status_code == 200, r2.text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! 🙏\nMai Jagruk Meme Bot hu.\n\nGitHub se meme aayenge, tum ✅ dabao, mai Instagram @jagruk_aadmi pe post kar dunga.\n\nCommands:\n/meme - Naya meme bhejo\n/status - Kitne pending hai")

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, photo_path = query.data.split("|", 1)
    if action == "APPROVE":
        await query.edit_message_caption(caption="⏳ Posting to Instagram... Ruko 10 sec")
        # GitHub se public URL banao
        image_url = GITHUB_RAW_BASE + photo_path
        # Caption file se caption lo
        caption = query.message.caption or "Follow @jagruk_aadmi for more memes 😂 #memes #jagruk_aadmi"
        ok, res = post_to_instagram(image_url, caption)
        if ok:
            await query.edit_message_caption(caption="✅ POST HO GAYA! Instagram pe check karo @jagruk_aadmi")
        else:
            await query.edit_message_caption(caption=f"❌ Post fail hua: {res[:300]}\nToken check karo ya manually post karo")
    elif action == "REJECT":
        await query.edit_message_caption(caption="❌ Skip kar diya. Agla meme bhej raha hu...")
    elif action == "EDIT":
        await query.edit_message_caption(caption="✏️ Naya caption bhejo, mai usi se post kar dunga.\nAbhi ke liye isko SKIP kar diya.")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))
    print("Telegram Bot chal raha hai... Phone pe /start bhejo")
    app.run_polling()
