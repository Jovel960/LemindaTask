import os
from dotenv import load_dotenv

load_dotenv()

APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')