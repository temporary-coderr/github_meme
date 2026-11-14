# JAGRUK MEME BOT - GITHUB SAVER VERSION
### Bot sirf meme banake GitHub me save karega, tum download karke Instagram pe post karoge

## Kya karega Bot?
1. Reddit + 9GAG se top viral memes lega
2. New Look dega: Yellow header, @jagruk_aadmi watermark, Hinglish text
3. Caption bana dega (caption.txt file me)
4. GitHub ke /output/2026-11-14/ folder me save karega
5. Tum GitHub se download karke @jagruk_aadmi pe post kar doge

## Setup - 5 min

### 1. GitHub Repo banao
- github.com > New Repository > Name: `jagruk-memes` > Public > Create
- Is zip ke saare files us repo me upload karo

### 2. Secrets daalo (GitHub me)
Repo > Settings > Secrets and variables > Actions > New repository secret
- Name: REDDIT_CLIENT_ID | Value: (reddit.com/prefs/apps se)
- Name: REDDIT_CLIENT_SECRET | Value: (same)
- Name: OPENAI_API_KEY | Value: (optional, bina iske bhi chalega)

### 3. Auto Run ON karo
Repo > Actions > Jagruk Meme Bot - Auto Save to GitHub > Enable
- Bot har din 10AM, 3PM, 8PM IST pe 5 naye memes bana ke GitHub me save karega
- Manual run ke liye: Actions > Run workflow > Run

### 4. Download & Post (Tumhara kaam - 2 min)
- GitHub Repo > output > Aaj ki date wale folder > meme_1.jpg download karo
- meme_1_caption.txt kholo, caption copy karo
- Instagram App > New Post > Reel > Photo select karo + Caption paste karo > Post

## Local me chalana hai to
```
pip install -r requirements.txt
cp .env.example .env  # fill keys
python main.py --once --count 5
# Memes output/ folder me milenge
./push_to_github.sh  # GitHub pe push karne ke liye
```

## Kya-kya save hota hai?
```
output/
  2026-11-14/
    meme_1.jpg
    meme_1_caption.txt  <- Caption copy-paste karne ke liye
    meme_2.jpg
    meme_2_caption.txt
```

## Kyu ye sabse safe hai?
- Koi Token nahi, koi Password nahi, koi Meta App nahi
- Koi Ban ka risk nahi - kyuki post tum khud kar rahe ho, bot nahi
- GitHub free hai, 24/7 chalta hai
