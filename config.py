import os
from dotenv import load_dotenv
load_dotenv()
REDDIT_CLIENT_ID=os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET=os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT=os.getenv("REDDIT_USER_AGENT","jagruk-meme-bot-github")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
CAPTION_STYLE=os.getenv("CAPTION_STYLE","hinglish")
WATERMARK_TEXT=os.getenv("WATERMARK_TEXT","@jagruk_aadmi")
SUBREDDITS=["IndianDankMemes","desimemes","dankmemes","memes","indianmemes","ProgrammerHumor"]
OUTPUT_DIR="output"
