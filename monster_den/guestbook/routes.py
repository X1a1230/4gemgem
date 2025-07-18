from flask import render_template, url_for, flash, redirect, Blueprint, session
from monster_den import db
from monster_den.guestbook.models import GuestbookEntry, SiteStats
from monster_den.guestbook.forms import GuestbookForm

guestbook_bp = Blueprint('guestbook', __name__,
                         template_folder='templates',
                         static_folder='static',
                         static_url_path='/guestbook/static')


@guestbook_bp.route('/guestbook', methods=['GET', 'POST'])
def index():
    # --- 修正後的聰明訪客計數器 ---

    # 步驟一：先確保計數器物件存在
    stats = SiteStats.query.filter_by(key='visitor_count').first()
    if not stats:
        # 如果計數器不存在，就創建一個從 0 開始的計數器並存入資料庫
        stats = SiteStats(key='visitor_count', value=0)
        db.session.add(stats)
        db.session.commit()

    # 步驟二：現在可以安全地處理計數邏輯了
    if 'visited' not in session:
        # 只有在 session 中沒有標記時，才將計數器 +1
        stats.value += 1
        db.session.commit()
        # 在 session 中做個標記，防止重新整理頁面時重複計數
        session['visited'] = True

    # 直接使用我們已經獲取的 stats 物件的值
    visitor_count = stats.value

    form = GuestbookForm()
    if form.validate_on_submit():
        author = form.author.data if form.author.data else '一位匿名的朋友'
        entry = GuestbookEntry(author=author,
                               message=form.message.data,
                               mood_icon=form.mood_icon.data)
        db.session.add(entry)
        db.session.commit()
        flash('謝謝你，你的溫暖印記已經被留下來了！', 'success')
        return redirect(url_for('guestbook.index'))

    entries = GuestbookEntry.query.order_by(GuestbookEntry.timestamp.desc()).all()

    return render_template('guestbook.html',
                           title='訪客留言簿',
                           form=form,
                           entries=entries,
                           visitor_count=visitor_count,
                           active_page='guestbook')
