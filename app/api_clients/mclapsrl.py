import requests
from app import settings
from pydantic import BaseModel
from app.data_models import open_ai_models




def model_filter(model: str) -> open_ai_models:
    if "gpt-3.5-turbo" in model:
        return "gpt-3.5-turbo"
    if "gpt-4-turbo" in model:
        return "gpt-4-turbo"
    if "gpt-4-0125-preview" in model:
        return "gpt-4-turbo"
    if "gpt-4o" in model:
        return "gpt-4o"
    if "gpt-4o-mini" in model:
        return "gpt-4o-mini"
    if "gpt-4-1106-preview" in model:
        return "gpt-4-turbo"
    if "text-embedding-3-small" in model:
        return "text-embedding-3-small"
    if "text-embedding-3-large" in model:
        return "text-embedding-3-large"
    else:
        return model

def parse_response(response) -> dict:
    try:
        model = model_filter(response.model)
    except AttributeError:
        model = None
    try:
        input_tokens = response.usage.prompt_tokens
    except AttributeError:
        input_tokens = 0
    try:
        output_tokens = response.usage.completion_tokens
    except AttributeError:
        output_tokens = 0
    try:    
        total_tokens = response.usage.total_tokens
    except AttributeError:
        total_tokens = 0
    parsed_json = {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens
    }
    return parsed_json


class mclapsrlClient:
    def __init__(self):
        self.base_url = settings.MCLAPSRL_API
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    def check_service_status(self) -> dict:
        response_root = (requests.get(f"{self.base_url}/")).json()
        response_redis = (requests.get(f"{self.base_url}/redis_connection")).json()
        mclapsrl_status = {
            "root_status": response_root,
            "redis_status": response_redis
        }
        return mclapsrl_status

    def get_counter_status(self, model: open_ai_models):
        response = requests.get(f"{self.base_url}/counter_status", params={'model': model})
        return response.json()


    #post
    def create_counter(self, model: open_ai_models) -> bool:
        attempts = 10
        while attempts > 0:
            try:
                response = (requests.post(f"{self.base_url}/create_counter", headers = self.headers, json = {"model":model})).json()  # returns true false for whether counter created
                if response == True:
                    return True
                else:
                    print(f"Counter creation failed for model {model}, retrying  ({attempts} attempts remaining).")
                    attempts -= 1
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                print(f"Error in mclapsrl connection: {e}, retrying  ({attempts} attempts remaining).")
                attempts -= 1
            
        return False
    

    #post
    def new_response(self, response) -> bool:
        #openai generator object parsed to dictionary
        response_body = parse_response(response)

        attempts = 10
        while attempts > 0:
            try:
                response = requests.post(f"{self.base_url}/new_response", headers = self.headers, json = response_body)
                if response.json() == True:
                    return True
                else:
                    print(f"Response logging failed, retrying  ({attempts} attempts remaining).")
                    attempts -= 1
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                print(f"Error in mclapsrl connection: {e}, retrying  ({attempts} attempts remaining).")
                attempts -= 1
            except requests.exceptions.RequestException as e:
                print(f"Request exception: {e}")
                break #breaks loop if request exception occurs

        return False


    #returns boolean status of model, or false if client is down, so if client is down the simulation halts indefinitely
    def model_status(self, model: open_ai_models) -> bool:      
        attempts = 10
        while attempts > 0:
            try:
                response = requests.get(f"{self.base_url}/model_status", params={'model': model})
                return response.json()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                print(f"Error in mclapsrl connection: {e}, retrying ({attempts} attempts remaining).")
                attempts -= 1
        
        return False



