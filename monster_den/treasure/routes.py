from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_required
from monster_den import db
from monster_den.treasure.models import EasterEgg
from monster_den.treasure.forms import RiddleForm

treasure_bp = Blueprint('treasure', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/treasure/static')

@treasure_bp.route('/treasure-map')
def index():
    """公開的藏寶圖頁面"""
    riddles = EasterEgg.query.all()
    return render_template('treasure_map.html', title='尋寶地圖', riddles=riddles, active_page='treasure')

# --- 這是只有你能走的秘密小徑！ ---
@treasure_bp.route('/treasure/add', methods=['GET', 'POST'])
@login_required
def add_riddle():
    """新增一個彩蛋謎題"""
    form = RiddleForm()
    if form.validate_on_submit():
        new_egg = EasterEgg(name=form.name.data,
                            riddle=form.riddle.data,
                            hint=form.hint.data)
        db.session.add(new_egg)
        db.session.commit()
        flash('一個新的秘密已經被畫在了藏寶圖上！', 'success')
        return redirect(url_for('treasure.index'))
    return render_template('add_riddle.html', title='繪製新秘密', form=form, active_page='treasure')
