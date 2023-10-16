from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN-AI-API-KEY")
BUBBLE_DATA_API_URL = os.getenv("BUBBLE-DATA-API-URL")
BUBBLE_DATA_API_TOKEN = os.getenv("BUBBLE-DATA-API-TOKEN")
BUBBLE_VERSION = os.getenv("BUBBLE-VERSION")
DEBUG = os.getenv("DEBUG") == 'True'
