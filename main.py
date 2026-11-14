import requests, os, uuid, datetime, random
from restyler import restyle_meme
from caption_generator import make_caption

def fetch_no_secret(count=5):
    memes = []
    # 1. Meme API - No Secret
    try:
        r = requests.get(f"https://meme-api.com/gimme/{count}", timeout=10)
        data = r.json()
        for m in data.get("memes", []):
            img_url = m.get("url")
            fname = f"temp_{uuid.uuid4().hex}.jpg"
            rr = requests.get(img_url, timeout=10)
            if rr.status_code == 200:
                open(fname, "wb").write(rr.content)
                memes.append({"file": fname, "title": m.get("title",""), "source": "Meme API"})
        print(f"Meme API se mile: {len(memes)}")
    except Exception as e:
        print(f"Meme API fail: {e}")

    # 2. Agar phir bhi kam hai to 9GAG se lo
    if len(memes) < count:
        try:
            r = requests.get("https://9gag.com/v1/group-posts/group/default/type/hot?after=&c=10", timeout=10, headers={"User-Agent":"Mozilla/5.0"})
            for p in r.json().get("data",{}).get("posts",[])[:count-len(memes)]:
                img = p.get("images",{}).get("image700",{}).get("url")
                if img:
                    fname = f"temp_{uuid.uuid4().hex}.jpg"
                    rr = requests.get(img, timeout=10)
                    if rr.status_code == 200:
                        open(fname,"wb").write(rr.content)
                        memes.append({"file": fname, "title": p.get("title",""), "source": "9GAG"})
            print(f"Total ab: {len(memes)}")
        except Exception as e:
            print(f"9GAG fail: {e}")
    return memes

def run(count=5):
    memes = fetch_no_secret(count)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = f"output/{today}"
    os.makedirs(folder, exist_ok=True)
    for i, meme in enumerate(memes):
        restyled = restyle_meme(meme["file"], top_text=meme["title"][:60], bottom_text="Tag your friend 😂")
        final = f"{folder}/meme_{i+1}.jpg"
        os.rename(restyled, final)
        caption = make_caption(meme["title"])
        open(f"{folder}/meme_{i+1}_caption.txt","w", encoding="utf-8").write(caption)
        os.remove(meme["file"])
        print(f"Saved: {final}")
    print("Done! Bina Secret ke ho gaya")

if __name__ == "__main__":
    run(5)
