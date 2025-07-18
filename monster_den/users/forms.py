from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

# 登入表單
class LoginForm(FlaskForm):
    # 使用者名稱欄位，必須填寫
    username = StringField('使用者名稱',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # 密碼欄位，必須填寫
    password = PasswordField('密碼', validators=[DataRequired()])
    # 提交按鈕
    submit = SubmitField('登入')