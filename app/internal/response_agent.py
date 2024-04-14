from app.internal import agent_data
from app.internal.tokenizer import count_tokens
from app.internal.mclapsrl import mclapsrlClient
from app import settings

import time
import numpy as np

import spacy
from typing import List, Optional
import openai
from sklearn.metrics.pairwise import cosine_similarity as cs
from concurrent.futures import ThreadPoolExecutor

openai.api_key = settings.OPEN_AI_KEY


nlp = spacy.load("en_core_web_sm")
rate_limiter = mclapsrlClient()



class Agent:

    def __init__(self, instruction:str, model:Optional[str] = "gpt-3.5-turbo", temperature: Optional[float] = 1.21, json_mode:Optional[bool] = True):
        self.lt_memory = agent_data.AgentData()
        self.st_memory: List[str] = []
        self.st_memory_capacity: int = 2000
        self.instruction:str = instruction
        self.llm_model = model
        self.temperature = temperature
        self.json_mode = json_mode
    

    #add limiter
    def embed(self, string:str, embedding_model: Optional[str] = "text_embedding-3-small") -> np.ndarray:
        while rate_limiter.model_status(embedding_model) == False:
            time.sleep(2)
        response=openai.Embedding.create(
            model = embedding_model,
            input=str(string)
            )
        rate_limiter.new_response(response)
        embedding = np.array(response['data'][0]['embedding'])
        return embedding

        

    def evaluator(self, string1:str, string2:str) -> float:
        try:
            k = cs(self.embed(string1).reshape(1,-1),self.embed(string2).reshape(1,-1))[0][0]
            return k
        except Exception as e:
            try:
                v_1=np.array(nlp(string1).vector)
                v_2=np.array(nlp(string2).vector)
                k_backup = cs(v_1.reshape(1,-1),v_2.reshape(1,-1))[0][0]
                return k_backup  
            except Exception as e:
                return 0  # or any other default value
        
    def st_memory_length(self) -> int:
        return count_tokens(' '.join(self.st_memory))
    

    def construct_st_memory(self, query:str) -> None:
        if len(self.st_memory) == 0:
            recalled_information = self.lt_memory.query(query)
            if recalled_information is not None:
                for string in recalled_information:
                    self.st_memory.append(string)
        else:   
            current_memory = '\n'.join(self.st_memory)
            k = self.evaluator(query, current_memory)
            recalled_information = self.lt_memory.query(query, evalutator_k=k)
            if recalled_information is not None:
                for string in recalled_information:
                    self.st_memory.append(string)
            if self.st_memory_length() > self.st_memory_capacity:
                self.restructure_memory(query)
    
    
    
    #pop out strings with lowest similarity to query
    def restructure_memory(self, query:str) -> None:
        similarity_scores = []
        with ThreadPoolExecutor(max_workers=len(self.st_memory)) as executor:
            similarity_scores = list(executor.map(lambda x: self.evaluator(query, x), self.st_memory))
        
        new_lt_memory: List[str] = []
        while self.st_memory_length() > self.st_memory_capacity:
            index = similarity_scores.index(min(similarity_scores))
            forgotten_memory = self.st_memory.pop(index)
            similarity_scores.pop(index)
            new_lt_memory.append(forgotten_memory)
        new_lt_memory = '\n'.join(new_lt_memory)
        self.lt_memory.add_data_str(new_lt_memory)
            

    #add limiter
    def model_response(self, query: str) -> str:
        memory_prompt = "You recall the following information:\n" + '\n'.join(self.st_memory)

        if self.json_mode == True:
            while rate_limiter.model_status(self.llm_model) == False:
                time.sleep(2)
            completion = openai.ChatCompletion.create(
                    model = self.llm_model,
                    response_format={"type": "json_object"},
                    messages=[
                            {"role": "system", "content": self.instruction},
                            {"role": "user", "content": memory_prompt +"\n"+"Based on the information, you respond to the following query in json:/n"+query},
                        ],
                    temperature=self.temperature,
                    max_tokens=512,
                    n=1  
                    )
            # rate_limiter.new_response(completion)
            print(type(completion))
            response=completion.choices[0].message.content
            return response

        else:
            while rate_limiter.model_status(self.llm_model) == False:
                time.sleep(2)
            completion=openai.ChatCompletion.create(
                    model = self.llm_model,
                    messages=[
                            {"role": "system", "content": self.instruction},
                            {"role": "user", "content": memory_prompt +"\n"+"Based on the information, you respond to the following query:/n"+query},
                        ],
                    temperature=self.temperature,
                    max_tokens=512,
                    n=1  
                    )
            # rate_limiter.new_response(completion)
            print(type(completion))
            response=completion.choices[0].message.content
            return response
    
    
    #endpoints
    def chat(self, query:str) -> str:
        self.construct_st_memory(query)
        response = self.model_response(query)
        self.st_memory.append(":\n".join([query,response]))
        if self.st_memory_length() > self.st_memory_capacity:
            self.restructure_memory(query)
        return response
    
    def inject_memory(self, string:str) -> None:
        if count_tokens(string) > 110:
            self.lt_memory.add_data_str(string)
        else:
            self.st_memory.append(string)
            if self.st_memory_length() > self.st_memory_capacity:
                self.restructure_memory(string)
            
        
        
    



