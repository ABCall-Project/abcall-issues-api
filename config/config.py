import os
from dotenv import load_dotenv

environment = os.getenv('FLASK_ENV')

if environment == 'local':
    load_dotenv(dotenv_path='.env.local')
else:
    load_dotenv(dotenv_path='.env')

class Config:
    ENVIRONMENT = environment
    APP_NAME=os.getenv('APP_NAME')
    DATABASE_URI=os.getenv('DATABASE_URI')
    AUTH_API_PATH=os.getenv('AUTH_API_PATH')