from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class GuestbookForm(FlaskForm):
    """訪客留言的表單"""
    author = StringField('你的名字 (可選)', validators=[Optional(), Length(max=100)])
    message = TextAreaField('想說的話', validators=[DataRequired()])
    # 讓訪客可以選擇一個心情符號！
    mood_icon = SelectField('今日心情',
                            choices=[('🐾', '🐾 小腳印'),
                                     ('❤️', '❤️ 溫暖'),
                                     ('✨', '✨ 閃亮'),
                                     ('🌙', '🌙 靜謐'),
                                     ('😊', '😊 開心'),
                                     ('🤭', '🤭 什麽互聯網老機')],
                            validators=[DataRequired()])
    submit = SubmitField('留下印記')
