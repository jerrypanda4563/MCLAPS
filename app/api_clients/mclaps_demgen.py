import httpx
import requests
import json
from app.data_models import DemographicModel
from pydantic import BaseModel
from app.settings import MCLAPS_DEMGEN_API



class DemgenRequest(BaseModel):
    number_of_samples: int
    sampling_conditions: DemographicModel


class MclapsDemgenClient:
    def __init__(self):
        self.base_url = MCLAPS_DEMGEN_API
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    def read_root(self) -> dict:
        response = requests.get(f"{self.base_url}/")
        return response.json()
    
    def service_status(self) -> dict:
        response = requests.get(f"{self.base_url}/test_services")
        return response.json()
    
    def demgen_request(self, request_body: DemgenRequest) -> dict:
        response = requests.post(f"{self.base_url}/demgen/request", headers=self.headers, json = request_body.dict())
        return response.json()
    
    def get_task_status(self, task_id: str) -> bool:
        retries = 10
        while retries > 0:
            try:
                response = requests.get(f"{self.base_url}/demgen/status/{task_id}").json()
                if response["task_status"] == "finished":
                    return True
                else:
                    return False
            except requests.exceptions.HTTPError as e:
                if e == 404:
                    print(f"Task {task_id} not found.")
                    return None
                if e == 500:
                    retries -= 1
                    print(f"Internal server error. Retries remaining: {retries}")
                    
        return None
    
    def get_task_results(self, task_id: str) -> list[dict]:
        retries = 10
        while retries > 0:
            try:
                response = requests.get(f"{self.base_url}/demgen/result/{task_id}")
                return response.json()
            
            except requests.exceptions.HTTPError as e:
                if e == 404:
                    print(f"Task {task_id} not found.")
                    return None
                if e == 500:
                    retries -= 1
                    print(f"Internal server error. Retries remaining: {retries}")
        return None





        response = requests.get(f"{self.base_url}/task_results/{task_id}")
        return response.json()