from app.internal import response_agent 
import traceback
from typing import Dict, List

import json
import openai.error
import time


#when an instance is ran, return a response_data json object containing responses and demographic data
#this is the part that can be setup as a celery task, so json as input and output




class Simulator():

    def __init__(self,survey: Dict, demographic: Dict):
        self.survey_responses: List[Dict] = []
        self.survey_context: str = survey["description"]
        self.survey_questions: List[Dict] = survey["questions"]
        self.demographic: Dict = demographic

    def simulate(self) -> Dict:
    
        retries = 3

        survey_context: str = self.survey_context
        survey_questions: List[Dict] = self.survey_questions


        simulator = response_agent.Agent(instruction="You are behaving like a real person.", model = "gpt-3.5-turbo-0125", json_mode = True)
        simulator.inject_memory(survey_context)
        for k, v in self.demographic.items():
            simulator.inject_memory(f"{k}: {v}")
        

        for question in survey_questions:
            question_schema = question
            prompt = question_schema["question"] + "\nResponse schema:\n" + json.dumps(question_schema)

            for _ in range(retries):

                try:
                    response = simulator.chat(query=prompt)
                    response_json = json.loads(response)
                    answer = response_json["answer"]
                    question_schema["answer"] = answer
                    self.survey_responses.append(question_schema)
                    break
                except json.JSONDecodeError:
                    print(f"Error decoding the response JSON (Attempt {_ + 1}).")
                except openai.error.ServiceUnavailableError as e:
                    print(f'Service unavailable error (Attempt {_ + 1}): {json.dumps(question_schema)}. {e}')
                    wait_time=60
                    time.sleep(wait_time)
                    print (f'Waiting for {wait_time} seconds before resuming.')
                except openai.error.Timeout as e:
                    print(f'OpenAI Timeout error (Attempt {_ + 1}): {json.dumps(question_schema)}. {e}')
                    wait_time=60
                    time.sleep(wait_time)
                    print (f'Waiting for {wait_time} seconds before resuming.')
                except openai.error.RateLimitError as e:
                    print(f'Rate limit error (Attempt {_ + 1}): {json.dumps(question_schema)}. {e}')
                    wait_time=60
                    time.sleep(wait_time)
                    print (f'Waiting for {wait_time} seconds before resuming.')
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



    



