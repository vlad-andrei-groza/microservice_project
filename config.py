import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///math.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
