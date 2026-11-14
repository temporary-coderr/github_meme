import os, glob, requests, json, time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(photo_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ POST KARO", "callback_data": f"APPROVE|{photo_path}"}],
            [{"text": "❌ SKIP KARO", "callback_data": f"REJECT|{photo_path}"}],
        ]
    }
    with open(photo_path, "rb") as f:
        files = {"photo": f}
        data = {"chat_id": CHAT_ID, "caption": caption, "reply_markup": json.dumps(keyboard)}
        r = requests.post(url, files=files, data=data)
        print(f"Sent {photo_path}: {r.status_code}")
        return r.status_code == 200

if __name__ == "__main__":
    # SIRF AAJ ke naye meme bhejo, purane nahi
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    files = sorted(glob.glob(f"output/{today}/*_feed.jpg"))
    print(f"Found {len(files)} NEW memes for today {today} - Purane nahi bhejunga")
    
    for fp in files:
        cap_path = fp.replace("_feed.jpg", "_caption.txt")
        caption = open(cap_path, encoding="utf-8").read()[:900] if os.path.exists(cap_path) else "New Meme"
        ok = send_to_telegram(fp, caption)
        if ok:
            # ✅ Bhej diya to DELETE kar do, taaki dobara na bheje
            print(f"Deleting {fp} after send...")
            try:
                os.remove(fp)
                # Reel + Caption bhi delete karo
                reel = fp.replace("_feed.jpg", "_reel.jpg")
                if os.path.exists(reel): os.remove(reel)
                if os.path.exists(cap_path): os.remove(cap_path)
                print(f"Deleted {fp}")
            except Exception as e:
                print(f"Delete fail: {e}")
        time.sleep(2)
    print("DONE - Sab naye meme bhej diye aur delete kar diye, agli baar sirf naye jayenge")
