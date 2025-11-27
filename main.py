import os
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
)
# استيراد معالج الرسائل الجديد (handle_message) ومعالج الـ Callback (handle_callback_query)
from handlers import start, handle_message, handle_callback_query, notify_update_to_users, notify_update_command, handle_notify_update_activation
from keep_alive import keep_alive
import asyncio
import nest_asyncio

TOKEN = os.getenv("TOKEN")

async def main():
    if not TOKEN:
        print("FATAL: TOKEN environment variable is not set.")
        return
        
    application = ApplicationBuilder().token(TOKEN).build()

    # إضافة أوامر البوت
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("notify", notify_update_command)) # أمر الإشعار للمشرف

    # إضافة معالج الرسائل النصية
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
    # إضافة معالج الـ Callback Queries لأزرار Inline (مثل جداول الامتحانات)
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # تعيين قائمة الأوامر المتاحة
    commands = [
        ("start", "🚀 بدء استخدام البوت والعودة للقائمة الرئيسية")
    ]
    await application.bot.set_my_commands(commands)

    print("Bot started and handlers are set...")
    await application.run_polling()


if __name__ == "__main__":
    # تشغيل keep_alive لضمان استمرارية عمل البوت
    check_secrets()
    keep_alive()

    # تطبيق nest_asyncio للسماح بتشغيل asyncio.run داخل بيئات غير اعتيادية (مثل Jupyter/Colab)
    nest_asyncio.apply()

    asyncio.run(main())


def check_secrets():
    token = os.getenv("TOKEN")
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME")

    if not token:
        print("⚠️ TOKEN is not set in secrets.")
    else:
        print("✅ TOKEN is set.")

    if not mongo_uri:
        print("⚠️ MONGO_URI is not set in secrets.")
    else:
        print("✅ MONGO_URI is set.")

    if not mongo_db_name:
        print(
            "⚠️ MONGO_DB_NAME is not set in secrets, using default value: telegram_bot_db"
        )
    
