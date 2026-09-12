import os
from dotenv import load_dotenv

load_dotenv()

# مەنبە قانال (ئەرەپچە)
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL", "ajMubasher")

# نىشان قانال (ئۇيغۇرچە)
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "@DUNYA_NEWS1")

# سۈنئىي ئەقىل ئاچقۇچى
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# تېلېگرامما روبوت توكىنى (@DUNYA_NWES1bot)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# تەكشۈرۈش ئارىلىقى (سېكۇنت)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "25"))

# خەۋەر ئاخىرىغا قوشۇلىدىغان قانال بەلگىسى
CHANNEL_FOOTER = """

📢 قانىلىمىزغا ئەزا بولۇشنى ئۇنۇتماڭ:
🔗 https://t.me/DUNYA_NEWS1"""
