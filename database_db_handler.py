 import sqlite3
import time

class DBHandler:
    def __init__(self, db_path="database/users.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # جدول المستخدمين، تاريخ الانتهاء، وحالة الـ VIP
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (user_id INTEGER PRIMARY KEY, expiry TIMESTAMP, is_vip BOOLEAN)''')
        # جدول مفاتيح التفعيل
        cursor.execute('''CREATE TABLE IF NOT EXISTS keys 
                          (key_id TEXT PRIMARY KEY, duration_days INTEGER)''')
        self.conn.commit()

    def check_vip(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT expiry FROM users WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res and res[0] > time.time():
            return True
        return False
