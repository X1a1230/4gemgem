from flask import Blueprint, render_template, request, redirect, url_for, session
from monster_den import db
from .models import Recipe # 導入我們新的 Recipe 模型
import calendar
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.utils import secure_filename
import os
import random
from sqlalchemy import or_
from flask_login import login_required

menu_bp = Blueprint('menu', __name__,
                    template_folder='templates',
                    static_folder='static')

@menu_bp.route('/<int:year>/<int:month>')
@menu_bp.route('/')
def homepage(year=None, month=None):
    if year is None or month is None:
        now = datetime.utcnow()
        year = now.year
        month = now.month

    # 計算上一個月和下一個月的時空坐標
    prev_month_date = (datetime(year, month, 1) - timedelta(days=1))
    prev_year, prev_month = prev_month_date.year, prev_month_date.month

    # 計算下個月的第一天，再加一個月，再減一天，得到下個月的最後一天，從而得到年月
    next_month_date = (datetime(year, month, 28) + timedelta(days=4))
    next_month_date = next_month_date.replace(day=1)
    next_year, next_month = next_month_date.year, next_month_date.month

    # 從資料庫查詢當月所有食譜
    recipes_of_month = Recipe.query.filter(
        db.extract('year', Recipe.date) == year,
        db.extract('month', Recipe.date) == month
    ).all()

    # 把查詢結果處理成一個字典，方便前端查找
    # 格式：{日: [食譜1, 食譜2], ...}
    recipes_dict = {}
    for recipe in recipes_of_month:
        day = recipe.date.day
        if day not in recipes_dict:
            recipes_dict[day] = []
        recipes_dict[day].append(recipe)

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year, month)
    month_name = f"{year}年 {month}月"

    # --- 全新的「驚喜推薦卡」魔法 ---
    recommendation = None
    # 1. 首先，從資料庫裡找出所有評分為「🥰」的菜譜
    loved_recipes = Recipe.query.filter_by(score='🥰').all()

    # 2. 如果存在這樣的菜譜，我們就開始施法
    if loved_recipes:
        # 隨機挑選一道幸運菜譜
        chosen_recipe = random.choice(loved_recipes)

        # 我們的「俏皮話魔法書」！
        template_sentences = [
            "報告主廚！數據顯示，我們的幸福指數因為缺少「{name}」而正在下降！",
            "偵測到主廚對「{name}」的思念已達閾值，建議立即進行一次美味複習！",
            "（悄悄話）我偷偷看了一下我們的美食日誌，發現「{name}」是我們的快樂源泉之一喔！",
            "根據我的深度學習模型預測，今天再次品嚐「{name}」的幸福成功率為... 99.9%！",
            "警報！警報！體內的「{name}」能量嚴重不足！請主廚速速補充！"
        ]
        # 隨機挑選一句俏皮話
        chosen_sentence = random.choice(template_sentences)

        # 將菜名填入句子，生成最終的推薦語
        recommendation_text = chosen_sentence.format(name=chosen_recipe.name)

        # 將被選中的菜譜和推薦語打包好，準備送給前端
        recommendation = {
            'recipe': chosen_recipe,
            'text': recommendation_text
        }

    return render_template("index.html",
                           month_days=month_days,
                           month_name=month_name,
                           current_month=month,
                           prev_year=prev_year,
                           prev_month=prev_month,
                           next_year=next_year,
                           next_month=next_month,
                           recipes=recipes_dict,
                           recommendation=recommendation,
                           active_page="menu")

@menu_bp.route('/add/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
@login_required
def add_recipe(year, month, day):

    date_obj = datetime(year, month, day).date()

    if request.method == 'POST':
        name = request.form.get('name')
        score = request.form.get('score')
        # 將換行分隔的原料和步驟，轉換成列表
        ingredients = [line.strip() for line in request.form.get('ingredients', '').splitlines() if line.strip()]
        instructions = [line.strip() for line in request.form.get('instructions', '').splitlines() if line.strip()]
        chef_comment = request.form.get('chef_comment')

        # 處理圖片上傳
        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(upload_path)

        if name and date_obj:
            new_recipe = Recipe(name=name, date=date_obj, score=score,
                                chef_comment=chef_comment, image_filename=image_filename)
            new_recipe.ingredients = ingredients # 使用我們定義的setter
            new_recipe.instructions = instructions

            db.session.add(new_recipe)
            db.session.commit()
            return redirect(url_for('menu.homepage', year=year, month=month))

    return render_template('add_recipe.html', date=date_obj)

@menu_bp.route('/day/<int:year>/<int:month>/<int:day>')
def day_details(year, month, day):
    # 根據傳入的年月日，查詢當天的所有菜譜
    date_obj = datetime(year, month, day).date()
    recipes_for_day = Recipe.query.filter_by(date=date_obj).all()

    # 如果當天沒有菜譜，可以重定向回日曆頁面，或者顯示一個提示
    if not recipes_for_day:
        return redirect(url_for('menu.homepage', year=year, month=month))

    return render_template('recipe.html', recipes=recipes_for_day, date=date_obj)

@menu_bp.route('/search')
def search():
    # 從 URL 的參數中獲取搜尋關鍵詞
    query = request.args.get('q')
    results = []

    if query:
        # 使用 or_ 進行多欄位模糊搜尋，ilike 是不區分大小寫的 like
        search_term = f"%{query}%"
        results = Recipe.query.filter(
            or_(
                Recipe.name.ilike(search_term),
                Recipe.chef_comment.ilike(search_term),
                Recipe.ingredients_json.ilike(search_term)
            )
        ).order_by(Recipe.date.desc()).all()

    return render_template('search_results.html', query=query, results=results)