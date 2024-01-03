from dotenv import load_dotenv
import os


load_dotenv()

TOKEN_API_KEY = os.getenv(
    'TOKEN_API_KEY',
    '123123123123123123',  # placeholder for a key
)

ADMIN_ID = os.getenv('ADMIN_ID', 0)

DB_PATH = os.getenv('DB_PATH', '')
