import string
import random

from yacut.settings import RANDOM_STRING_LEN


class HTTPMethod:
    GET = 'GET'
    POST = 'POST'


def get_unique_short_id():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=RANDOM_STRING_LEN
        )
    )
