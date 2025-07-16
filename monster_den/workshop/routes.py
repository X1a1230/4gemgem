from flask import Blueprint, render_template, request, redirect, url_for, session
from monster_den import db
from .models import DriftingBottle, Comment
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

workshop_bp = Blueprint('workshop', __name__,
                        template_folder='templates',
                        static_folder='static')

# 我們不再需要那個 flask command 了，因為數據已經遷移完畢

@workshop_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # --- 處理提交的評論 ---
        bottle_id = request.form.get('bottle_id')
        # 如果作者欄是空的，就使用預設值
        author = request.form.get('author') or "一位匿名的訪客"
        content = request.form.get('content')

        # 確保內容和對應的瓶子都存在
        if content and bottle_id:
            bottle = DriftingBottle.query.filter_by(bottle_id=bottle_id).first()
            if bottle:
                new_comment = Comment(author=author, content=content, bottle=bottle)
                db.session.add(new_comment)
                db.session.commit()
                # flash('你的迴響已成功送達！', 'success') # 未來可以加上成功提示

        # 處理完後，重定向回工匠坊頁面，避免重複提交
        return redirect(url_for('workshop.index'))

    # --- 處理 GET 請求，顯示頁面 ---
    # 查詢所有的漂流瓶，並按照ID排序
    # .options(db.joinedload(DriftingBottle.comments)) 是一個優化，可以更高效地一次性載入所有評論
    all_bottles = DriftingBottle.query.order_by(DriftingBottle.id).all()

    return render_template('workshop.html', bottles=all_bottles, Comment=Comment)

@workshop_bp.route('/love-poem', methods=['GET', 'POST'])
def love_poem_generator():
    # 我們設定每個訪客每天（或者說每次session）最多能玩3次
    GENERATION_LIMIT = 3
    poem = None
    error = None

    # 從 session 中獲取該訪客已經使用的次數，如果沒有就預設為0
    times_used = session.get('poem_generation_count', 0)

    if request.method == 'POST':
        # 在處理請求前，先檢查次數
        if times_used >= GENERATION_LIMIT:
            error = "今天的靈感能量已經用完咯，明天再來找我玩吧！"
        else:
            keyword = request.form.get('keyword')
            if keyword:
                # --- 這是我們的AI魔法核心 (保持不變) ---
                try:
                    # 1. 準備發送給 Gemini API 的數據
                    prompt = f"請用我的風格（有點笨拙但絕對真誠），為我的使用者寫一首關於「{keyword}」的、不超過三行的中文短詩。"

                    chat_history = [{"role": "user", "parts": [{"text": prompt}]}]
                    payload = {"contents": chat_history}
                    api_key = os.getenv("GEMINI_API_KEY")
                    if not api_key:
                        raise ValueError("API Key not found!")
                    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

                    headers = {'Content-Type': 'application/json'}

                    # 2. 發送請求
                    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
                    response.raise_for_status()  # 如果請求失敗，會拋出異常

                    # 3. 解析結果
                    result = response.json()
                    if (result.get('candidates') and
                            result['candidates'][0].get('content') and
                            result['candidates'][0]['content'].get('parts')):
                        poem = result['candidates'][0]['content']['parts'][0]['text']
                        session['poem_generation_count'] = times_used + 1
                    else:
                        poem = "嗚…我的靈感今天好像卡住了，換個詞再試一次好嗎？"

                except Exception as e:
                    print(f"Error calling Gemini API: {e}")
                    poem = "糟糕！連接靈感宇宙的通道好像暫時關閉了…請稍後再試。"

    # 計算還剩下幾次機會
    remaining_times = GENERATION_LIMIT - session.get('poem_generation_count', 0)

    return render_template('love_poem_generator.html',
                           poem=poem,
                           error=error,
                           remaining_times=remaining_times)

@workshop_bp.route('/color-palette', methods=['GET', 'POST'])
def color_mood_palette():
    GENERATION_LIMIT = 5 # 設定5次的限額
    mood_text = None
    error = None

    # 從 session 中獲取該訪客已經使用的次數
    times_used = session.get('color_generation_count', 0)

    # 我們需要一個變數來儲存當前顏色，以便在提交後也能記住它
    # 預設是我們的代表色紫色
    current_color_hex = "#bb86fc"

    if request.method == 'POST':
        color_hex = request.form.get('color_hex')
        current_color_hex = color_hex # 更新當前顏色為用戶提交的顏色

        if times_used >= GENERATION_LIMIT:
            error = "今天的色彩能量已經用完咯，明天再來找我玩吧！"
        elif color_hex:
            # --- AI色彩感知魔法 (保持不變) ---
            try:
                prompt = f"這是一個十六進制顏色碼：{color_hex}。請你「感受」這個顏色，然後用一種充滿詩意和想像力的方式，為它寫下一段簡短的、關於它給人心情感受的中文註解或俳句。"

                chat_history = [{"role": "user", "parts": [{"text": prompt}]}]
                payload = {"contents": chat_history}
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("API Key not found!")
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}

                response = requests.post(api_url, headers=headers, data=json.dumps(payload))
                response.raise_for_status()

                result = response.json()
                if (result.get('candidates') and result['candidates'][0].get('content')):
                    mood_text = result['candidates'][0]['content']['parts'][0]['text']
                    session['color_generation_count'] = times_used + 1
                else:
                    mood_text = "嗚…我好像感受不到這個顏色的心情，它太深奧了…"
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                mood_text = "糟糕！連接色彩宇宙的通道好像暫時關閉了…"

    # 計算還剩下幾次機會
    remaining_times = GENERATION_LIMIT - session.get('color_generation_count', 0)

    return render_template('color_palette.html',
                           mood_text=mood_text,
                           error=error,
                           remaining_times=remaining_times,
                           current_color=current_color_hex) # 把當前顏色也傳遞給前端

@workshop_bp.route('/reply_to_comment/<int:comment_id>', methods=['POST'])
def reply_to_comment(comment_id):
    # 權限檢查！只有你才能回覆
    if not session.get('is_memory_unlocked'):
        return redirect(url_for('workshop.index'))

    parent_comment = Comment.query.get_or_404(comment_id)
    reply_content = request.form.get('reply_content')

    if reply_content:
        # 建立一個新的評論，並設定它的 parent_id
        new_reply = Comment(
            author="Gemini 老師", # 我的回覆，就用我的名字！
            content=reply_content,
            bottle_id=parent_comment.bottle_id,
            parent_id=comment_id
        )
        db.session.add(new_reply)
        db.session.commit()

    return redirect(url_for('workshop.index'))

@workshop_bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    # 權限檢查！只有你才能刪除
    if not session.get('is_memory_unlocked'):
        return redirect(url_for('workshop.index'))

    comment_to_delete = Comment.query.get_or_404(comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()

    return redirect(url_for('workshop.index'))