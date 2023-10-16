from bubble_api import BubbleClient
from typing import List, Type
from app.internal import simulation
from app import settings

bubble_client = BubbleClient(
    base_url=settings.BUBBLE_DATA_API_URL,
    api_token=settings.BUBBLE_DATA_API_TOKEN,
    bubble_version=settings.BUBBLE_VERSION
)


def save_simulation(sim: List[Type[simulation.Simulation]]):
    simulation_list = List[map]
    for cls in sim:
        answer_dict = {}
        # Use the question as the key and the answer as the value
        question = cls.responses["question"]
        answer = cls.responses["answer"]
        answer_dict[question] = answer
        simulation_list.append(answer_dict)
        
    try: 
        bubble_client.create_bulk("database_name", simulation_list)

    except Exception as e:
        print('failed saving to bubble database', e)
