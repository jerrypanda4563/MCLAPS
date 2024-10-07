from app.internal import agent_data
from app.internal.tokenizer import count_tokens
from app.api_clients.mclapsrl import mclapsrlClient
from app import settings
from app.internal import chunking
import random

import uuid
import time
import numpy as np

import spacy
from typing import List, Optional
import openai
from openai.error import OpenAIError, Timeout, ServiceUnavailableError, RateLimitError
from sklearn.metrics.pairwise import cosine_similarity as cs
from concurrent.futures import ThreadPoolExecutor
from app.data_models import AgentParameters

import gc

openai.api_key = settings.OPEN_AI_KEY


nlp = spacy.load("en_core_web_sm")      
rate_limiter = mclapsrlClient()


#### note to self: new data str is only added when injecting under satisfied conditions or when restructuring memory

class Agent:

    def __init__(self, instruction:str, params: AgentParameters):
        ######
        # self.agent_id = str(uuid.uuid4()) #unique id for agent
        ######
        self.lt_memory = agent_data.AgentData(
            memory_limit = params.memory_limit, 
            chunk_size = round(params.chunk_size/(params.reconstruction_top_n + 1)), 
            sampling_top_n = params.sampling_top_n, 
            reconstruction_top_n = params.reconstruction_top_n, 
            reconstruction_trigger_factor = params.reconstruction_factor,
            embedding_dim = params.embedding_dimension,
            memory_loss_factor = params.memory_loss_factor
            )
        
        self.st_memory: list[str] = []
        self.instruction:str = instruction
        self.lt_memory_chunk_size = round(params.chunk_size/(params.reconstruction_top_n + 1))

       

        self.st_memory_capacity: int = params.memory_context_length
        self.max_output_length: int = params.max_output_length
        self.lt_memory_trigger_length: int = params.lt_memory_trigger_length   # n. of tokens in string required to force trigger lt_memory storage rather than st_memory
        self.memory_chunk_size: int = params.chunk_size
        self.memory_limit: int = params.memory_limit
        self.embedding_dimension: int = params.embedding_dimension

        self.llm_model = params.agent_model
        self.embedding_model = params.embedding_model
        self.model_temperature = params.llm_temperature
        self.agent_temperature = params.agent_temperature    # for query randomness
        self.json_mode = params.json_mode
        self.existence_date = params.existance_date
    

    #add limiter
    def embed(self, string:str) -> np.ndarray:

        def normalize_l2(x):
            x = np.array(x)
            if x.ndim == 1:
                norm = np.linalg.norm(x)
                if norm == 0:
                    return x
                return x / norm
            else:
                norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
                return np.where(norm == 0, x, x / norm)
            
        while rate_limiter.model_status(self.embedding_model) == False:
            time.sleep(2)
        retries = 5
        while retries > 0:
            try:
                response=openai.Embedding.create(
                    model = self.embedding_model,
                    input=str(string)
                    )

                rate_limiter.new_response(response)
                embedding = np.array(normalize_l2(response['data'][0]['embedding'][:self.embedding_dimension]))
                return embedding
            except (OpenAIError, Timeout, ServiceUnavailableError, RateLimitError) as e:
                print(f"Error while embedding in response agent: {e}")
                retries -= 1
                time.sleep(5)
                continue
            # except RateLimitError as e:
            #     print(f"Rate limit error serverside: {e}")
            #     rate_limiter.
            #     time.sleep(5)
        else:
            print(f"Warning: zero vector returned for string {string}")
            return np.zeros(self.embedding_dimension)
            
        

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
                return 1  # if fails, always stick with the current memory since max k is 1
        
    def st_memory_length(self) -> int:
        return count_tokens(' '.join(self.st_memory))
    
    def debug_st_memory(self) -> None:
        for i, memory_object in enumerate(self.st_memory):
            if type(memory_object) != str:
                print(f"Memory object is not string: {memory_object}")
                raise ValueError(f"Memory object index number {i} is not a string.")
            
    
    ################
    #can potentially be added with random generation of memory based on initialization data
    def random_memory(self) -> list[str]:
        
        trigger_value = random.random()
        if trigger_value < self.agent_temperature:
            return []
        else:
            if len(self.lt_memory.DataChunks) == 0:
                return []

            else:
                sampled_chunk: agent_data.Chunk = random.choice(self.lt_memory.DataChunks)
                related_chunk_indices = sorted(enumerate(sampled_chunk.conjugate_vector.tolist()), key=lambda x: x[1], reverse=True)[0:round(self.memory_chunk_size/self.lt_memory_chunk_size)]
                related_chunks = [self.lt_memory.DataChunks[index] for index, _ in related_chunk_indices]
                related_strings = [chunk.string for chunk in related_chunks]
                memory_chunks = related_strings.extend([sampled_chunk.string])
                return memory_chunks
        
    ###################


    

    def construct_st_memory(self, query_str: str) -> None:
        if random.random() < self.agent_temperature:
            random_memory = self.random_memory()
        else:
            random_memory = []
        
        current_memory = self.st_memory.copy()
        if len(self.st_memory) == 0:
            queried_memory = self.lt_memory.query(query_str)
            self.st_memory =current_memory + queried_memory + random_memory
        else:
            #1-agent_temp/2 chance of querying memory
            if random.random() > self.agent_temperature/2:
                with ThreadPoolExecutor(max_workers=len(self.st_memory)) as executor:
                    similarity_scores = list(executor.map(lambda x: self.evaluator(query_str, x), self.st_memory))
                k = np.average(similarity_scores) #mean similarity to query
                queried_memory = self.lt_memory.query(query_str, k)
                self.st_memory = current_memory + queried_memory + random_memory
            else: 
                #generates random memory along with current memory, ignores query
                self.st_memory = current_memory + random_memory

        if self.st_memory_length() > self.st_memory_capacity:
            self.restructure_memory(string = query_str)
    
    
    #pop out strings with lowest similarity to query and add popped memory to lt_memory
    def restructure_memory(self, string:str) -> None:
        
        with ThreadPoolExecutor(max_workers=len(self.st_memory)) as executor:
            similarity_scores = list(executor.map(lambda x: self.evaluator(string, x), self.st_memory))

        new_lt_memory: list[str] = []
        while self.st_memory_length() > self.st_memory_capacity:
            index = similarity_scores.index(min(similarity_scores))
            forgotten_memory = self.st_memory.pop(index)
            similarity_scores.pop(index)
            new_lt_memory.append(forgotten_memory)
        new_lt_memory_joined = '\n'.join(new_lt_memory)
        self.lt_memory.add_data_str(new_lt_memory_joined)
            

    #add limiter
    def model_response(self, query: str) -> str:
        memory_prompt = "You recall the following pieces of information:\n" + '\n'.join(self.st_memory) 
        
        #json mode
        if self.json_mode == True:
            while rate_limiter.model_status(self.llm_model) == False:
                time.sleep(2)
            completion = openai.ChatCompletion.create(
                    model = self.llm_model,
                    response_format={"type": "json_object"},
                    messages=[
                            {"role": "system", "content": self.instruction + "\n" + memory_prompt + "\n" + f"The current date is {self.existence_date}"},
                            {"role": "user", "content": query},
                        ],
                    temperature=self.model_temperature,
                    max_tokens=self.max_output_length,
                    n=1  
                    )
 
            rate_limiter.new_response(completion)
            response = completion.choices[0].message.content
            return response
        
        #non-json mode
        else:
            while rate_limiter.model_status(self.llm_model) == False:
                time.sleep(2)
            completion=openai.ChatCompletion.create(
                    model = self.llm_model,
                    messages=[
                            {"role": "system", "content": self.instruction + "\n" + memory_prompt + "\n" + f"The current date is {self.existence_date}"},
                            {"role": "user", "content": query},
                        ],
                    temperature=self.model_temperature,
                    max_tokens=self.max_output_length,
                    n=1  
                    )
            rate_limiter.new_response(completion)
            response=completion.choices[0].message.content
            return response
    
    
    #interacted functions
    def chat(self, query:str) -> str:
        self.debug_st_memory()
        self.construct_st_memory(query)   #changes system message 
        response: str = self.model_response(query)
        resoponse_chunked: list[str] = chunking.chunk_string(response, chunk_size = self.memory_chunk_size)
        self.st_memory.extend(resoponse_chunked)
        if self.st_memory_length() > self.st_memory_capacity:
            self.restructure_memory(query)
        return response
    



    ####************ 
    def inject_memory(self, string: str) -> None:
        string_length: int = count_tokens(string)

        if string_length >= self.lt_memory_trigger_length:
            self.lt_memory.add_data_str(string)

        else:
            available_st_memory: int = self.st_memory_capacity - self.st_memory_length()
            if string_length > available_st_memory:
                self.lt_memory.add_data_str(string) ###directly addes the string chunked in AgentData
            else: 
                string_chunks: list[str] = chunking.chunk_string(string, chunk_size = self.memory_chunk_size) #chunk size to be larger for strings within st memory
                self.st_memory.extend(string_chunks)
                if self.st_memory_length() > self.st_memory_capacity:
                    self.restructure_memory(string)
                

                
            
        
        
    



