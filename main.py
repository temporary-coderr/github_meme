import os, requests, uuid, datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps

print("=== JAGRUK BOT - NO CAPTION MODE ===")
print("Bot koi caption nahi lagayega")
WATERMARK = "@jagruk_aadmi"
BRAND_COLOR = (255, 214, 10)

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def clean_restlye(image_path):
    # NO CAPTION - Sirf Header + Photo + Watermark
    img = Image.open(image_path).convert("RGB")
    w,h = img.size
    img = img.crop((int(w*0.01), int(h*0.01), int(w*0.99), int(h*0.99)))
    img = ImageOps.autocontrast(img, cutoff=1)
    W,H = 1080, 1350
    canvas = Image.new("RGB", (W,H), (10,10,10))
    draw = ImageDraw.Draw(canvas)
    # Header only - koi caption nahi
    draw.rectangle([0,0,W,90], fill=BRAND_COLOR)
    draw.text((25,22), "JAGRUK MEMES", font=get_font(40), fill=(0,0,0))
    draw.text((W-310,22), WATERMARK, font=get_font(30), fill=(0,0,0))
    # Photo full area - 100 to 1330, koi text nahi
    photo_top = 100
    photo_bottom = 1330
    photo_h = photo_bottom - photo_top
    photo_w = 1060
    r = min(photo_w/img.width, photo_h/img.height)
    tw2 = int(img.width*r); th2 = int(img.height*r)
    img2 = img.resize((tw2, th2), Image.LANCZOS)
    px = (W-tw2)//2
    py = photo_top + (photo_h - th2)//2
    canvas.paste(img2, (px, py))
    draw.text((20, H-38), WATERMARK, font=get_font(26), fill=(255,255,255))
    draw.rectangle([0,0,W-1,H-1], outline="#FFD60A", width=10)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = f"output/{today}"
    os.makedirs(folder, exist_ok=True)
    feed_path = f"{folder}/meme_{uuid.uuid4().hex[:6]}_feed.jpg"
    canvas.save(feed_path, quality=92)
    # Reel version
    W2,H2 = 1080,1920
    canvas2 = Image.new("RGB", (W2,H2), (0,0,0))
    feed_img = Image.open(feed_path).resize((1080,1350))
    canvas2.paste(feed_img, (0, (H2-1350)//2))
    reel_path = feed_path.replace("_feed.jpg", "_reel.jpg")
    canvas2.save(reel_path, quality=92)
    return feed_path, reel_path

def run(count=5):
    try:
        r = requests.get(f"https://meme-api.com/gimme/{count}", timeout=15)
        memes = r.json().get("memes", [])
    except: memes = []
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = f"output/{today}"; os.makedirs(folder, exist_ok=True)
    saved=0
    for i,m in enumerate(memes):
        try:
            rr = requests.get(m.get("url"), timeout=15)
            if rr.status_code==200:
                temp=f"temp_{i}.jpg"; open(temp,"wb").write(rr.content)
                feed, reel = clean_restlye(temp)
                with open(feed.replace("_feed.jpg","_caption.txt"),"w",encoding="utf-8") as f:
                    f.write(f"Original Title: {m.get('title','')}\n\n--- CAPTION KHALI HAI ---\nTum Telegram pe dekh ke khud likhoge\n\n#memes #jagruk_aadmi")
                os.remove(temp); saved+=1; print(f"Saved {feed} - NO CAPTION")
        except Exception as e: print(f"Fail {e}")
    print(f"DONE {saved} clean memes - NO CAPTION")

if __name__=="__main__": run(5)
