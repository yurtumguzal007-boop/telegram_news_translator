import requests
import config

API_BASE = f"https://api.telegram.org/bot{config.BOT_TOKEN}"

def send_text_news(text: str) -> bool:
    url = f"{API_BASE}/sendMessage"
    payload = {
        "chat_id": config.TARGET_CHANNEL,
        "text": text,
        "disable_web_page_preview": False
    }
    try:
        resp = requests.post(url, json=payload, timeout=20)
        data = resp.json()
        if data.get("ok"):
            return True
        else:
            print(f"[بۇيرۇق ئەۋەتىشتە خاتالىق]: {data.get('description')}")
            return False
    except Exception as e:
        print(f"[ئۇلىنىش خاتالىقى]: {e}")
        return False

def send_photo_news(photo_url: str, caption: str) -> bool:
    url = f"{API_BASE}/sendPhoto"
    payload = {
        "chat_id": config.TARGET_CHANNEL,
        "photo": photo_url,
        "caption": caption[:1024]
    }
    try:
        resp = requests.post(url, json=payload, timeout=25)
        data = resp.json()
        if data.get("ok"):
            return True
        else:
            print(f"[رەسىم ئەۋەتىشتە خاتالىق]: {data.get('description')}")
            # رەسىم ئەۋەتىلمىسە تېكىستىنى بولسىمۇ ئەۋەتىش
            return send_text_news(caption)
    except Exception as e:
        print(f"[ئۇلىنىش خاتالىقى]: {e}")
        return send_text_news(caption)

def send_video_news(video_url: str, caption: str) -> bool:
    url = f"{API_BASE}/sendVideo"
    payload = {
        "chat_id": config.TARGET_CHANNEL,
        "video": video_url,
        "caption": caption[:1024]
    }
    try:
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        if data.get("ok"):
            return True
        else:
            print(f"[سىن ئەۋەتىشتە خاتالىق]: {data.get('description')}")
            return send_text_news(caption)
    except Exception as e:
        print(f"[ئۇلىنىش خاتالىقى]: {e}")
        return send_text_news(caption)
