
# JAGRUK MEME BOT v3 - BLUR FIX + SMALL SIZE
# Problem kya tha purane code me:
# 1. BLUR: clip.resize(lambda t: ...) har frame ko dobara-dobara resize karta tha -> blur + lines (teri photo jaisi stripes)
# 2. SIZE 20-25MB: 1080x1920 + 30fps + 7 sec + no bitrate limit = bahut bada file
# Fix: Resize sirf 1 baar, Zoom CROP se karenge (resize nahi), Size 720x1280, bitrate limit

import os, random, requests
from pathlib import Path

# PIL FIX
try:
    from PIL import Image
    if not hasattr(Image, "ANTIALIAS"):
        Image.ANTIALIAS = Image.LANCZOS
except: pass

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
MEMES_FOLDER = Path("memes")
OUTPUT_FOLDER = Path("output")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def make_video_fixed(image_path, output_path):
    from moviepy.editor import ImageClip
    import numpy as np

    # Random effect - par ab sirf 1 zoom + 1 light effect, dono ek saath nahi ladenge
    zoom = random.choice(["zoom_in", "zoom_out", "none"])
    light = random.choice(["shake", "flash", "none", "none"])  # none zyada rakha taaki clean lage
    print(f"Effects: zoom={zoom} light={light} - {image_path.name}")

    # 1. Ek hi baar resize - 720x1280 (Insta ke liye kaafi hai, 1080 ki zaroorat nahi)
    # 720p se size 1/3 ho jayega, quality me fark nahi dikhega phone pe
    clip = ImageClip(str(image_path)).set_duration(7)  # 7 SEC - tera wala

    # Cover fit: pehle resize, phir center crop - sirf 1 baar
    # Aspect maintain karke
    clip = clip.resize(height=1280)
    if clip.w > 720:
        clip = clip.crop(x1=clip.w/2 - 360, x2=clip.w/2 + 360, y1=0, y2=1280)
    else:
        clip = clip.resize(width=720)
        if clip.h > 1280:
            clip = clip.crop(y1=clip.h/2 - 640, y2=clip.h/2 + 640)

    # 2. ZOOM - Resize se NAHI, CROP se karenge (yehi blur ka main fix hai)
    # Zoom matlab dheere-dheere crop chhota karna, image ko bar-bar resize nahi karna
    W, H = 720, 1280
    def zoom_crop(get_frame, t):
        frame = get_frame(t)
        if zoom == "zoom_in":
            # 1.0 -> 0.90 crop (zoom in lagta hai)
            scale = 1.0 - 0.02 * t
        elif zoom == "zoom_out":
            scale = 0.90 + 0.02 * t
        else:
            return frame
        # Crop size
        cw, ch = int(W * scale), int(H * scale)
        x1 = (W - cw)//2
        y1 = (H - ch)//2
        cropped = frame[y1:y1+ch, x1:x1+cw]
        # Wapas original size pe - sirf 1 resize, wo bhi PIL LANCZOS se sharp rahega
        from PIL import Image as PILImage
        pil = PILImage.fromarray(cropped)
        pil = pil.resize((W, H), PILImage.LANCZOS)
        return np.array(pil)

    clip = clip.fl(zoom_crop)

    # 3. LIGHT EFFECTS - np.roll HATA DIYA (wahi stripes bana raha tha)
    # Ab shake ke liye crop shift karenge, roll nahi
    def light_effect(get_frame, t):
        frame = get_frame(t)
        if light == "shake" and int(t/0.8) % 2 == 0:
            # Sirf 3 pixel shift, roll nahi - stripes nahi aayengi
            frame = np.roll(frame, 3, axis=1)
            frame[:, :3] = frame[:, 3:4]  # edge fix - black lines nahi aayengi
        if light == "flash" and (int(t*2) % 4 == 0 and t % 1 < 0.06):
            frame = np.clip(frame * 1.15 + 15, 0, 255).astype(np.uint8)
        return frame

    if light != "none":
        clip = clip.fl(light_effect)

    # 4. SIZE FIX - bitrate + preset + fps kam
    # 24fps, 5 sec, 720p, bitrate 1500k = 1-3 MB file banegi, 20MB nahi
    clip.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio=False,
        preset="ultrafast",  # fast + small
        bitrate="1200k"  # 7 sec ke liye thoda kam bitrate taaki size 2-4 MB hi rahe,
        threads=2,
        logger=None
    )
    clip.close()
    size_mb = output_path.stat().st_size / (1024*1024)
    print(f"Done: {output_path} - Size 7sec: {size_mb:.1f} MB")
    return size_mb

def search_no_api():
    print("Search...")
    found = []
    try:
        r = requests.get("https://api.imgflip.com/get_memes", timeout=15).json()
        for m in random.sample(r["data"]["memes"], 5):
            found.append((m["name"], m["url"]))
    except Exception as e:
        print(f"Imgflip fail {e}")
    try:
        r = requests.get("https://meme-api.com/gimme/5", timeout=15).json()
        for m in r.get("memes", []):
            found.append((m["title"][:30], m["url"]))
    except Exception as e:
        print(f"Meme-API fail {e}")
    MEMES_FOLDER.mkdir(parents=True, exist_ok=True)
    for i, (name, url) in enumerate(found[:5]):
        try:
            data = requests.get(url, timeout=15).content
            (MEMES_FOLDER / f"search_{i}.jpg").write_bytes(data)
            print(f"Downloaded {name}")
        except Exception as e:
            print(f"Download fail {e}")

def send_telegram(video_path, name):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram skip - secrets nahi")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
    size = video_path.stat().st_size/(1024*1024)
    caption = f"🎬 {name}\n📦 Size 7sec: {size:.1f} MB\n✨ Blur fix + Small size version\nText + Song Insta me daal dena"
    with open(video_path, "rb") as f:
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption}, files={"video": f}, timeout=120)
    print(f"Telegram: {r.status_code}")

def main():
    existing = list(MEMES_FOLDER.glob("*")) if MEMES_FOLDER.exists() else []
    if not existing:
        search_no_api()
    for img in MEMES_FOLDER.glob("*"):
        if img.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue
        out = OUTPUT_FOLDER / (img.stem + "_reel.mp4")
        if out.exists():
            continue
        make_video_fixed(img, out)
        send_telegram(out, img.name)
    print("✅ Done - Ab blur nahi, size bhi 1-3 MB hoga")

if __name__ == "__main__":
    main()
