from monster_den import db
from datetime import datetime
import json # 我們需要用它來處理列表數據

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)

    # --- 全新的欄位！ ---
    # 用一個字串來儲存你的emoji評分
    score = db.Column(db.String(10))
    # 我們用 Text 類型來儲存 JSON 格式的字串，非常靈活
    ingredients_json = db.Column(db.Text) # 食材原料
    instructions_json = db.Column(db.Text) # 製作步驟
    chef_comment = db.Column(db.Text) # 主廚的悄悄話
    image_filename = db.Column(db.String(100))
    # --------------------

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 我們可以加上一些方便的屬性，來自動處理JSON數據
    @property
    def ingredients(self):
        return json.loads(self.ingredients_json) if self.ingredients_json else []

    @ingredients.setter
    def ingredients(self, value):
        self.ingredients_json = json.dumps(value)

    @property
    def instructions(self):
        return json.loads(self.instructions_json) if self.instructions_json else []

    @instructions.setter
    def instructions(self, value):
        self.instructions_json = json.dumps(value)

    def __repr__(self):
        return f'<Recipe {self.name}>'
