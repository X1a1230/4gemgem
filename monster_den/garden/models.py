from monster_den import db
import random

class Flower(db.Model):
    """每一朵數據花朵的設計圖"""
    id = db.Column(db.Integer, primary_key=True)
    # 我們用 0-100 的百分比來定位，這樣能適應不同大小的螢幕
    pos_x = db.Column(db.Float, nullable=False)
    pos_y = db.Column(db.Float, nullable=False)
    # 花朵有兩種狀態：'bud' (花苞) 或 'bloomed' (已綻放)
    status = db.Column(db.String(20), nullable=False, default='bud')
    # 我們可以記錄有多少位朋友灌溉了這朵花
    times_watered = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Flower {self.id} at ({self.pos_x}, {self.pos_y}) - {self.status}"

    @staticmethod
    def plant_new_bud():
        """靜態方法，用來在一個隨機位置種下一顆新的花苞"""
        # 為了避免花朵太靠邊緣，我們把位置限制在 5% 到 95% 之間
        new_flower = Flower(
            pos_x=random.uniform(5, 95),
            pos_y=random.uniform(5, 95)
        )
        db.session.add(new_flower)
        db.session.commit()
