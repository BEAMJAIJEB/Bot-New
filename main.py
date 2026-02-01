import feedparser
import requests
import time
import os
from flask import Flask

# ================= CONFIG =================
RSS_URL = "https://rss.app/feeds/gDMH42xLPnSfEB6Q.xml"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1464073685072740383/Fr2NA2BMrp_JT_ghxfPfFZExlhRIrg-eH1O4N_sIEeAiYuz64Gg9alIsUf66co1wQ8Zk"
CHECK_INTERVAL = 60  # ตรวจข่าวทุก 60 วินาที
SENT_FILE = "sent.txt"
# =========================================

app = Flask(__name__)

@app.route("/")
def home():
    return "News Bot is running"

# โหลดข่าวที่เคยส่งแล้ว
def load_sent():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

# บันทึกข่าวที่ส่งแล้ว
def save_sent(link):
    with open(SENT_FILE, "a", encoding="utf-8") as f:
        f.write(link + "\n")

def send_to_discord(title, link):
    data = {
        "content": f"🌍 **World Economy News**\n**{title}**\n{link}"
    }
    requests.post(DISCORD_WEBHOOK, json=data, timeout=10)

def check_news():
    sent = load_sent()
    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("❌ ไม่พบข่าวใน RSS")
        return

    for entry in feed.entries[:5]:  # เอาข่าวใหม่สุด 5 ข่าว
        link = entry.link
        title = entry.title

        if link in sent:
            continue

        send_to_discord(title, link)
        save_sent(link)
        print("✅ ส่งข่าว:", title)

def bot_loop():
    print("🤖 Bot started")
    while True:
        try:
            check_news()
        except Exception as e:
            print("⚠️ Error:", e)
        time.sleep(CHECK_INTERVAL)

# ===== START =====
if __name__ == "__main__":
    from threading import Thread
    Thread(target=bot_loop).start()
    app.run(host="0.0.0.0", port=10000)