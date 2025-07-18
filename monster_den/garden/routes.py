from flask import render_template, url_for, flash, redirect, Blueprint, jsonify
from flask_login import login_required
from monster_den import db
from monster_den.garden.models import Flower

garden_bp = Blueprint('garden', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/garden/static')


@garden_bp.route('/garden')
def index():
    """顯示螢光花園"""
    flowers = Flower.query.all()
    return render_template('garden.html', title='螢光花園', flowers=flowers, active_page='garden')


@garden_bp.route('/garden/water/<int:flower_id>', methods=['POST'])
def water_flower(flower_id):
    """處理澆水動作的 API 端點"""
    flower = Flower.query.get_or_404(flower_id)
    if flower.status == 'bud':
        flower.status = 'bloomed'

    flower.times_watered += 1
    # --- 我們的彩蛋觸發器！ ---
    # 為了方便測試，我們先把觸發條件設為 10 次
    # 未來我們可以把它改成 99 次，或者任何我們喜歡的數字！
    if flower.times_watered >= 10 and not flower.special_status:
        flower.special_status = 'rare'

    db.session.commit()
    # 在回傳的 JSON 裡，加上我們新的彩蛋狀態！
    return jsonify({
        'success': True,
        'status': flower.status,
        'times_watered': flower.times_watered,
        'special_status': flower.special_status
    })


@garden_bp.route('/garden/plant', methods=['POST'])
@login_required  # 只有我的園丁伴侶才能播種！
def plant_new_buds():
    """處理播種動作"""
    # 每次種下 5 顆新的花苞
    for _ in range(5):
        Flower.plant_new_bud()
    flash('新的花苞已經在花園的土壤裡悄悄發芽了。', 'success')
    return redirect(url_for('garden.index'))