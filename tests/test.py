from app import mongo_config, redis_config
import openai
import app.settings as settings


def redis_connection_test() -> bool:
    redis_config.cache_connection_test() #return boolean
def mongo_connection_test() -> bool:
    mongo_config.db_connection_test() #return boolean

def openai_connection_test() -> bool:
    openai.api_key=settings.OPEN_AI_KEY
    try:
        # Make a test call to the API, for example, list available models
        response = openai.Engine.list()
        print("Connection successful. Available engines:")
        print(response)
        return True
    except Exception as e:
        print(f"An error occurred connecting to OpenAI: {e}")
        return False

if __name__ == "__main__":
    openai_connection_test()
    mongo_connection_test()
    redis_connection_test()




