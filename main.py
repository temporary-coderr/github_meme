
import os
import random
import requests
from pathlib import Path

try:
    from PIL import Image
    if not hasattr(Image, "ANTIALIAS"):
        Image.ANTIALIAS = Image.LANCZOS
except Exception:
    pass

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
MEMES_FOLDER = Path("memes")
OUTPUT_FOLDER = Path("output")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def make_video(image_path, output_path):
    from moviepy.editor import ImageClip
    import numpy as np
    from PIL import Image as PILImage

    zoom = random.choice(["zoom_in", "zoom_out", "none"])
    light = random.choice(["shake", "flash", "none", "none"])
    print("Effects:", zoom, light, image_path.name)

    clip = ImageClip(str(image_path)).set_duration(7)
    clip = clip.resize(height=1280)
    if clip.w > 720:
        clip = clip.crop(x1=clip.w / 2 - 360, x2=clip.w / 2 + 360, y1=0, y2=1280)
    else:
        clip = clip.resize(width=720)
        if clip.h > 1280:
            clip = clip.crop(y1=clip.h / 2 - 640, y2=clip.h / 2 + 640)

    W = 720
    H = 1280

    def zoom_crop(get_frame, t):
        frame = get_frame(t)
        if zoom == "zoom_in":
            scale = 1.0 - 0.02 * t
        elif zoom == "zoom_out":
            scale = 0.90 + 0.02 * t
        else:
            return frame
        cw = int(W * scale)
        ch = int(H * scale)
        x1 = (W - cw) // 2
        y1 = (H - ch) // 2
        cropped = frame[y1:y1 + ch, x1:x1 + cw]
        pil = PILImage.fromarray(cropped)
        pil = pil.resize((W, H), PILImage.LANCZOS)
        return np.array(pil)

    clip = clip.fl(zoom_crop)

    def light_effect(get_frame, t):
        frame = get_frame(t)
        if light == "shake" and int(t / 0.8) % 2 == 0:
            frame = np.roll(frame, 3, axis=1)
            frame[:, :3] = frame[:, 3:4]
        if light == "flash" and (int(t * 2) % 4 == 0 and t % 1 < 0.06):
            frame = np.clip(frame * 1.15 + 15, 0, 255).astype(np.uint8)
        return frame

    if light != "none":
        clip = clip.fl(light_effect)

    clip.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio=False,
        preset="ultrafast",
        bitrate="1200k",
        threads=2,
        logger=None,
    )
    clip.close()
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print("Done:", output_path, "Size:", round(size_mb, 1), "MB")
    return size_mb

def search_no_api():
    print("Search...")
    found = []
    try:
        r = requests.get("https://api.imgflip.com/get_memes", timeout=15).json()
        memes = r["data"]["memes"]
        for m in random.sample(memes, 5):
            found.append((m["name"], m["url"]))
    except Exception as e:
        print("Imgflip fail:", e)
    try:
        r = requests.get("https://meme-api.com/gimme/5", timeout=15).json()
        for m in r.get("memes", []):
            found.append((m["title"][:30], m["url"]))
    except Exception as e:
        print("Meme-API fail:", e)
    MEMES_FOLDER.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(found[:5]):
        name, url = item
        try:
            data = requests.get(url, timeout=15).content
            (MEMES_FOLDER / ("search_" + str(i) + ".jpg")).write_bytes(data)
            print("Downloaded:", name)
        except Exception as e:
            print("Download fail:", e)

def send_telegram(video_path, name):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram skip - secrets nahi")
        return
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendVideo"
    size = video_path.stat().st_size / (1024 * 1024)
    caption = "Meme Ready - " + name + " - Size: " + str(round(size, 1)) + " MB - 7 sec"
    with open(video_path, "rb") as f:
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption}, files={"video": f}, timeout=120)
    print("Telegram:", r.status_code)

def main():
    existing = []
    if MEMES_FOLDER.exists():
        existing = list(MEMES_FOLDER.glob("*"))
    if not existing:
        search_no_api()
    for img in MEMES_FOLDER.glob("*"):
        if img.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue
        out = OUTPUT_FOLDER / (img.stem + "_reel.mp4")
        if out.exists():
            continue
        make_video(img, out)
        send_telegram(out, img.name)
    print("Done All")

if __name__ == "__main__":
    main()
