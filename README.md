# JAGRUK MEME BOT - Full Package

## Kya hai isme?
- main.py - Static meme -> Dynamic Reel (10 random effects, NO TEXT, Search bina API ke)
- telegram_bot.py - Telegram se /search karne ke liye (24x7 Railway/Render/Laptop pe chalega)
- .github/workflows/meme_bot.yml - Har 7 ghante me auto chalega + manual run
- requirements.txt

## Secrets (GitHub > Settings > Secrets > Actions)
- TELEGRAM_TOKEN
- TELEGRAM_CHAT_ID

## Kaise chalaye?
1. Ye sab files apne repo me daalo (main.py replace karo)
2. memes/ me photo daalo ya khali chhodo (khali hai to auto-search chalega)
3. GitHub Actions > Run workflow dabao ya 7 ghante wait karo
4. Telegram pe video aayegi -> ✅ dabao -> ready -> Insta pe manually Text + Song laga ke post karo

## Telegram Commands (telegram_bot.py chalane pe)
- /start - Bot on hai ya nahi
- /search - Bina GitHub khole naye memes dhundo
- /status - Status check

## Sources - Sab Bina API Key ke
- Imgflip API - NO KEY
- Meme-API - NO KEY
- Reddit r/memes public JSON - NO KEY
- Reddit API (optional) - Key chahiye to skip ho jayega

## Note
- Video me TEXT nahi hai, text tu Insta me daalega
- Auto-post OFF hai, tu manually upload karega - account safe rahega
