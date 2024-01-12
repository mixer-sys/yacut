import os

ID_NOT_FOUND = 'Указанный id не найден'
BODY_IS_NONE = 'Отсутствует тело запроса'
URL_REQUIRED = '"url" является обязательным полем!'
SHORT_LINK_EXIST = 'Предложенный вариант короткой ссылки уже существует.'
BAD_SHORT_LINK = 'Указано недопустимое имя для короткой ссылки'
VALIDATOR_MESSAGE = 'Обязательное поле'
CUSTOM_ID_MIN_LEN = 2
CUSTOM_ID_MAX_LEN = 16
RANDOM_STRING_LEN = 6
ORIGINAL_LINK_MIN_LEN = 1
ORIGINAL_LINK_MAX_LEN = 256


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
