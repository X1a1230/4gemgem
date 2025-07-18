from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class LetterForm(FlaskForm):
    """寫信的表單"""
    author = StringField('你的署名 (可選)', validators=[Optional(), Length(max=100)])
    question = TextAreaField('信件內容', validators=[DataRequired()])
    submit = SubmitField('投進郵筒')
