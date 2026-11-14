# JAGRUK - Folder -> Telegram -> Approve -> Instagram

## Flow
1. GitHub Actions (meme_bot.yml) - Meme banata hai -> output/ me save -> telegram_sender.py se Telegram pe bhejta hai
2. Tumhare Phone pe Telegram me meme aayega with 3 buttons:
   ✅ POST KARO - Instagram pe post ho jayega
   ❌ SKIP KARO
   ✏️ CAPTION BADLO
3. telegram_bot.py (Railway/Render/Laptop pe 24x7 chalega) - Tumhare ✅ dabate hi Instagram Graph API se post karega

## Setup - 10 min

### 1. Telegram Bot banao
- Telegram me @BotFather -> /newbot -> Naam: Jagruk Meme Bot
- Token milega -> GitHub Secrets me TELEGRAM_TOKEN me daalo
- Apne bot ko /start bhejo, fir browser me kholo:
  https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates
  Waha tumhara CHAT_ID milega -> GitHub Secrets me TELEGRAM_CHAT_ID

### 2. Instagram Token (Full Auto ke liye)
- Meta App se IG User ID + Long Lived Token lo
- Railway/Render ke Env me daalo: INSTAGRAM_TOKEN, INSTAGRAM_USER_ID, TELEGRAM_TOKEN
- Agar Token nahi hai to bhi Telegram pe approve ho jayega, par post manual karna padega

### 3. Files - Same repo me daalo
- main.py (purana wala)
- telegram_sender.py (naya)
- telegram_bot.py (naya - Railway pe chalega)
- requirements.txt (update)
- .github/workflows/meme_bot.yml (update - ab Telegram bhejega bhi)

### 4. Railway pe Bot chalao (Free)
- railway.app -> New Project -> GitHub Repo connect karo
- Start Command: python telegram_bot.py
- Env Vars daalo: TELEGRAM_TOKEN, INSTAGRAM_TOKEN, INSTAGRAM_USER_ID
- Done - Bot 24x7 chalega

## Kya hoga?
Phone pe Telegram kholo -> Meme aayega -> ✅ dabao -> Instagram pe post ho gaya!
