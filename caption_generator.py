import random
from config import CAPTION_STYLE
FALLBACK={"hinglish":["Bhai ye toh mera hi scene hai 😭😂","Relatable hai toh share kar do yaar","POV: Syllabus dekh ke mera reaction","Ye wala toh dil se laga 😂","Mummy ne dekha toh khatam mai 😭","Engineering wale samjhenge 😂"],"english":["This one hit too hard 😭","Tag someone who does this 😂","Relatable? Follow for more"]}
def make_caption(title=""):
    style=CAPTION_STYLE.lower()
    try:
        from openai import OpenAI
        from config import OPENAI_API_KEY
        if OPENAI_API_KEY:
            c=OpenAI(api_key=OPENAI_API_KEY)
            r=c.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system","content":f"Write viral meme caption in {style}, 1-2 lines, funny. Context: {title}"}], max_tokens=60)
            cap=r.choices[0].message.content.strip()
            h="#memes #desimemes #indianmemes #hinglishmemes #jagruk_aadmi #funny #relatable #viral"
            return f"{cap}\n.\n.\n{h}"
    except Exception as e: print(e)
    cap=random.choice(FALLBACK.get(style, FALLBACK["hinglish"]))
    h="#memes #desimemes #indianmemes #hinglishmemes #jagruk_aadmi #funny #relatable #viral"
    return f"{cap}\n.\n.\n{h}"
