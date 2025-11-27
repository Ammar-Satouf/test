# keep_alive.py
# هذا الملف يقوم بتشغيل خادم ويب صغير باستخدام Flask
# للحفاظ على اتصال البوت (Keep-Alive) في بيئات الاستضافة التي تتطلب ذلك.

from flask import Flask
from threading import Thread

# إنشاء تطبيق Flask
app = Flask('')

@app.route('/')
def home():
    """الرد على طلبات Ping"""
    return "I'm alive! The Telegram Bot is running."

def run():
    """تشغيل خادم Flask في منفذ 8080"""
    # يجب أن يكون المنفذ 8080 ليتوافق مع معظم بيئات الاستضافة السحابية
    print("Starting Flask web server for Keep-Alive on port 8080...")
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """بدء تشغيل خادم الويب في خيط منفصل"""
    t = Thread(target=run)
    t.start()
    print("Keep-Alive thread started.")
