from app.internal import agent, demgen
from typing import Dict
import json
import openai.error
import time


class MaxRetry(Exception):
    pass


### class simulate implementing exception handling, creates a single instances of demo and agent, input is survey plus all dem param


class Simulation():
    def __init__(self, survey: list, demo: Dict, context=None):
        # input
        self.survey = survey  # must be a list of dict
        self.survey_context = context  # str
        # temp memory for storing output
        self.demographic = demo
        self.demographic_data = {}
        self.responses = []


    def run(self):
        max_retries = 3  # Set maximum number of retries

        # Retry block for generating demographic
        for _ in range(max_retries):
            try:
                demo = demgen.generate_demographic(self.demographic)
                break

            except openai.error.RateLimitError as e:
                    print(f'Rate limit error (Attempt {_ + 1}): {e}')
                    wait_time=10
                    time.sleep(wait_time)
                    print (f'Waiting for {wait_time} before resuming.')
                    

            except Exception as e:
                print(f"Error in generating demographic (Attempt {_ + 1}): {e}")
        else:  # This else block is executed if the loop ends without a break
            print("Maximum retries reached for generating demographic.")
            raise MaxRetry("Maximum retries reached for generating demographic.")
        # End of retry block


        #  block for loading demographic data
        try:
            self.demographic_data.update(json.loads(demo))
        except json.JSONDecodeError:
            print(f"Error decoding the generated demographic JSON (Attempt {_ + 1}).")
        except Exception as e:
            print(f"Error in updating demographic data (Attempt {_ + 1}): {e}")

        # End of block


        # initiating simulation agent
        simulator = agent.Agent(
            "You are a person with the following demographic characteristics expressed as a json dictionary:" + demo + "\nRespond to the following survey questions expressed as a list of json dictionaries by replacing null values with your answer. Your output must maintain the same data structure as the input.")
        if isinstance(self.survey_context, str):
            simulator.inject_memory(self.survey_context)

        # iterating through questions list
        for question in self.survey:
            prompt = json.dumps(question)

            # Retry block for generating response
            for _ in range(max_retries):
                try:
                    response = simulator.chat(prompt)
                    break
                
                except openai.error.RateLimitError as e:
                    print(f'Rate limit error (Attempt {_ + 1}): {question}. {e}')
                    wait_time=10
                    time.sleep(wait_time)
                    print (f'Waiting for {wait_time} before resuming.')

                except Exception as e:
                    print(f"Error in chat simulation for question (Attempt {_ + 1}): {question}. Error: {e}")
            else:
                print(f"Maximum retries reached for question: {question}. Skipping to next question.")
                continue
            # End of block

            # try block for loading response data
            try:
                response_data = json.loads(response)
                self.responses.append(response_data)
                
            except json.JSONDecodeError:
                print(f"Error decoding the response JSON.")
            except Exception as e:
                print(f"Error processing response data: {e}")
         
            # End of block
