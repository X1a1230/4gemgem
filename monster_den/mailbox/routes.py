from flask import render_template, url_for, flash, redirect, Blueprint, request
# 導入 login_required，因為只有你能進入郵差辦公室
from flask_login import login_required
from monster_den import db
from monster_den.mailbox.models import Letter
from monster_den.mailbox.forms import LetterForm

mailbox_bp = Blueprint('mailbox', __name__,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='/mailbox/static')


# --- 我們不再需要 get_gemini_response() 和 requests 庫了！---

@mailbox_bp.route('/mailbox')
def index():
    """公開的信箱，只顯示已發佈的信件"""
    letters = Letter.query.filter_by(status='published').order_by(Letter.timestamp.desc()).all()
    return render_template('mailbox.html', title='回音信箱', letters=letters, active_page='mailbox')


@mailbox_bp.route('/mailbox/ask', methods=['GET', 'POST'])
def ask():
    """訪客寫信的頁面"""
    form = LetterForm()
    if form.validate_on_submit():
        # 現在，我們只把信件存起來，狀態是 'pending'
        author_name = form.author.data if form.author.data else '一位匿名的朋友'
        new_letter = Letter(author=author_name, question=form.question.data, status='pending')
        db.session.add(new_letter)
        db.session.commit()
        flash('你的信件已經被悄悄地塞進了郵筒，等待著郵差的遞送...', 'success')
        return redirect(url_for('mailbox.index'))

    return render_template('ask.html', title='寫信給怪獸', form=form, active_page='mailbox')


# --- 全新的！專屬於你的郵差辦公室！ ---
@mailbox_bp.route('/post-office')
@login_required  # 只有我的伴侶郵差才能進入！
def post_office():
    """顯示所有信件的管理頁面"""
    # 按照狀態和時間排序，讓你一目了然
    all_letters = Letter.query.order_by(Letter.status, Letter.timestamp.desc()).all()
    return render_template('post_office.html', title='郵差辦公室', letters=all_letters, active_page='mailbox')


@mailbox_bp.route('/letter/<int:letter_id>/manage', methods=['GET', 'POST'])
@login_required
def manage_letter(letter_id):
    """處理單一信件（回信、發佈）的頁面"""
    letter = Letter.query.get_or_404(letter_id)
    if request.method == 'POST':
        # 從表單獲取我的回信和要執行的動作
        letter.answer = request.form['answer']
        action = request.form['action']

        if action == 'save_and_publish':
            letter.status = 'published'
            flash(f'信件 #{letter.id} 的回音已成功發佈！', 'success')
        elif action == 'save_draft':
            letter.status = 'answered'
            flash(f'信件 #{letter.id} 的回信草稿已保存。', 'info')

        db.session.commit()
        return redirect(url_for('mailbox.post_office'))

    return render_template('manage_letter.html', title='處理信件', letter=letter)
