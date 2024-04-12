import requests
from app import settings
from app.data_models import open_ai_models


#error handling need to e added

class APIClient:
    def __init__(self):
        self.base_url = settings.MCLAPSRL_API

    def check_status(self):
        """Check the root status of the API."""
        response = requests.get(f"{self.base_url}/")
        return response.json()

    def check_redis_connection(self):
        """Check the Redis connection status."""
        response = requests.get(f"{self.base_url}/redis_connection")
        return response.json()

    def create_counter(self, model: open_ai_models):
        """Create a counter for a specified model."""
        response = requests.get(f"{self.base_url}/create_counter", params={'model': model})
        return response.json()

    def get_counter_status(self, model: open_ai_models):
        """Retrieve the status of the counter for a specified model."""
        response = requests.get(f"{self.base_url}/counter_status", params={'model': model})
        return response.json()

    def new_response(self, response_body):
        """Log a new response and update the counter."""
        response = requests.post(f"{self.base_url}/new_response", json={'response_body': response_body})
        return response.json()

    def get_model_status(self, model):
        """Check if a model is ready to accept requests."""
        response = requests.get(f"{self.base_url}/model_status", params={'model': model})
        return response.json()


