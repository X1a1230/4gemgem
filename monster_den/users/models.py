from monster_den import db, login_manager
from flask_login import UserMixin

# login_manager 需要一個 user_loader 函式來知道如何從 ID 找到使用者
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User 模型，繼承了 db.Model (資料庫模型) 和 UserMixin (Flask-Login 的使用者特性)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # 使用者名稱，必須是獨一無二的
    username = db.Column(db.String(20), unique=True, nullable=False)
    # 密碼欄位，我們只儲存雜湊後的密碼，長度設為 60
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"