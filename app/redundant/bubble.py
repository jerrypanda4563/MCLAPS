from bubble_api import BubbleClient
from typing import List,Dict, Type
from app.internal import simulation, simulation_runner
from app import settings

bubble_client = BubbleClient(
    base_url=settings.BUBBLE_DATA_API_URL,
    api_token=settings.BUBBLE_DATA_API_TOKEN,
    bubble_version=settings.BUBBLE_VERSION
)


def save_to_bubble(data: Dict[Type[simulation_runner.run_single_simulation]], data_type: str, simulation_id: str):
    ##data to save is simulation_data, output returned from run_single_simulation

    demographic=data["demographic_data"] #its a dictionary with multiple different key value pairs
    response = data["response_data"]
    type = data_type
    response_data_formatted = {}
    
    response_data_formatted["Simulation ID"] = simulation_id
    demographic["Simulation ID"]=simulation_id

    for item in response:
        key=item["question"]
        value=item["answer"]
        response_data_formatted[key] = value
        
    
    try:
        bubble_client.create(type,response_data_formatted)
    except Exception as e:
        print(f"An error occurred appending response data: {e}")

    try:
        bubble_client.create("Demographic Data", demographic)
    except Exception as e:
        print(f"An error occurred appending demographic data: {e}")

