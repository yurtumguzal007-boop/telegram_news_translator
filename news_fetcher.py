import urllib.request
import re
import html
import config

def fetch_latest_news():
    url = f"https://t.me/s/{config.SOURCE_CHANNEL}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_html = response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[تور تورىنى زىيارەت قىلىشتا خاتالىق]: {e}")
        return []

    # بۆلەكلەرگە ئايرىش
    delimiter = f'data-post="{config.SOURCE_CHANNEL}/'
    chunks = raw_html.split(delimiter)
    
    news_items = []
    
    for chunk in chunks[1:]:
        # ID نى ئېلىش
        id_match = re.match(r'^(\d+)"', chunk)
        if not id_match:
            continue
        msg_id = int(id_match.group(1))

        # تېكىست مەزمۇننى ئېلىش
        text_match = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', chunk, re.DOTALL)
        text = ""
        if text_match:
            raw_text = text_match.group(1)
            raw_text = re.sub(r'<br\s*/?>', '\n', raw_text)
            raw_text = re.sub(r'<[^>]+>', '', raw_text)
            text = html.unescape(raw_text).strip()

        # رەسىم بارمۇ يوق تەكشۈرۈش
        photo_match = re.search(r'tgme_widget_message_photo_wrap[^>]*style="[^"]*background-image:\s*url\(\'([^\']+)\'\)', chunk)
        if not photo_match:
            photo_match = re.search(r'tgme_widget_message_photo_wrap[^>]*style="[^"]*background-image:\s*url\(([^)]+)\)', chunk)
        
        photo_url = ""
        if photo_match:
            photo_url = photo_match.group(1).strip("'\"")

        # سىن (ۋىدېئو) بارمۇ يوق تەكشۈرۈش
        video_match = re.search(r'<video[^>]*src="([^"]+)"', chunk)
        video_url = video_match.group(1) if video_match else ""

        media_type = "text"
        media_url = ""
        if video_url:
            media_type = "video"
            media_url = video_url
        elif photo_url:
            media_type = "photo"
            media_url = photo_url

        if text or media_url:
            news_items.append({
                "id": msg_id,
                "text": text,
                "media_type": media_type,
                "media_url": media_url
            })

    # تەرتىپى: كونا دىن يېڭىغا قاراپ (سۈزۈپ چىقىرىش ئۈچۈن)
    news_items.sort(key=lambda x: x["id"])
    return news_items
