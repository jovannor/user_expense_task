import os
import environ
'''
CREATE USER user_expense_usr with password '468gA4edffu2dffgfghgghdsdsd33445sd56fsds34e3WKaG8x';
CREATE DATABASE user_expense_db OWNER user_expense_usr;
GRANT ALL PRIVILEGES ON DATABASE user_expense_db to user_expense_usr;
'''

WEBSITE_ROOT = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)

PROJECT_ROOT = os.path.abspath(os.path.dirname(WEBSITE_ROOT))

env = environ.Env()
for filename in os.listdir(PROJECT_ROOT):
    if filename.endswith('.env'):
        env_file = os.path.join(PROJECT_ROOT, filename)
        env.read_env(env_file)

# SECRET_KEY = "django-insecure-_(t422i0!6x&oa^ft7y6*s3sdfd567tu@u=gvint9nc#s8b$78keudw$d5"
os.environ['DJANGO_SETTINGS_MODULE'] = "project.core.settings.local"
os.environ['POSTGRES_HOST'] = "localhost"


from .base import *