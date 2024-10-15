import requests
import json
from app.data_models import DemographicModel
from pydantic import BaseModel
from app.settings import MCLAPS_DEMGEN_API



class DemgenRequest(BaseModel):
    number_of_samples: int
    batch_size: int
    sim_id: str
    sampling_conditions: DemographicModel




class MclapsDemgenClient:
    def __init__(self):
        self.base_url = MCLAPS_DEMGEN_API
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    def array_status(self) -> dict:
        response = requests.get(f"{self.base_url}/data_arr_status", headers=self.headers)
        return response.json()
            
    def read_root(self) -> dict:
        response = requests.get(f"{self.base_url}/")
        return response.json()
    
    def reinitialize(self) -> dict:
        response = requests.get(f"{self.base_url}/data_reset", headers=self.headers)
        return response.json()
    
    def service_status(self) -> dict:
        response = requests.get(f"{self.base_url}/test_services", headers=self.headers)
        return response.json()
    
    def kill_all_task(self) -> bool:
        response = requests.get(f"{self.base_url}/kill_all", headers=self.headers)
        return response.json()
    
    def demgen_request(self, request_body: DemgenRequest) -> dict:
        response = requests.post(f"{self.base_url}/demgen/request", headers=self.headers, json = request_body.dict())
        return response.json()
    
    def get_task_status(self, task_id: str) -> bool:
        response = requests.get(f"{self.base_url}/demgen/task_status", params = {"task_id": task_id}, headers = self.headers)
        return response.json()
    
    def get_task_results(self, task_id: str) -> dict:
        response = requests.get(f"{self.base_url}/demgen/task_result", params = {"task_id": task_id}, headers=self.headers)
        return response.json()
    
    def get_dataset(self, dataset_id: str) -> dict:
        response = requests.get(f"{self.base_url}/demgen/dataset", params = {"dataset_id": dataset_id}, headers=self.headers)
        return response.json()

    