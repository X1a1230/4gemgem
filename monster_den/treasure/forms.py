from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional

class RiddleForm(FlaskForm):
    """新增或編輯謎題的表單"""
    name = StringField('彩蛋內部代號', validators=[DataRequired()])
    riddle = TextAreaField('藏寶圖上的謎語', validators=[DataRequired()])
    hint = StringField('給偵探的小提示 (可選)', validators=[Optional()])
    submit = SubmitField('畫在地圖上')
