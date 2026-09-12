import os
from dotenv import load_dotenv

load_dotenv()

# مەنبە قانال (ئەرەپچە)
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL", "ajMubasher")

# نىشان قانال (ئۇيغۇرچە)
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "@DUNYA_NEWS1")

# سۈنئىي ئەقىل ئاچقۇچى
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6KGvIiWwxSLnropKcPfjluCH-FRFT6DRWbOd3v8sMHOfA")

# تېلېگرامما روبوت توكىنى (@DUNYA_NWES1bot)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8715293160:AAHSh7rCNLDPAn7mIEUtSLnPmlA71A-bTO4")

# تەكشۈرۈش ئارىلىقى (سېكۇنت)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "25"))

# خەۋەر ئاخىرىغا قوشۇلىدىغان قانال بەلگىسى
CHANNEL_FOOTER = """

📢 قانىلىمىزغا ئەزا بولۇشنى ئۇنۇتماڭ:
🔗 https://t.me/DUNYA_NEWS1"""
