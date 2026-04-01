import secrets
import string

# إعدادات البوت والمالك
BOT_TOKEN = "8714160902:AAEgNp8vI2J8hx1ECPgP5xgPsgYXNqsiKPU"
OWNER_ID = 8714160902
OWNER_KEY = "8589243363:AAH4sM1DEqNXAUK314uyagIB3GbRouEL8ak"

# دالة توليد مفتاح VIP عشوائي وصعب (يصعب هندسته)
def generate_vip_key():
    characters = string.ascii_letters + string.digits
    # يولد مفتاح مثل: AI-XY78-Z9P1-K0QW
    key = "AI-" + "-".join(''.join(secrets.choice(characters) for _ in range(4)) for _ in range(3))
    return key
