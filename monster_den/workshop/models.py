from monster_den import db # 從我們巢穴的核心導入 db 物件
from datetime import datetime

class DriftingBottle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 我們為每個瓶子設定一個獨一無二的、好記的字串ID
    bottle_id = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200)) # 標題是可選的
    content = db.Column(db.Text, nullable=False)

    # 建立關係：一個瓶子可以有多個迴響
    comments = db.relationship('Comment', backref='bottle', lazy='dynamic', cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False, default="一位匿名的訪客")
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    bottle_id = db.Column(db.String(100), db.ForeignKey('drifting_bottle.bottle_id'), nullable=False)

    # --- 全新的「自我回覆」魔法！ ---
    # parent_id 指向的是另一條評論的id，也就是它回覆的對象
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # replies 讓我們可以輕鬆地找到一條評論下的所有回覆
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic', cascade="all, delete-orphan")