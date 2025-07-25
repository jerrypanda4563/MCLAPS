from app.internal import response_agent 
from app.data_models import SurveyModel, DemographicModel, AgentParameters
import traceback
from typing import Dict, List, Optional
from app.internal.prompt_payloads import initialization_prompt, Iterator

import json
import openai.error
import time



#when an instance is ran, return a response_data json object containing responses and demographic data
#this is the part that can be setup as a celery task, so json as input and output




class Simulator():
    #unwraps agent parameters and performs initialization of agent 
    def __init__(self, survey: Dict, demographic: Dict, agent_params: AgentParameters, retries: Optional[int] = 3):
        
        self.results: list[dict] = []

        self.survey_context: list[str] = survey["context"]
        self.json_mode: bool = agent_params.json_mode
        
        self.iterator = Iterator(json_mode = agent_params.json_mode, iteration_questions = survey["questions"])
        self.demographic: Dict = demographic["demographic"]
        self.persona: Dict = demographic["persona"]

        self.simulator = response_agent.Agent(
            ##replace with initialization prompt
            instruction = initialization_prompt(self.demographic, self.persona), 
            params = agent_params
            )
        
        self.retry_policy = retries
        
        
    def simulate(self) -> Dict:

        for context in self.survey_context:
            self.simulator.inject_memory(context)
        
        #iterating though generator object
        for _ in range(self.iterator.n_of_iter):
            current_iteration = self.iterator.iter()
            schema = self.iterator.iterations[_]

            for i in range(self.retry_policy):
                try: 
                    result = self.simulator.chat(current_iteration)
                    print(result)
                    break
                except (openai.error.ServiceUnavailableError, openai.error.Timeout, openai.error.RateLimitError) as e:
                    print(f'OpenAI error in simulation run for agent {self.simulator.agent_id} (Attempt {i + 1}): for question {_+1}. {e}')
                    traceback.print_exc()  
            else:
                print(f"Maximum retries reached for question: {json.dumps(schema)}. Skipping to next question.")
                schema["answer"] = None
                self.results.append(schema)
                break
            
            if self.json_mode:
                try:
                    response_json = json.loads(result)
                    answer = response_json["answer"]
                    schema["answer"] = answer
                    self.results.append(schema)
                except Exception as e: 
                    schema["answer"] = result
                    self.results.append(schema)
            else:
                schema["answer"] = result
                self.results.append(schema)
        

        simulation_result = {
            "response_data": self.results,
            "demographic_data": self.demographic,
            "persona": self.persona
        }

        return simulation_result






    



