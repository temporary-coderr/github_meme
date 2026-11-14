import os, requests, uuid, datetime, random
from PIL import Image, ImageDraw, ImageFont, ImageOps

print("=== JAGRUK BOT FINAL - Zero Secret - Smart + Creative ===")

# ===== CONFIG - Koi Secret nahi chahiye =====
WATERMARK = "@jagruk_aadmi"
BRAND_COLOR = (255, 214, 10)

# Hinglish captions - Title se smart choose karega
CAPTIONS_POOL = [
    "Bhai ye toh mera hi scene hai 😭😂",
    "Relatable hai toh share kar do yaar",
    "Tag karo us dost ko jo ye karta hai 😂",
    "POV: Ye dekh ke mera reaction",
    "Ye wala toh dil se laga 😂",
    "Mummy ne dekha toh khatam mai 😭",
    "Bhai ye dard khatam kahe nahi hota",
]

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Arial Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def wrap_text(text, font, max_w, draw):
    words = text.split(); lines=[]; cur=""
    for w in words:
        test = cur+" "+w if cur else w
        if draw.textlength(test, font=font) <= max_w: cur=test
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def smart_caption(title):
    # Title se smart caption - bina AI ke
    t = title.lower() if title else ""
    if "microsoft" in t or "ai" in t or "code" in t:
        return "Bhai AI ne toh sabki naukri kha li 😂"
    if "exam" in t or "study" in t or "school" in t:
        return "POV: Exam se ek raat pehle mera haal 😭"
    if "dog" in t or "cat" in t or "animal" in t:
        return "Bhai iska toh roz ka hai 😂"
    if "mom" in t or "mummy" in t or "dad" in t or "papa" in t:
        return "Mummy ne dekh liya toh khatam 😭"
    if "salary" in t or "money" in t or "job" in t:
        return "Salary aate hi khatam, ye dukh khatam kahe nahi hota"
    if "wifi" in t or "internet" in t or "phone" in t:
        return "WiFi band hote hi sabko yaad aata hai 😂"
    return random.choice(CAPTIONS_POOL)

