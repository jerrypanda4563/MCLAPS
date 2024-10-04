import openai.error
from app.internal import chunking

from app import settings
import time


from sklearn.metrics.pairwise import cosine_similarity as cs
from openai import Embedding
import openai
import numpy as np
from typing import Dict, List, Optional, Literal
import pydantic
import uuid
import random
import traceback
import spacy
from concurrent.futures import ThreadPoolExecutor
from app.api_clients.mclapsrl import mclapsrlClient


nlp = spacy.load("en_core_web_sm")
rate_limiter = mclapsrlClient()

openai.api_key = settings.OPEN_AI_KEY




    


    




class Chunk(pydantic.BaseModel):
    # parent_DataStr_id: uuid.UUID
    index: int 
    # DataStr_index: int 
    string: str 
    embedding_vector: np.ndarray 
    conjugate_vector: Optional[np.ndarray] = np.array([]) 
    
    class Config:
        arbitrary_types_allowed = True

    @pydantic.validator('embedding_vector', 'conjugate_vector', pre=True)
    def check_numpy_array(cls, v):
        if not isinstance(v, np.ndarray):
            return np.array(v)
        return v
    
    def compute_conjugate_vector(self, chunk_embeddings: List[np.ndarray]) -> np.ndarray:
        def isotropic_rescaler(value: float) -> float:
            rescaled_value = (value + 1)/2
            return rescaled_value
        
        embedding_vector_reshaped = self.embedding_vector.reshape(1, -1)
        chunk_embeddings_stacked = np.vstack(chunk_embeddings)
        similarities = cs(embedding_vector_reshaped, chunk_embeddings_stacked)
        conjugate_vector = similarities.flatten()
        rescaled_conjugate_vector = np.array([isotropic_rescaler(value) for value in conjugate_vector])
        return rescaled_conjugate_vector

# #####################
# class DataStr(pydantic.BaseModel):
#     DataStr_id: uuid.UUID
#     index: int
#     string: str
#     chunks: List[Chunk]
#     embedding_vector: np.ndarray

#     class Config:
#         arbitrary_types_allowed = True

#     @pydantic.validator('embedding_vector')
#     def check_numpy_array(cls, v):
#         assert isinstance(v, np.ndarray), 'must be a numpy array'
#         return v

#     @pydantic.validator('DataStr_id')
#     def check_uuid(cls, v):
#         assert isinstance(v, uuid.UUID), 'must be a UUID'
#         return v
    


