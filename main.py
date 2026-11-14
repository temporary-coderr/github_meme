"""
JAGRUK BOT - GITHUB SAVER VERSION
- Fetches memes from Reddit + 9GAG
- Restyles with new look + watermark
- Saves to /output folder with caption.txt
- GitHub Actions will auto-push to GitHub
- You download from GitHub and post manually to Instagram - 0 ban risk

Usage:
  python main.py --once --count 5   # save 5 memes
  python main.py --once --mode create --count 3  # create original memes
"""
import argparse, os, random, requests, uuid, datetime
from config import SUBREDDITS, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, OUTPUT_DIR, WATERMARK_TEXT
from restyler import restyle_meme
from caption_generator import make_caption

def fetch_reddit(limit=5):
    import praw
    reddit=praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)
    seen=set()
    if os.path.exists("seen_urls.txt"):
        seen=set(open("seen_urls.txt").read().splitlines())
    out=[]
    for sub in SUBREDDITS:
        try:
            for post in reddit.subreddit(sub).hot(limit=10):
                if post.url in seen: continue
                if not any(post.url.lower().endswith(e) for e in [".jpg",".jpeg",".png"]): continue
                if post.score<800: continue
                fname=f"temp_{uuid.uuid4().hex}.jpg"
                r=requests.get(post.url, timeout=10)
                if r.status_code==200:
                    open(fname,"wb").write(r.content)
                    out.append({"file":fname,"title":post.title,"source":f"r/{sub}"})
                    open("seen_urls.txt","a").write(post.url+"\n")
                    if len(out)>=limit: return out
        except Exception as e: print(f"r/{sub} error {e}")
    return out

def fetch_9gag(limit=5):
    try:
        r=requests.get("https://9gag.com/v1/group-posts/group/default/type/hot?after=&c=10", timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        data=r.json(); out=[]
        for p in data.get("data",{}).get("posts",[])[:limit]:
            img=p.get("images",{}).get("image700",{}).get("url")
            if img:
                fname=f"temp_{uuid.uuid4().hex}.jpg"
                rr=requests.get(img, timeout=10)
                if rr.status_code==200:
                    open(fname,"wb").write(rr.content)
                    out.append({"file":fname,"title":p.get("title",""),"source":"9GAG"})
        return out
    except Exception as e: print("9GAG fail",e); return []

def save_meme(meme, index):
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    folder=f"{OUTPUT_DIR}/{today}"
    os.makedirs(folder, exist_ok=True)
    # Restyle
    restyled=restyle_meme(meme["file"], top_text=meme["title"][:60], bottom_text="Tag your friend 😂", watermark=WATERMARK_TEXT)
    # Rename to nice name in dated folder
    final_path=f"{folder}/meme_{index+1}.jpg"
    os.rename(restyled, final_path)
    # Caption file
    caption=make_caption(meme["title"])
    with open(f"{folder}/meme_{index+1}_caption.txt","w", encoding="utf-8") as f:
        f.write(f"Source: {meme['source']}\nTitle: {meme['title']}\n\n--- CAPTION (copy paste) ---\n\n{caption}")
    # Cleanup temp
    try: os.remove(meme["file"])
    except: pass
    print(f"✅ Saved: {final_path}")
    return final_path

def run(count=5, mode="mix"):
    print(f"Fetching {count} memes - Mode: {mode}")
    memes=fetch_reddit(count)
    if len(memes)<count:
        memes+=fetch_9gag(count-len(memes))
    print(f"Got {len(memes)} memes")
    for i, meme in enumerate(memes):
        save_meme(meme, i)
    print(f"\nDone! Check {OUTPUT_DIR}/ folder")
    print("Download from GitHub and post manually to @jagruk_aadmi")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--once", action="store_true")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--mode", default="mix")
    a=p.parse_args()
    run(count=a.count, mode=a.mode)