def transformative_restlye(image_path, title):
    # ===== CREATIVITY - Har photo pe naya look =====
    # 1. Open + crop 2% (hash change - copy nahi lagega)
    img = Image.open(image_path).convert("RGB")
    w,h = img.size
    img = img.crop((int(w*0.02), int(h*0.02), int(w*0.98), int(h*0.98)))
    img = ImageOps.autocontrast(img, cutoff=1)
    # 2. Feed version - 1080x1350 (4:5) - Portrait, Instagram pe sabse zyada reach
    W,H = 1080, 1350
    canvas = Image.new("RGB", (W,H), (10,10,10))
    # Meme area
    tw = 1000; r = tw/img.width; th = int(img.height*r)
    if th > 850:
        th=850; r=th/img.height; tw=int(img.width*r)
    img2 = img.resize((tw,th), Image.LANCZOS)
    canvas.paste(img2, ((W-tw)//2, 160))
    draw = ImageDraw.Draw(canvas)
    # Brand header
    draw.rectangle([0,0,W,100], fill=BRAND_COLOR)
    draw.text((30,28), "JAGRUK MEMES", font=get_font(42), fill=(0,0,0))
    draw.text((W-320,28), WATERMARK, font=get_font(32), fill=(0,0,0))
    # Top Hinglish - Smart caption from title
    top_text = smart_caption(title)
    f = get_font(52)
    lines = wrap_text(top_text, f, 950, draw)
    ty = 110
    for line in lines:
        tw2 = draw.textlength(line, font=f)
        draw.text(((W-tw2)//2, ty), line, font=f, fill=(255,255,255), stroke_width=4, stroke_fill=(0,0,0))
        ty+=65
    # Bottom - Tag line
    f2 = get_font(50)
    bottom = "Tag your friend 😂"
    tw2 = draw.textlength(bottom, font=f2)
    draw.text(((W-tw2)//2, H-110), bottom, font=f2, fill=BRAND_COLOR, stroke_width=3, stroke_fill=(0,0,0))
    # Border + watermark
    draw.rectangle([0,0,W-1,H-1], outline="#FFD60A", width=12)
    draw.text((20, H-40), WATERMARK, font=get_font(28), fill=(255,255,255))
    # Save Feed version
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = f"output/{today}"
    os.makedirs(folder, exist_ok=True)
    feed_path = f"{folder}/meme_{uuid.uuid4().hex[:6]}_feed.jpg"
    canvas.save(feed_path, quality=92)
    # Reel version - 1080x1920 (9:16) - Feed wali ko beech me rakh ke
    W2,H2 = 1080,1920
    canvas2 = Image.new("RGB", (W2,H2), (0,0,0))
    # Feed image ko resize karke beech me
    feed_img = Image.open(feed_path)
    feed_img = feed_img.resize((1080,1350))
    canvas2.paste(feed_img, (0, (H2-1350)//2))
    reel_path = feed_path.replace("_feed.jpg", "_reel.jpg")
    canvas2.save(reel_path, quality=92)
    return feed_path, reel_path

def fetch_memes(count=5):
    print("Meme API se search kar raha hu (bina Secret)...")
    try:
        r = requests.get(f"https://meme-api.com/gimme/{count}", timeout=15)
        print(f"Status: {r.status_code}")
        data = r.json()
        memes = data.get("memes", [])
        print(f"Mile: {len(memes)}")
        return memes
    except Exception as e:
        print(f"Meme API FAIL: {e}")
        return []

def run(count=5):
    memes = fetch_memes(count)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = f"output/{today}"
    os.makedirs(folder, exist_ok=True)
    saved = 0
    if memes:
        for i, m in enumerate(memes):
            try:
                print(f"Downloading {i+1}: {m.get('title','')[:50]}")
                rr = requests.get(m.get("url"), timeout=15)
                if rr.status_code==200:
                    temp = f"temp_{i}.jpg"
                    open(temp,"wb").write(rr.content)
                    feed, reel = transformative_restlye(temp, m.get("title",""))
                    # Caption file
                    cap = smart_caption(m.get("title",""))
                    hashtags = "#memes #desimemes #indianmemes #hinglishmemes #jagruk_aadmi #funny #relatable #viral"
                    with open(feed.replace("_feed.jpg","_caption.txt"),"w",encoding="utf-8") as f:
                        f.write(f"Source: Meme API\nTitle: {m.get('title','')}\n\n--- CAPTION ---\n\n{cap}\n.\n.\n{hashtags}")
                    os.remove(temp)
                    saved+=1
                    print(f"Saved: {feed} + {reel}")
            except Exception as e:
                print(f"Fail {i}: {e}")
    if saved==0:
        print("API fail, khud ke 5 custom meme bana raha hu...")
        topics = ["Exam se ek raat pehle","Mummy ka phone aane par","Salary aate hi khatam","Monday morning office","WiFi band hone par"]
        for i, t in enumerate(topics):
            # Custom meme - sirf text, koi download nahi - 100% original
            img = Image.new("RGB",(1080,1080),(255,214,10))
            draw = ImageDraw.Draw(img)
            draw.rectangle([50,50,1030,1030], fill=(0,0,0))
            draw.text((80,200), t.upper(), font=get_font(60), fill=(255,255,255))
            draw.text((80,600), "Tag your friend 😂", font=get_font(50), fill=(255,214,10))
            draw.text((80,900), WATERMARK, font=get_font(45), fill=(255,255,255))
            path = f"{folder}/meme_{i+1}_feed.jpg"
            img.save(path)
            open(f"{folder}/meme_{i+1}_caption.txt","w",encoding="utf-8").write(f"{t}\n\nTag your friend 😂\n#memes #desimemes #jagruk_aadmi")
            saved+=1
    print(f"=== DONE - Total: {saved} memes in {folder} ===")
    print(f"Files: {os.listdir(folder)}")

if __name__=="__main__":
    run(5)
