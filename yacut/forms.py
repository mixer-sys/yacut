from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut.settings import (
    CUSTOM_ID_MAX_LEN, CUSTOM_ID_MIN_LEN,
    ORIGINAL_LINK_MAX_LEN, ORIGINAL_LINK_MIN_LEN
)


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=(DataRequired(message='Обязательное поле'),
                    Length(ORIGINAL_LINK_MIN_LEN, ORIGINAL_LINK_MAX_LEN))
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=(Length(CUSTOM_ID_MIN_LEN, CUSTOM_ID_MAX_LEN), Optional())
    )
    message = StringField(
        'Сообщение о готовности ссылки'
    )
