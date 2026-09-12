import time
import sys
import os

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import config
from database import init_db, is_news_posted, mark_news_posted, get_max_posted_id
from translator import translate_news
from news_fetcher import fetch_latest_news
import bot_sender
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Telegram News Translator 24/7 is running happily!")

    def log_message(self, format, *args):
        pass

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    try:
        server = HTTPServer(("0.0.0.0", port), HealthHandler)
        print(f"🌐 Health server running on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"Health server error: {e}")

def run():
    # Start web server for cloud hosting (Render)
    threading.Thread(target=start_health_server, daemon=True).start()

    print("=" * 60)
    print("🚀 تېلېگرامما ئاپتوماتىك خەۋەر تەرجىمە ۋە تارقىتىش سىستېمىسى")
    print(f"📡 مەنبە قانال: @{config.SOURCE_CHANNEL}")
    print(f"📢 نىشان قانال: {config.TARGET_CHANNEL}")
    print(f"⏱ كۆزىتىش ئارىلىقى: ھەر {config.CHECK_INTERVAL} سېكۇنتتا بىر قېتىم")
    print("=" * 60)

    init_db()

    # دەسلەپكى قوزغىلىش: ئالدىنقى بار بولغان كونا خەۋەرلەرنى ساندانغا قوشۇپ قويۇش
    # بۇ ئارقىلىق دەسلەپ قوزغالغاندا كونا 20 خەۋەرنى قالايمىقان تەكرار چىقىرىۋېتىشنىڭ ئالدىنى ئالىدۇ
    initial_news = fetch_latest_news()
    max_id = get_max_posted_id()

    if max_id == 0 and initial_news:
        print(f"ℹ️ تۇنجى قېتىم قوزغالدى. كونا {len(initial_news)} پارچە خەۋەر ساندانغا خاتىرىلەندى.")
        print("💡 ھازىردىن باشلاپ چىققان يېڭى خەۋەرلەر دەرھال تەرجىمە قىلىنىپ قانىلىڭىزغا يوللىنىدۇ...\n")
        for item in initial_news:
            mark_news_posted(item["id"], item["text"], "INITIAL_SYNC", item["media_type"], item["media_url"])
    
    print("✅ سىستېما تولۇق قوزغالدى ۋە يېڭى خەۋەر كۈتمەكتە...")

    while True:
        try:
            items = fetch_latest_news()
            for item in items:
                msg_id = item["id"]
                if not is_news_posted(msg_id):
                    print(f"\n⚡ [يېڭى ئەرەپچە خەۋەر تېپىلدى! ID: {msg_id}]")
                    arabic_text = item["text"]
                    if arabic_text:
                        print(f"📝 ئەسلى تېكىست: {arabic_text[:100]}...")
                        print("🤖 سۈنئىي ئەقىل (Gemini) ئۇيغۇرچىغا تەرجىمە قىلىۋاتىدۇ...")
                        translated = translate_news(arabic_text)
                    else:
                        translated = config.CHANNEL_FOOTER.strip()

                    if translated:
                        print(f"✨ ئۇيغۇرچە نەتىجە:\n{translated}\n")
                        print(f"📤 {config.TARGET_CHANNEL} قانىلىغا يوللىنىۋاتىدۇ...")

                        success = False
                        if item["media_type"] == "photo" and item["media_url"]:
                            success = bot_sender.send_photo_news(item["media_url"], translated)
                        elif item["media_type"] == "video" and item["media_url"]:
                            success = bot_sender.send_video_news(item["media_url"], translated)
                        else:
                            success = bot_sender.send_text_news(translated)

                        if success:
                            print(f"🎉 [مۇۋەپپەقىيەتلىك تارقىتىلدى! ID: {msg_id}]")
                            mark_news_posted(msg_id, arabic_text, translated, item["media_type"], item["media_url"])
                            time.sleep(3)
                        else:
                            print(f"⚠️ يوللاش مەغلۇپ بولدى. روبوتنىڭ قانالدا Admin ھوقۇقى بار-يوقلۇقىنى تەكشۈرۈڭ.")
                    else:
                        print(f"⚠️ تەرجىمە ئېلىنمىدى (ID: {msg_id})")

            time.sleep(config.CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 سىستېما ئىشلەتكۈچى تەرىپىدىن توختىتىلدى.")
            break
        except Exception as e:
            print(f"[كۈتۈلمىگەن خاتالىق]: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run()
