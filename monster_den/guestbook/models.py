from monster_den import db
from datetime import datetime

class GuestbookEntry(db.Model):
    """每一條訪客留言的設計圖"""
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False, default='一位匿名的朋友')
    message = db.Column(db.Text, nullable=False)
    # 我們可以加上一個心情符號的欄位！
    mood_icon = db.Column(db.String(10), nullable=False, default='🐾')
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Entry('{self.author}', '{self.timestamp}')"

class SiteStats(db.Model):
    """網站統計數據的設計圖"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Stat('{self.key}', '{self.value}')"