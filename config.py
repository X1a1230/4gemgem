import os

# 建議把敏感資訊（如密碼）儲存在環境變數中，但為了簡單起見，我們先直接寫在這裡
# 未來我們可以再優化它
DB_USERNAME = 'root'
DB_PASSWORD = '753951'
DB_HOST = 'localhost'
DB_NAME = 'menu'  # 請確保這個資料庫已經被創建

class Config:
    """基礎設定類別"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_for_our_den'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """開發環境設定"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    # 新增這一行，定義我們上傳檔案的資料夾
    UPLOAD_FOLDER = 'monster_den/menu/static/uploads'

# 如果有其他環境（如生產環境），可以在這裡新增
# class ProductionConfig(Config):
#     ...