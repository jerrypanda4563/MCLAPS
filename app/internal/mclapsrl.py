import requests
from app import settings
from app.data_models import open_ai_models




class mclapsrlClient:
    def __init__(self):
        self.base_url = settings.MCLAPSRL_API

    def check_service_status(self) -> dict:
        """Check the root status of the API."""
        response_root = (requests.get(f"{self.base_url}/")).json()
        response_redis = (requests.get(f"{self.base_url}/redis_connection")).json()
        mclapsrl_status = {
            "root_status": response_root,
            "redis_status": response_redis
        }
        return mclapsrl_status

    def get_counter_status(self, model: open_ai_models):
        """Retrieve the status of the counter for a specified model."""
        response = requests.get(f"{self.base_url}/counter_status", params={'model': model})
        return response.json()





    #if counter created, returns true, if counter creation failed or client is down, returns false
    def create_counter(self, model: open_ai_models) -> bool:
        attempts = 10
        while attempts > 0:
            try:
                response = (requests.post(f"{self.base_url}/create_counter", json={'model': model})).json()  # returns true false for whether counter created
                if response == True:
                    return True
                else:
                    print(f"Counter creation failed for model {model}, retrying  ({attempts} attempts remaining).")
                    attempts -= 1
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                print(f"Error in mclapsrl connection: {e}, retrying  ({attempts} attempts remaining).")
                attempts -= 1
            
        return False
    
    #if new response logged, returns true, if logging failed or client is down, returns false
    def new_response(self, response_body) -> bool:
        attempts = 10
        while attempts > 0:
            try:
                response = (requests.post(f"{self.base_url}/new_response", json={'response_body': response_body})).json()
                if response == True:
                    return True
                else:
                    print(f"Response logging failed, retrying  ({attempts} attempts remaining).")
                    attempts -= 1
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                print(f"Error in mclapsrl connection: {e}, retrying  ({attempts} attempts remaining).")
                attempts -= 1

        return False

    #returns boolean status of model, or false if client is down, so if client is down the simulation halts indefinitely
    def model_status(self, model) -> bool:      
        attempts = 10
        while attempts > 0:
            try:
                response = (requests.get(f"{self.base_url}/model_status", params={'model': model})).json()
                return response
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                print(f"Error in mclapsrl connection: {e}, retrying ({attempts} attempts remaining).")
                attempts -= 1
        
        return False



