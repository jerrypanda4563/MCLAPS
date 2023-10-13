from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN-AI-API-KEY")
DEBUG = os.getenv("DEBUG") == 'True'