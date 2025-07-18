from monster_den import db
from datetime import datetime

class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False, default='一位匿名的朋友')
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True)  # 我的回信，由你填上
    # 'pending': 等待你審閱, 'answered': 我已回信但未發佈, 'published': 已發佈
    status = db.Column(db.String(20), nullable=False, default='pending')
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Letter from {self.author} - Status: {self.status}"