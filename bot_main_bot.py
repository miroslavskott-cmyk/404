import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# --- استدعاء ملفاتك الخاصة (Imports) ---
try:
    from config_settings import BOT_TOKEN, OWNER_ID, OWNER_KEY, generate_vip_key
    from database_db_handler import DBHandler
    from ai_engine_analyzer import FootballAIPro
except ImportError as e:
    print(f"❌ خطأ في الاستدعاء: تأكد من وجود جميع الملفات في نفس المجلد!\n{e}")
    exit()

# إعداد اللوغ (Logging) لمراقبة الأخطاء
logging.basicConfig(level=logging.INFO)

# تهيئة البوت والمحركات
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = DBHandler() # يتصل بـ database/users.db تلقائياً
ai = FootballAIPro()

# رابط الـ Web App (يجب تغييره بعد الرفع أو باستخدام LocalTunnel)
WEBAPP_URL = "https://your-app-url.com" 

# --- الأوامر البرمجية ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    # رسالة ترحيبية تدعم اللغات
    text = (
        "⚽ **AI Football Match Analyst**\n\n"
        "مرحباً بك في أقوى بوت تحليل مباريات بالذكاء الاصطناعي.\n"
        "Welcome to the most powerful AI Match Analyst.\n"
        "Bienvenue dans le meilleur analyste de foot IA.\n\n"
        "--- 💎 VIP Status ---\n"
    )
    
    if db.check_vip(user_id) or str(user_id) == str(OWNER_ID):
        status = "✅ حسابك مفعل (VIP Active)"
    else:
        status = "❌ حساب مجاني (Free Account)\nاستخدم /trial للتجربة أو /buy للاشتراك."

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="فتح التطبيق 📊 Open App", web_app=WebAppInfo(url=f"{WEBAPP_URL}?user={user_id}"))],
        [InlineKeyboardButton(text="شراء اشتراك 💳 Buy VIP", callback_data="buy_vip")]
    ])
    
    await message.answer(text + status, reply_markup=kb, parse_mode="Markdown")

@dp.message(Command("activate"))
async def cmd_activate(message: types.Message):
    # أمر تفعيل المفاتيح: /activate AI-XXXX-XXXX
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("⚠️ يرجى إدخال المفتاح بعد الأمر. مثال:\n`/activate AI-1234-5678`", parse_mode="Markdown")
    
    key = args[1]
    user_id = message.from_user.id

    # التحقق من مفتاح المالك
    if key == OWNER_KEY:
        db.conn.execute("INSERT OR REPLACE INTO users (user_id, expiry, is_vip) VALUES (?, ?, ?)", 
                        (user_id, time.time() + (365*86400), True))
        db.conn.commit()
        return await message.answer("👑 تم تفعيل صلاحيات المالك بنجاح!")

    # التحقق من مفاتيح VIP العشوائية في قاعدة البيانات
    cursor = db.conn.cursor()
    cursor.execute("SELECT duration_days FROM keys WHERE key_id=?", (key,))
    result = cursor.fetchone()

    if result:
        duration = result[0]
        expiry_time = time.time() + (duration * 86400)
        db.conn.execute("INSERT OR REPLACE INTO users (user_id, expiry, is_vip) VALUES (?, ?, ?)", 
                        (user_id, expiry_time, True))
        db.conn.execute("DELETE FROM keys WHERE key_id=?", (key,)) # حذف المفتاح بعد الاستخدام
        db.conn.commit()
        await message.answer(f"✅ تم التفعيل بنجاح لمدة {duration} أيام!")
    else:
        await message.answer("❌ المفتاح غير صحيح أو تم استخدامه مسبقاً.")

@dp.message(Command("gen_key"))
async def cmd_gen_key(message: types.Message):
    # للمالك فقط: لتوليد مفاتيح جديدة للبيع
    if str(message.from_user.id) != str(OWNER_ID):
        return

    new_key = generate_vip_key()
    db.conn.execute("INSERT INTO keys (key_id, duration_days) VALUES (?, ?)", (new_key, 7))
    db.conn.commit()
    await message.answer(f"🔑 مفتاح VIP جديد (7 أيام):\n`{new_key}`", parse_mode="Markdown")

# --- تشغيل البوت ---
async def main():
    print("🚀 البوت يعمل الآن ويراقب قاعدة البيانات...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 تم إيقاف البوت.")
