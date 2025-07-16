from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig # 導入我們寫好的設定
from markupsafe import Markup # 導入 Markup，這是製作安全HTML的魔法材料

# --- 這是我們新增的「魔法卷軸」定義 ---
# 我們定義一個叫做 nl2br 的函式
def nl2br(value):
    # 它會接收一個字串，把裡面的換行符號(\n)替換成HTML的換行標籤(<br>)
    # Markup() 會告訴系統，這段HTML是安全的，請直接顯示
    return Markup(value.replace('\n', '<br>\n'))

# 1. 我們先在這裡建立一個 db 物件，但還不將它綁定到任何 app
#    這讓我們的藍圖和模型可以安全地導入它
db = SQLAlchemy()

def create_app():
    """應用程式工廠函式"""
    app = Flask(__name__, template_folder='templates')

    # 2. 從我們的設定檔載入所有設定
    app.config.from_object(DevelopmentConfig)

    # 關鍵！從我們的設定檔裡，為 app 設定一個 SECRET_KEY
    # 如果沒有這把「鎖」，session 魔法就無法啟動
    app.config['SECRET_KEY'] = DevelopmentConfig.SECRET_KEY

    # 3. 將 db 物件與我們的 app 綁定
    db.init_app(app)

    # --- 將我們的魔法卷軸，正式登錄到魔法書裡 ---
    app.jinja_env.filters['nl2br'] = nl2br

    # --- 註冊我們的房間 (藍圖) ---
    from .Menu.routes import menu_bp
    app.register_blueprint(menu_bp, url_prefix='/menu')

    from .main.routes import main_bp
    app.register_blueprint(main_bp)

    # 新增這一行來註冊我們的工匠坊
    from .workshop.routes import workshop_bp
    app.register_blueprint(workshop_bp, url_prefix='/workshop')

    from .memory.routes import memory_bp
    app.register_blueprint(memory_bp, url_prefix='/memory')

    return app
