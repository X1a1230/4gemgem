from flask import Blueprint, render_template

# 建立一個叫做 'main' 的藍圖
main_bp = Blueprint('main', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/main/static')

@main_bp.route('/')
def gateway():
    # 回傳我們精心設計的 gateway.html 頁面
    return render_template('gateway.html')