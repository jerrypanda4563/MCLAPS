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
    
    def get_task_status(self, task_ids: list[str]) -> bool:
        retries = 10
        while retries > 0:

            try:
                response = requests.get(f"{self.base_url}/demgen/status", params = {"task_ids": task_ids}, headers = self.headers).json()
                truth_values = [response[task_id] for task_id in task_ids]
                if all(truth_value == "finished" for truth_value in truth_values):
                    return True
                elif all(truth_value == "started" for truth_value in truth_values):
                    return False
                else:
                    return None

            except requests.exceptions.HTTPError as e:
                if e == 404:
                    print(f"Task {task_ids} not found.")
                    return None
                if e == 500:
                    retries -= 1
                    print(f"Internal server error. Retries remaining: {retries}")   

        return None
    
    def get_task_results(self, task_ids: list[str]) -> list[dict]:
        retries = 10
        while retries > 0:
            try:
                response = requests.get(f"{self.base_url}/demgen/result", params = {"task_ids": task_ids}, headers=self.headers).json()
                if response == "null":
                    return []
                
                return response
            
            except requests.exceptions.HTTPError as e:
                if e == 404:
                    print(f"Task {task_id} not found.")
                    return None
                if e == 500:
                    retries -= 1
                    print(f"Internal server error. Retries remaining: {retries}")
        return None




