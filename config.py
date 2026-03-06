"""
所有配置项
"""
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

SECRET_KEY = "sadadfaf"

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'vegetable_provider'
MYSQL_CHARSET = 'utf8mb4'


SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}"
# SQLALCHEMY_ECHO = True
# SQLALCHEMY_TRACK_MODIFICATION = False

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USERNAME = '3330291170@qq.com'
MAIL_PASSWORD = 'zutnymsnnbnydcbj'

MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = '3330291170@qq.com'
