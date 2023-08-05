import hashlib
import string
from random import choice


def random_string(length=8):
    options = string.ascii_letters + string.digits

    return ''.join(choice(options) for _ in range(length))


def sha1(content, encoding='utf-8'):
    return hashlib.sha1(
        content.encode(encoding)
    ).hexdigest()
