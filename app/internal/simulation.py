from app.internal import response_agent 
from app.data_models import SurveyModel, DemographicModel, AgentParameters
import traceback
from typing import Dict, List
from app.internal.prompt_payloads import input_question, initialization_prompt

import json
import openai.error
import time



#when an instance is ran, return a response_data json object containing responses and demographic data
#this is the part that can be setup as a celery task, so json as input and output




class Simulator():
    #unwraps agent parameters and performs initialization of agent 
    def __init__(self, survey: Dict, demographic: Dict, agent_params: AgentParameters):
        self.survey_responses: List[Dict] = []
        self.survey_context: str = survey["description"]
        self.survey_questions: List[Dict] = survey["questions"]
        self.demographic: Dict = demographic["demographic"]
        self.persona: Dict = demographic["persona"]

        self.simulator = response_agent.Agent(
            ##replace with initialization prompt
            instruction = initialization_prompt(demographic), 
            params = agent_params
            )
    


    def simulate(self) -> Dict:
    
        retries = 3

        survey_context: str = self.survey_context
       


        self.simulator.inject_memory(survey_context)
        # for k, v in self.demographic.items():
        #     self.simulator.inject_memory(f"{k}: {v}")
        

        #iterating through world state
        survey_questions: List[Dict] = self.survey_questions
        for question in survey_questions:

            response_schema = question
            prompt: str = input_question(question)

            for _ in range(retries):

                try:
                    response = self.simulator.chat(query=prompt)
                    response_json = json.loads(response)
                    answer = response_json["answer"]
                    response_schema["answer"] = answer
                    self.survey_responses.append(response_schema)
                    break
                except KeyError:
                    print(f"'answer' not found in response {response_json} (Attempt {_ + 1}).")
                except json.JSONDecodeError:
                    print(f"Error decoding the response JSON (Attempt {_ + 1}).")
                except (openai.error.ServiceUnavailableError, openai.error.Timeout, openai.error.RateLimitError) as e:
                    print(f'OpenAI error (Attempt {_ + 1}): {json.dumps(response_schema)}. {e}')
                    wait_time=60
                    print (f'Waiting for {wait_time} seconds before resuming.')                   
                    time.sleep(wait_time)
                except Exception as e:
                    print(f"Error in generating response (Attempt {_ + 1}): {json.dumps(response_schema)}. {e}")
                    traceback.print_exc()  
            else:
                print(f"Maximum retries reached for question: {json.dumps(response_schema)}. Skipping to next question.")
                response_schema["answer"] = None
                self.survey_responses.append(response_schema)
                continue
        
        simulation_result = {
            "response_data": self.survey_responses,
            "demographic_data": self.demographic,
            "persona": self.persona
        }

        return simulation_result



    



