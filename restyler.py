from PIL import Image, ImageDraw, ImageFont, ImageOps
import os, uuid, random
def _font(s):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/System/Library/Fonts/Arial Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p,s)
            except: pass
    return ImageFont.load_default()
def _wrap(t,f,max_w,d):
    words=t.split(); lines=[]; cur=""
    for w in words:
        test=cur+" "+w if cur else w
        if d.textlength(test,font=f)<=max_w: cur=test
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def restyle_meme(image_path, top_text="", bottom_text="", watermark="@jagruk_aadmi"):
    img=Image.open(image_path).convert("RGB")
    w,h=img.size
    img=img.crop((int(w*0.01),int(h*0.01),int(w*0.99),int(h*0.99)))
    img=ImageOps.autocontrast(img, cutoff=1)
    W,H=1080,1350
    canvas=Image.new("RGB",(W,H),(10,10,10))
    tw=1000; r=tw/img.width; th=int(img.height*r)
    if th>900:
        th=900; r=th/img.height; tw=int(img.width*r)
    img2=img.resize((tw,th), Image.LANCZOS)
    canvas.paste(img2, ((W-tw)//2, 140))
    draw=ImageDraw.Draw(canvas)
    draw.rectangle([0,0,W,100], fill=(255,214,10))
    draw.text((30,28),"JAGRUK MEMES", font=_font(42), fill=(0,0,0))
    draw.text((W-320,28),watermark, font=_font(32), fill=(0,0,0))
    if top_text:
        f=_font(56); lines=_wrap(top_text.upper(),f,950,draw); ty=110
        for line in lines:
            tw2=draw.textlength(line,font=f); draw.text(((W-tw2)//2,ty),line,font=f,fill=(255,255,255),stroke_width=4,stroke_fill=(0,0,0)); ty+=70
    if bottom_text:
        f=_font(54); lines=_wrap(bottom_text,f,950,draw); by=H-120-len(lines)*65
        for line in lines:
            tw2=draw.textlength(line,font=f); draw.text(((W-tw2)//2,by),line,font=f,fill=(255,214,10),stroke_width=4,stroke_fill=(0,0,0)); by+=65
    draw.rectangle([0,0,W-1,H-1], outline="#FFD60A", width=12)
    draw.text((20,H-40),watermark, font=_font(28), fill=(255,255,255))
    os.makedirs("output", exist_ok=True)
    out=f"output/{uuid.uuid4().hex[:8]}.jpg"
    canvas.save(out, quality=92)
    return out
