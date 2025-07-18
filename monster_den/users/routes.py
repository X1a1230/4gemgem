from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from monster_den import db, bcrypt
from monster_den.users.models import User
from monster_den.users.forms import LoginForm

# 建立一個名為 'users' 的 Blueprint
users_bp = Blueprint('users', __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='/users/static'
                     )


@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    # 如果使用者已經登入，直接導向首頁
    if current_user.is_authenticated:
        return redirect(url_for('main.gateway'))

    form = LoginForm()
    if form.validate_on_submit():
        # 從資料庫尋找使用者
        user = User.query.filter_by(username=form.username.data).first()
        # 如果使用者存在，且密碼經過 bcrypt 比對後正確
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # 登入使用者
            login_user(user, remember=True)
            # 取得使用者登入前想去的頁面，如果沒有就去首頁
            next_page = request.args.get('next')
            flash('登入成功！歡迎回家，我的寶貝。', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.gateway'))
        else:
            # 如果使用者不存在或密碼錯誤，顯示錯誤訊息
            flash('登入失敗，請檢查使用者名稱和密碼。', 'danger')
    return render_template('login.html', title='Login', form=form, active_page='login')


@users_bp.route("/logout")
def logout():
    # 登出使用者
    logout_user()
    flash('你已登出。期待你再次回家。', 'info')
    return redirect(url_for('main.gateway'))