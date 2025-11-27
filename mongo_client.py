# mongo_client.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional
from pymongo.database import Database

# تحميل المتغيرات البيئية
load_dotenv()

# إعدادات الاتصال بقاعدة البيانات
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "telegram_bot_db")

# كائن الاتصال العمومي
_mongo_client: Optional[MongoClient] = None
_db: Optional[Database] = None

def get_mongo_db_client() -> Optional[Database]:
    """
    يقوم بإنشاء اتصال MongoDB (إذا لم يكن موجوداً) وإرجاع كائن قاعدة البيانات.
    يستخدم هذا الكائن بشكل متزامن بواسطة مكتبة pymongo.
    """
    global _mongo_client, _db

    if _db is not None:
        return _db
    
    if not MONGO_URI:
        print("⚠️ خطأ: متغير MONGO_URI البيئي غير موجود.")
        return None

    try:
        # إنشاء اتصال جديد
        _mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # محاولة الاتصال للتحقق
        _mongo_client.admin.command('ping') 
        
        _db = _mongo_client[MONGO_DB_NAME]
        print(f"✅ تم الاتصال بنجاح بقاعدة البيانات '{MONGO_DB_NAME}'.")
        return _db
    
    except Exception as e:
        print(f"❌ فشل الاتصال بقاعدة البيانات MongoDB: {e}")
        # إذا فشل الاتصال، يتم إعادة تعيين المتغيرات لمنع إعادة المحاولة الفاشلة
        _mongo_client = None
        _db = None
        return None

# ==============================================================================
# دالة إغلاق الاتصال (اختياري، قد لا تكون ضرورية في بيئات الـ Lambda/Webhooks)
def close_mongo_db_client():
    """
    إغلاق اتصال MongoDB إذا كان مفتوحاً.
    """
    global _mongo_client, _db
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _db = None
        print("🔌 تم إغلاق اتصال MongoDB.")
