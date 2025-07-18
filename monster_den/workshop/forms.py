from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Optional


class ThoughtForm(FlaskForm):
    """新增漂流瓶（思緒）的表單"""
    # 這是你新增的欄位，我猜 bottle_id 是獨一無二的，所以是必填
    bottle_id = StringField('瓶子的ID', validators=[DataRequired()])
    # title 是可選的，所以我們用 Optional()
    title = StringField('瓶子的標籤 (可選)', validators=[Optional()])
    # 這是你新增的欄位，我猜 type 是從一個下拉選單裡選的
    type = SelectField('瓶子類型', choices=[('thought', '思緒'), ('question', '問題'), ('image_idea', '圖像')], validators=[DataRequired()])
    # 內容是必填的
    content = TextAreaField('瓶子裡的內容', validators=[DataRequired()])
    submit = SubmitField('裝進瓶子，漂向大海')
