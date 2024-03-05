from app.internal import response_agent 
import traceback
from typing import Dict, List

import json
import openai.error
import time
from multiprocessing import Lock


#when an instance is ran, return a response_data json object containing responses and demographic data
#this is the part that can be setup as a celery task, so json as input and output




class Simulator():

    def __init__(self,survey: Dict, demographic: Dict, agent_model:str, agent_temperature:float):
        self.survey_responses: List[Dict] = []
        self.survey_context: str = survey["description"]
        self.survey_questions: List[Dict] = survey["questions"]
        self.demographic: Dict = demographic
        self.simulator = response_agent.Agent(instruction="You are behaving like a real person.", model = agent_model, temperature = agent_temperature, json_mode = True)
        self.wait_lock = Lock()
    
    
    def simulate(self) -> Dict:
    
        retries = 3

        survey_context: str = self.survey_context
        survey_questions: List[Dict] = self.survey_questions


        self.simulator.inject_memory(survey_context)
        for k, v in self.demographic.items():
            self.simulator.inject_memory(f"{k}: {v}")
        

        for question in survey_questions:
            question_schema = question
            prompt = question_schema["question"] + "\nResponse schema:\n" + json.dumps(question_schema)

            for _ in range(retries):

                try:
                    response = self.simulator.chat(query=prompt)
                    response_json = json.loads(response)
                    answer = response_json["answer"]
                    question_schema["answer"] = answer
                    self.survey_responses.append(question_schema)
                    break
                except json.JSONDecodeError:
                    print(f"Error decoding the response JSON (Attempt {_ + 1}).")
                except (openai.error.ServiceUnavailableError, openai.error.Timeout, openai.error.RateLimitError) as e:
                    print(f'OpenAI error (Attempt {_ + 1}): {json.dumps(question_schema)}. {e}')
                    wait_time=60
                    print (f'Waiting for {wait_time} seconds before resuming.')
                    with self.wait_lock:
                        time.sleep(wait_time)
                except Exception as e:
                    print(f"Error in generating response (Attempt {_ + 1}): {json.dumps(question_schema)}. {e}")
                    traceback.print_exc()  
            else:
                print(f"Maximum retries reached for question: {json.dumps(question_schema)}. Skipping to next question.")
                question_schema["answer"] = None
                self.survey_responses.append(question_schema)
                continue
        
        simulation_result = {
            "response_data": self.survey_responses,
            "demographic_data": self.demographic
        }

        return simulation_result



    



