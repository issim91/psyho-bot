import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# API Tokens
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:postgres@localhost/psychobot')

# Session settings
SESSION_DURATION = timedelta(minutes=60)
MAX_SESSIONS_PER_USER = 4

# OpenAI settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPEN_AI_MODEL', 'gpt-4o')
OPENAI_TEMPERATURE = 0.7
OPENAI_MAX_TOKENS = 2000

# Psychologist personality settings
PSYCHOLOGIST_NAME = 'Доктор'
PSYCHOLOGIST_GENDER = 'female'
PSYCHOLOGIST_AGE = '45'
PSYCHOLOGIST_SPECIALIZATION = 'когнитивно-поведенческая терапия' 
