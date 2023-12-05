from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN-AI-API-KEY")
MONGO_URI= os.getenv("MONGO-URI")
REDIS_URI = os.getenv("REDIS-URI")
REDIS_PORT = os.getenv("REDIS-PORT")
DEBUG = os.getenv("DEBUG") == 'True'
