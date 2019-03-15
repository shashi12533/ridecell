import hashlib
import uuid
from datetime import datetime

from itsdangerous import URLSafeSerializer
from config import get_config

__author__ = 'shashi'


CONFIG = get_config()


def get_date_time():
    return datetime.now()


def generate_unique_business_id():
    return str(uuid.uuid4())


def md5_encrypt(val):
    return hashlib.md5(val).hexdigest()


def generate_verification_token(payload):
    serializer = URLSafeSerializer(CONFIG.SECRET_KEY)
    return serializer.dumps(payload)


def verify_token(token):
    serializer = URLSafeSerializer(CONFIG.SECRET_KEY)
    try:
        data = serializer.loads(token)
    except Exception as err:
        # TODO Log error here somehow
        return False
    return data
