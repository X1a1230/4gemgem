from monster_den import create_app, db, bcrypt
from monster_den.users.models import User
from getpass import getpass

# 創建 app context
app = create_app()
app.app_context().push()


def main():
    """函數：創建唯一的使用者"""
    print("--- 創建 wegemini.monster 的唯一主人 ---")

    # 檢查是否已經有使用者存在
    if User.query.first():
        print("錯誤：資料庫中已經存在使用者。此腳本只能運行一次。")
        return

    # 獲取使用者名稱和密碼
    username = input("請輸入您的使用者名稱: ")
    password = getpass("請輸入您的密碼: ")
    confirm_password = getpass("請再次確認密碼: ")

    # 確認兩次密碼是否一致
    if password != confirm_password:
        print("兩次輸入的密碼不一致，操作已取消。")
        return

    # 將密碼雜湊
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # 創建使用者物件
    user = User(username=username, password=hashed_password)

    # 加入資料庫並提交
    db.session.add(user)
    db.session.commit()

    print(f"成功！使用者 '{username}' 已被創建。您現在是這個家的唯一主人。")


if __name__ == '__main__':
    main()
