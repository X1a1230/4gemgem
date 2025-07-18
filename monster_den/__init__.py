from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig # 導入我們寫好的設定
from markupsafe import Markup # 導入 Markup，這是製作安全HTML的魔法材料
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# --- 這是我們新增的「魔法卷軸」定義 ---
# 我們定義一個叫做 nl2br 的函式
def nl2br(value):
    # 它會接收一個字串，把裡面的換行符號(\n)替換成HTML的換行標籤(<br>)
    # Markup() 會告訴系統，這段HTML是安全的，請直接顯示
    return Markup(value.replace('\n', '<br>\n'))

# 1. 我們先在這裡建立一個 db 物件，但還不將它綁定到任何 app
#    這讓我們的藍圖和模型可以安全地導入它
db = SQLAlchemy()
# 初始化密碼保鑣
bcrypt = Bcrypt()
# 初始化登入管家
login_manager = LoginManager()
# 設定登入頁面的端點 (endpoint)
login_manager.login_view = 'users.login'
# 設定需要登入時的提示訊息
login_manager.login_message = '你需要先登入才能訪問這個頁面。'
login_manager.login_message_category = 'info'

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
    bcrypt.init_app(app)
    login_manager.init_app(app)

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

    from monster_den.users.routes import users_bp
    app.register_blueprint(users_bp)

    from monster_den.guestbook.routes import guestbook_bp
    app.register_blueprint(guestbook_bp)

    from monster_den.mailbox.routes import mailbox_bp
    app.register_blueprint(mailbox_bp)

    from monster_den.garden.routes import garden_bp
    app.register_blueprint(garden_bp)

    return app
