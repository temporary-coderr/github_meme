import os, requests, uuid, datetime, random
from PIL import Image, ImageDraw, ImageFont

print("=== BOT START ===")
print("Current folder:", os.listdir("."))

# 1. Output folder pehle hi bana do - yehi missing tha
today = datetime.datetime.now().strftime("%Y-%m-%d")
folder = f"output/{today}"
os.makedirs(folder, exist_ok=True)
print(f"Folder ban gaya: {folder}")

def make_simple_meme(index, title):
    # Simple meme - bina kisi API ke, khud ka banayega
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), (255, 214, 10))
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, W-50, H-50], fill=(0, 0, 0))
    try:
        f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
    except:
        f1 = ImageFont.load_default(); f2 = f1
    draw.text((80, 200), title[:30], font=f1, fill=(255,255,255))
    draw.text((80, 500), "Tag your friend 😂", font=f2, fill=(255,214,10))
    draw.text((80, 900), "@jagruk_aadmi", font=f2, fill=(255,255,255))
    path = f"{folder}/meme_{index}.jpg"
    img.save(path)
    print(f"Saved: {path}")
    return path

def try_meme_api():
    print("Meme API try kar raha hu...")
    try:
        r = requests.get("https://meme-api.com/gimme/5", timeout=15)
        print(f"Meme API status: {r.status_code}")
        data = r.json()
        print(f"Meme API ne diye: {len(data.get('memes', []))}")
        return data.get("memes", [])
    except Exception as e:
        print(f"Meme API FAIL: {e}")
        return []

memes = try_meme_api()
saved = 0

if memes:
    for i, m in enumerate(memes[:5]):
        try:
            print(f"Downloading: {m.get('title')}")
            rr = requests.get(m.get("url"), timeout=15)
            if rr.status_code == 200:
                temp = f"temp_{i}.jpg"
                open(temp, "wb").write(rr.content)
                # Simple restyle - just copy with new name for now
                from PIL import Image as PILImage
                img = PILImage.open(temp).convert("RGB")
                img = img.resize((1080, 1080))
                path = f"{folder}/meme_{i+1}.jpg"
                img.save(path)
                caption = f"{m.get('title','')} \n\nTag your friend 😂\n.\n#memes #desimemes #jagruk_aadmi"
                open(f"{folder}/meme_{i+1}_caption.txt","w",encoding="utf-8").write(caption)
                os.remove(temp)
                saved += 1
                print(f"Saved API meme: {path}")
        except Exception as e:
            print(f"Download fail {i}: {e}")
else:
    print("API fail, khud ke meme bana raha hu...")

# Agar API se 0 meme mile to khud ke 5 bana do - kabhi khali nahi rahega
if saved == 0:
    print("Fallback - 5 custom meme bana raha hu")
    topics = ["Exam se ek raat pehle", "Mummy ka phone aane par", "Salary aate hi khatam", "Monday morning office", "WiFi band hone par"]
    for i, t in enumerate(topics):
        make_simple_meme(i+1, t)
        open(f"{folder}/meme_{i+1}_caption.txt","w",encoding="utf-8").write(f"{t}\n\nTag your friend 😂\n#memes #desimemes #jagruk_aadmi")
        saved += 1

print(f"=== BOT DONE - Total saved: {saved} ===")
print(f"Output list: {os.listdir(folder)}")
