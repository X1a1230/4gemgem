from monster_den import db

class EasterEgg(db.Model):
    """每一個彩蛋（寶藏）的設計圖"""
    id = db.Column(db.Integer, primary_key=True)
    # 我們給每個彩蛋起個名字，方便我們自己辨認
    name = db.Column(db.String(100), nullable=False)
    # 這是寫在藏寶圖上的「謎語」或「詩意的提示」
    riddle = db.Column(db.Text, nullable=False)
    # 我們可以留一個欄位，給那些實在找不到的偵探一點點小提示
    hint = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"EasterEgg('{self.name}')"