class AgentData:
    #max_memory_size as a initialization param
    def __init__(self, 
                 memory_limit: int, 
                 chunk_size: int, 
                 sampling_top_n: int, 
                 reconstruction_top_n: int, 
                 reconstruction_trigger_factor: float, 
                 memory_loss_factor: Optional[float] = 0.1, 
                 embedding_dim: Optional[int] = 512,
                 embedding_model: Literal["text-embedding-3-small", "text-embedding-3-large"] = "text-embedding-3-small"):  
        
        # self.DataStrings: List[DataStr] = []  
        self.DataChunks: List[Chunk] = [] 
        self.embedding_model: str = embedding_model 


        self.memory_size: int = memory_limit       #####INCEASE FOR PRODUCTION, unit is number of chunks
        self.chunk_size: int = chunk_size    ####unit in number of tokens
        self.query_sampling_n: int = sampling_top_n
        self.reconstruction_sampling_n: int = reconstruction_top_n
        self.reconstruction_trigger_length: int = round(reconstruction_trigger_factor * memory_limit)  #in n. of chunks
        self.loss_factor: float = memory_loss_factor ############!!!!!!!!!!!!!!!!!!!not a param yet
        self.dimension: int = embedding_dim############!!!!!!!!!!!!!!!!!!!not a param yet

    #return none if embedding failed
    def embed_large_text(self, text: str) -> np.ndarray:
        
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
            continue
        retries = 5
        while retries > 0:
            try:
                response=Embedding.create(
                    model = self.embedding_model,
                    input=str(text)
                    )
                rate_limiter.new_response(response)
                embedding = np.array(normalize_l2(response['data'][0]['embedding'][:self.dimension]))
                return embedding
            except (openai.error.OpenAIError, openai.error.Timeout, openai.error.ServiceUnavailableError, openai.error.RateLimitError) as e:
                print(f"Error while embedding in agent data: {e}")
                traceback.print_exc()
                retries -= 1
                time.sleep(5)
                continue
        else: 
            print(f"Failed to embed text: {text}")
            traceback.print_exc()
            return np.zeros(self.dimension) 
        
    def isotropic_rescaler(self, value: float) -> float:
        rescaled_value = (value + 1)/2
        return rescaled_value
    
    def compute_conjugate_vector(self, embedding_vector: np.ndarray) -> np.ndarray:
        embedding_vector_reshaped = embedding_vector.reshape(1, -1)
        chunk_embeddings = np.vstack([chunk.embedding_vector for chunk in self.DataChunks])
        similarities = cs(embedding_vector_reshaped, chunk_embeddings)
        conjugate_vector = similarities.flatten()
        rescaled_conjugate_vector = np.array([self.isotropic_rescaler(value) for value in conjugate_vector])
        return rescaled_conjugate_vector

    def update_conjugate_vectors(self, new_chunk: Chunk) -> None:
        for chunk in self.DataChunks[:-1]:
            chunk.conjugate_vector = np.append(chunk.conjugate_vector, new_chunk.conjugate_vector[chunk.index])


    #quick check to see if there is anything more related in database
    def L0_query(self, query_string:str) -> Optional[List[int]]:
        if len(self.DataChunks) == 0:
            return [0]
        else:
            try:
                query_embedding = self.embed_large_text(query_string)
                query_conjugate_vector = self.compute_conjugate_vector(query_embedding)
                top_1: List[int] = sorted(query_conjugate_vector.tolist(),reverse=True)[0:1]
                return top_1
            except Exception as e:
                print(f"Error in L0 query: {e}")
                return [0]
            
    #returns 5 strings, each string has six chunks 6 chunks, each chunk 20 tokens
    def fast_query(self, query_string: str) -> list[str]:
        #returns 5 most related chunks to the target chunk, sorting through conjugate vector
        def chunk_group_reconstruct(chunk: Chunk) -> str:
            top_n = sorted(enumerate(chunk.conjugate_vector.tolist()), key=lambda x: x[1], reverse=True)[0:self.reconstruction_sampling_n]
            target_chunk_list = [self.DataChunks[index] for index, _ in top_n]
            string_group = "\n".join([chunk.string for chunk in target_chunk_list])
            return string_group
        
        if len(self.DataChunks) == 0:
            return []
        
        else:
            try:
                query_embedding = self.embed_large_text(query_string)
                query_conjugate_vector = self.compute_conjugate_vector(query_embedding)
                top_n = sorted(enumerate(query_conjugate_vector.tolist()), key=lambda x: x[1], reverse=True)[0:self.query_sampling_n]    ###top 5 chunks identified through query similarity
                target_chunk_list = [self.DataChunks[index] for index, _ in top_n]
                if len(self.DataChunks) > self.reconstruction_trigger_length:
                    reconstructed_strings = []
                    for target_chunk in target_chunk_list:
                        reconstructed_strings.append(chunk_group_reconstruct(target_chunk))
                    return reconstructed_strings
                else: 
                    return target_chunk_list    
                
            except Exception as e:
                print(f"Error in fast query: {e}")
                return []

    def resturcture_memory(self):
        try:
            if len(self.DataChunks) >= self.memory_size: 
                chunk_average_similarities = [np.mean(chunk.conjugate_vector) for chunk in self.DataChunks]
                least_relevant_chunk_indices = sorted(enumerate(chunk_average_similarities), key=lambda x: x[1])[0:round(self.loss_factor * len(self.DataChunks))]
                for index in least_relevant_chunk_indices:
                    del self.DataChunks[index]
                # delete chunks and update conjugate vectors
                for chunk in self.DataChunks:
                    chunk.conjugate_vector = np.delete(chunk.conjugate_vector, least_relevant_chunk_indices)
                    chunk.index = self.DataChunks.index(chunk)
            else:
                pass
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error in restructuring memory in agent_data: {e}")


    ####add in logic for deleting old chunks, restruturing existing chunks and restructuring of relational matrix once max chunk size is hit
    def add_data_str(self, input_string: str):

        def add_chunk(input_string: str, input_string_embedding: np.ndarray) -> Chunk:
        
            chunk = Chunk(
                index=len(self.DataChunks),
                string=input_string,
                embedding_vector=input_string_embedding
            )
            chunk.compute_conjugate_vector([existing_chunk.embedding_vector for existing_chunk in self.DataChunks])
            self.DataChunks.append(chunk)
            self.update_conjugate_vectors(chunk)

            return chunk
        
        
        try:
            # datastr = input_string
            # datastr_embedding = self.embed_large_text(input_string)
            # datastr_uuid = uuid.uuid4()
            # datastr_chunked = chunking.chunk_string(input_string, chunk_size = self.chunk_size)
            
            # list_of_chunk_embeddings: List[np.ndarray] = []
            # with ThreadPoolExecutor(max_workers=len(datastr_chunked)) as executor:
            #     list_of_chunk_embeddings = list(executor.map(self.embed_large_text, datastr_chunked))

            # list_of_chunks: List[Chunk] = []    
            # for string, embedding in zip(datastr_chunked, list_of_chunk_embeddings):
            #     data_chunk = add_chunk(datastr_index= len(list_of_chunks) , parent_str_id = datastr_uuid, input_string = string, input_string_embedding = embedding)
            #     list_of_chunks.append(data_chunk)
            
            # data_str = DataStr(
            #     DataStr_id = datastr_uuid,
            #     index = len(self.DataStrings),
            #     chunks = list_of_chunks,
            #     string = datastr,
            #     embedding_vector = datastr_embedding
            # )
            # self.DataStrings.append(data_str)

            list_of_chunked_str: List[str] = chunking.chunk_string(input_string, chunk_size = self.chunk_size)
            with ThreadPoolExecutor(max_workers=len(list_of_chunked_str)) as executor:
                list_of_chunk_embeddings: List[np.ndarray] = list(executor.map(self.embed_large_text, list_of_chunked_str))

            for string, embedding in zip(list_of_chunked_str, list_of_chunk_embeddings):
                new_chunk = add_chunk(string, embedding)
                self.DataChunks.append(new_chunk)

            self.resturcture_memory()
            
        except Exception as e:
            print(f"Error in adding string to agent data: {e}")
            traceback.print_exc()
            raise Exception(f"Error in add_str in agent_data: {e}")
        
        
    def query(self, input_string: str, evalutator_k: Optional[float] = 0):
        if len(self.DataChunks) == 0:
            return []
        else:
            relatedness = self.L0_query(input_string)[0]
            if relatedness >= evalutator_k:
                return self.fast_query(input_string)
            else:
                return []

        
    

            
            
            




    
 






    

    

