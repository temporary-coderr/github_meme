"""
STEP 1 - SENDER: GitHub output/ folder se Telegram pe bhejo
Ye file GitHub Actions me chalegi - output/ me jo meme honge wo Telegram pe bhej degi
"""
import os, glob, requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(photo_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    # Inline buttons - Approve / Reject
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ POST KARO - Instagram pe daal do", "callback_data": f"APPROVE|{photo_path}"}],
            [{"text": "❌ SKIP KARO", "callback_data": f"REJECT|{photo_path}"}],
            [{"text": "✏️ CAPTION BADLO", "callback_data": f"EDIT|{photo_path}"}]
        ]
    }
    with open(photo_path, "rb") as f:
        files = {"photo": f}
        data = {"chat_id": CHAT_ID, "caption": caption, "reply_markup": __import__("json").dumps(keyboard)}
        r = requests.post(url, files=files, data=data)
        print(f"Sent {photo_path}: {r.status_code} {r.text[:200]}")

if __name__ == "__main__":
    # output/ me latest date folder ke saare feed meme lo
    files = sorted(glob.glob("output/*/*_feed.jpg"))
    print(f"Found {len(files)} memes to send")
    for fp in files:
        cap_path = fp.replace("_feed.jpg", "_caption.txt")
        caption = open(cap_path, encoding="utf-8").read()[:900] if os.path.exists(cap_path) else "New Meme - Post karu?"
        send_to_telegram(fp, caption)
        print("Waiting 2 sec...")
        __import__("time").sleep(2)
    print("DONE - Sab Telegram pe bhej diye")
