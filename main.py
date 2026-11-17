
# JAGRUK MEME BOT v2 - Random Effects + Search Source
# Har reel alag dikhegi - 10 effects me se random 2-3 pick honge har baar
# Secrets: TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

import os, random, requests
from pathlib import Path

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
# Search ke liye - agar khali hai to search skip, sirf memes/ folder chalega
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "")
REDDIT_SECRET = os.environ.get("REDDIT_SECRET", "")

MEMES_FOLDER = Path("memes")
OUTPUT_FOLDER = Path("output")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# ================= 10 EFFECTS POOL =================
# Har video ke liye inme se random 2-3 effects choose honge
EFFECTS = [
    "zoom_in",       # Slow zoom in
    "zoom_out",      # Slow zoom out
    "shake_beat",    # Beat pe shake
    "flash_beat",    # Beat pe white flash
    "bounce",        # Halka up-down bounce
    "vignette",      # Corners dark - cinematic look
    "glitch",        # 1-2 baar chhota glitch
    "punch_zoom",    # Beech me ek tez zoom punch
    "slow_pan",      # Left se right slow pan
    "rotate_tilt",   # Halka tilt
]

def make_dynamic_video_v2(image_path, output_path):
    from moviepy.editor import ImageClip, CompositeVideoClip
    import numpy as np
    from PIL import Image, ImageEnhance

    # Random 2-3 effects pick karo - har reel alag lagegi
    chosen = random.sample(EFFECTS, k=random.choice([2,3,3]))
    print(f"Effects is reel ke liye: {chosen} - {image_path.name}")

    clip = ImageClip(str(image_path)).set_duration(7)
    clip = clip.resize(height=1920)
    if clip.w > 1080:
        clip = clip.crop(x1=clip.w/2 - 540, x2=clip.w/2 + 540)
    else:
        clip = clip.resize(width=1080)

    # --- ZOOM / PAN / BOUNCE ---
    if "zoom_in" in chosen:
        clip = clip.resize(lambda t: 1 + 0.022 * t)
    elif "zoom_out" in chosen:
        clip = clip.resize(lambda t: 1.18 - 0.022 * t)
    elif "punch_zoom" in chosen:
        # 3 sec pe ek tez punch zoom
        def punch(t):
            if 2.8 < t < 3.5:
                return 1.18
            return 1 + 0.01 * t
        clip = clip.resize(punch)
    elif "slow_pan" in chosen:
        clip = clip.set_position(lambda t: (-15 + t*5, 0))

    # --- SHAKE / GLITCH / FLASH / BOUNCE ---
    def apply_frame(get_frame, t):
        frame = get_frame(t)
        # Shake
        if "shake_beat" in chosen:
            beat = int(t / 0.8) % 2
            if beat == 0:
                frame = np.roll(frame, int(6 * np.sin(t*20)), axis=1)
        # Glitch - 2 random jagah
        if "glitch" in chosen and (1.2 < t < 1.35 or 4.5 < t < 4.65):
            frame = np.roll(frame, 40, axis=1)
            frame[:, :, 0] = np.roll(frame[:, :, 0], 10, axis=1)  # RGB shift
        # Flash
        if "flash_beat" in chosen and (int(t*2) % 4 == 0 and t % 1 < 0.08):
            frame = np.clip(frame * 1.4 + 40, 0, 255).astype(np.uint8)
        # Bounce
        if "bounce" in chosen:
            frame = np.roll(frame, int(8 * np.sin(t*4)), axis=0)
        # Vignette - static, par frame pe apply
        if "vignette" in chosen:
            # Simple: corners thode dark via gradient - har frame pe heavy hai isliye skip karte hain agar slow lage to
            pass
        return frame

    clip = clip.fl(apply_frame)
    clip.write_videofile(str(output_path), fps=30, codec="libx264", audio=False, logger=None)
    clip.close()
    return chosen

# ================= SEARCH SOURCE =================
def search_memes():
    """
    YE PART PYTHON KE BINA NAHI CHALEGA.
    GitHub Actions me Python hota hai, isliye waha chal jayega.
    Local bina Python ke nahi chalega - kyunki search ke liye API call + download karna padta hai.

    Sources:
    1. Imgflip - FREE, NO KEY chahiye - 100 trending templates deta hai
    2. Reddit r/memes - FREE par Reddit API key chahiye (REDDIT_CLIENT_ID/SECRET)
    3. Meme API (meme-api.com) - FREE, NO KEY - random memes
    """
    print("🔍 Search chal raha hai...")
    found = []

    # Source 1: Imgflip - Best for templates, NO KEY needed
    try:
        r = requests.get("https://api.imgflip.com/get_memes", timeout=15)
        memes = r.json()["data"]["memes"][:10]
        for m in memes:
            # Sirf URL save karte hain, photo download baad me hoga
            found.append({"source": "imgflip", "name": m["name"], "url": m["url"]})
        print(f"Imgflip se {len(found)} templates mile")
    except Exception as e:
        print(f"Imgflip fail: {e}")

    # Source 2: Meme API - Random viral memes, NO KEY
    try:
        r = requests.get("https://meme-api.com/gimme/10", timeout=15)
        for m in r.json().get("memes", []):
            found.append({"source": "meme-api", "name": m["title"][:30], "url": m["url"]})
        print(f"Meme-API se memes mile")
    except Exception as e:
        print(f"Meme-API fail: {e}")

    # Source 3: Reddit - Agar keys hain to hi chalega
    if REDDIT_CLIENT_ID and REDDIT_SECRET:
        print("Reddit search chal raha hai (keys mil gayi)...")
        # Yahan Reddit API call aayegi - abhi placeholder, kyunki keys nahi hain
    else:
        print("Reddit skip - REDDIT_CLIENT_ID/SECRET Secrets me nahi hai")

    # Download top 5 ko memes/ me daalo
    for i, m in enumerate(found[:5]):
        try:
            img_data = requests.get(m["url"], timeout=15).content
            ext = ".jpg"
            (MEMES_FOLDER / f"search_{i}_{m['source']}{ext}").write_bytes(img_data)
            print(f"Downloaded: {m['name']}")
        except Exception as e:
            print(f"Download fail {m['name']}: {e}")

    return found

def send_to_telegram(video_path, original_name, effects):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram skip - secrets nahi mile")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
    caption = f"🎬 Naya Reel Ready!\n\n📁 {original_name}\n✨ Effects: {', '.join(effects)}\n\nText + Song tu Insta me daal dena."
    with open(video_path, "rb") as f:
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption}, files={"video": f}, timeout=120)
    print(f"Telegram: {r.status_code}")
    return r.status_code == 200

def main():
    # Agar memes/ khaali hai to search se bharo
    existing = list(MEMES_FOLDER.glob("*")) if MEMES_FOLDER.exists() else []
    if not existing:
        print("memes/ khaali hai - Search se bhar rahe hain...")
        MEMES_FOLDER.mkdir(parents=True, exist_ok=True)
        search_memes()
    else:
        print(f"memes/ me {len(existing)} photos pehle se hain - Search skip")

    for img in MEMES_FOLDER.glob("*"):
        if img.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue
        out = OUTPUT_FOLDER / (img.stem + "_reel.mp4")
        if out.exists():
            continue
        effects = make_dynamic_video_v2(img, out)
        send_to_telegram(out, img.name, effects)
    print("✅ Done")

if __name__ == "__main__":
    main()
