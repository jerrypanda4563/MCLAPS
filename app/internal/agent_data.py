import openai.error
from app.internal import chunking
from app.internal.tokenizer import count_tokens
from app import settings
import time
import json


from sklearn.metrics.pairwise import cosine_similarity as cs
from openai import Embedding
import openai
import numpy as np
from typing import Dict, List, Optional
import pydantic
import uuid
import random
import spacy
from concurrent.futures import as_completed, ProcessPoolExecutor, ThreadPoolExecutor
import math
from app.api_clients.mclapsrl import mclapsrlClient


nlp = spacy.load("en_core_web_sm")
rate_limiter = mclapsrlClient()

openai.api_key = settings.OPEN_AI_KEY



class Chunk(pydantic.BaseModel):
    parent_DataStr_id: uuid.UUID
    Chunk_id: uuid.UUID
    index: int 
    DataStr_index: int 
    string: str 
    embedding_vector: np.ndarray 
    conjugate_vector: np.ndarray 
    
    class Config:
        arbitrary_types_allowed = True

    @pydantic.validator('embedding_vector', 'conjugate_vector')
    def check_numpy_array(cls, v):
        assert isinstance(v, np.ndarray), 'must be a numpy array'
        return v

    @pydantic.validator('parent_DataStr_id', 'Chunk_id')
    def check_uuid(cls, v):
        assert isinstance(v, uuid.UUID), 'must be a UUID'
        return v
    

class DataStr(pydantic.BaseModel):
    DataStr_id: uuid.UUID
    index: int
    string: str
    chunks: List[Chunk]
    embedding_vector: np.ndarray

    class Config:
        arbitrary_types_allowed = True

    @pydantic.validator('embedding_vector')
    def check_numpy_array(cls, v):
        assert isinstance(v, np.ndarray), 'must be a numpy array'
        return v

    @pydantic.validator('DataStr_id')
    def check_uuid(cls, v):
        assert isinstance(v, uuid.UUID), 'must be a UUID'
        return v
    

class AgentData:

    def __init__(self):
        self.DataStrings: List[DataStr] = []  
        self.DataChunks: List[Chunk] = []  
        self.memory_size: int = 5000       #####INCEASE FOR PRODUCTION
        self.conjugate_matrix: np.ndarray = np.array([[]]) 
        self.L2_conjugate_matrix: np.ndarray = np.array([[]]) 
        self.L2_diagnolized: np.ndarray = np.array([[]]) 

    #return none if embedding failed
    def embed_large_text(self, text: str, embedding_model: Optional[str] = "text-embedding-3-small") -> np.ndarray:
        while rate_limiter.model_status(embedding_model) == False:
            time.sleep(2)
            continue
        retries = 5
        while retries > 0:
            try:
                response=Embedding.create(
                    model = embedding_model,
                    input=str(text)
                    )
                rate_limiter.new_response(response)
                embedding = np.array(response['data'][0]['embedding'])
                return embedding
            except (openai.error.OpenAIError, openai.error.Timeout, openai.error.ServiceUnavailableError, openai.error.RateLimitError) as e:
                print(f"Error while embedding in agent data: {e}")
                retries -= 1
                time.sleep(5)
                continue
        

                
    def embed_text(self, text: str) -> np.ndarray:
        processed_text = nlp(text)
        embedding = np.array(processed_text.vector)
        return embedding
    
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

    def construct_matrices(self) -> None:
        if len(self.DataChunks) <= 1:
            pass
        else:
            self.conjugate_matrix = np.array([[]])
            self.conjugate_matrix = np.array([chunk.conjugate_vector for chunk in self.DataChunks])
            np.fill_diagonal(self.conjugate_matrix, 0) 
            self.L2_conjugate_matrix = self.conjugate_matrix/np.linalg.norm(self.conjugate_matrix, axis=1, keepdims=True)
            self.L2_diagnolized = np.diag(np.linalg.eig(self.L2_conjugate_matrix)[0])
    
    # def chunk_group_reconstruct(self, chunk: Chunk) -> str:
    #     #find a configuration of chunk sequence with the highest total similarity
    #     def generate_chunk_sequence(chunk:Chunk) -> List[Chunk]:
    #         #generate the configuration sequence of 10 chunks via greedy search
    #         initial_chunk=chunk
    #         sequence = [initial_chunk]
    #         for _ in range(9):
                
    #             next_chunk_index =  np.argmax(initial_chunk.conjugate_vector)
    #             if next_chunk_index == initial_chunk.index:
    #                 break
    #             else:
    #                 next_chunk = self.DataChunks[next_chunk_index]
    #                 sequence.append(next_chunk)
    #                 initial_chunk = next_chunk


    # CURRENTLY NOT IN USE DUE TO PERFORMANCE ISSUES
    def local_datastr_reconstruct(self, chunk: Chunk, query_string: str) -> str:
            
        parent_DataStr = [datastr for datastr in self.DataStrings if datastr.DataStr_id == chunk.parent_DataStr_id][0]
        if len(parent_DataStr.chunks) <= 10:
            return parent_DataStr.string
        
        query_embedding = self.embed_text(query_string)
        
        def annealer_reconstructor(target_chunk: Chunk, parent_DataStr: DataStr, query_embedding: np.ndarray) -> str:
            
            def generate_configuration(target_chunk: Chunk, datastr: DataStr) -> List[Chunk]:
                chunk_index = target_chunk.DataStr_index
                max_index = datastr.chunks[-1].DataStr_index  
                min_index = datastr.chunks[0].DataStr_index
                subset_length = math.ceil(0.1 * len(datastr.chunks))  


                offset = random.randint(0, subset_length)
                start_index = max(min_index, chunk_index - offset)
                end_index = min(max_index, start_index + subset_length)
                if chunk_index < start_index:
                    start_index = chunk_index
                if chunk_index > end_index:
                    end_index = chunk_index

                indices = list(range(start_index, end_index+1))  

                configuration_subspace = [c for c in datastr.chunks if c.DataStr_index in indices]

                if len(configuration_subspace) != 0:
                    return configuration_subspace
                elif target_chunk.DataStr_index != np.array([chunk.DataStr_index for chunk in configuration_subspace]).any():
                        raise ValueError('Target chunk is not in the configuration')
                else:
                    raise ValueError('Configuration subspace is empty')
                
            
            def generate_neighbor_state(init_config: List[Chunk], target_chunk: Chunk, datastr: DataStr) -> List[Chunk]:
                
                if len(init_config) == 0:
                    raise ValueError('Initial configuration is empty')
                
                if target_chunk.DataStr_index not in [chunk.DataStr_index for chunk in init_config]:
                    raise ValueError('Target chunk is not in the configuration')

                immutable_chunk = target_chunk
                parent_data_str = datastr
                config_0 = init_config.copy()
                actions = (1, -1, 0) 
                l_action = random.choice(actions)
                r_action = random.choice(actions)

                def left_action(action, config: List[Chunk], datastr: DataStr, target_chunk: Chunk) -> List[Chunk]:
                    config_modified = config.copy()
                    left_index = config_modified[0].DataStr_index
                    immutable_index = target_chunk.DataStr_index
                    if action == 1:
                        new_chunk_index = left_index - 1
                        if new_chunk_index >= 0:
                            config_modified.insert(0, datastr.chunks[new_chunk_index])
                        else:
                            pass
                    elif action == -1:
                        remove_index = left_index
                        if remove_index != immutable_index:
                            config_modified.pop(0)
                        else:
                            pass
                    return config_modified

                def right_action(action, config: List[Chunk], datastr: DataStr, target_chunk: Chunk) -> List[Chunk]:
                    config_modified = config.copy()
                    right_index = config_modified[-1].DataStr_index
                    immutable_index = target_chunk.DataStr_index
                    if action == 1:
                        new_chunk_index = right_index + 1
                        if new_chunk_index <= datastr.chunks[-1].DataStr_index - 1:
                            config_modified.append(datastr.chunks[new_chunk_index])
                        else:
                            pass
                    elif action == -1:
                        remove_index = right_index
                        if remove_index != immutable_index:
                            config_modified.pop(-1)
                        else:
                            pass
                    return config_modified

                config_1 = left_action(l_action, config_0, parent_data_str, immutable_chunk)
                config_2 = right_action(r_action, config_1, parent_data_str, immutable_chunk)
                if len(config_2) != 0:
                    return config_2
                else:
                    raise ValueError('Neighbor state is empty')
                
              

            def temperature(T0: float, a:float, t:float) -> float:
                T= T0 * (a**t)
                return T
            
            def metric_distance(config: List[Chunk], query_embedding: np.ndarray) -> float:
                string = ' '.join([chunk.string for chunk in config])
                distance = cs(self.embed_text(string).reshape(1,-1), query_embedding.reshape(1,-1))[0][0]
                return distance
            

           
            x = round(0.1*len(parent_DataStr.chunks)) 
            T_init: int = x 
            decay_rate: float = 1-1/x 
            timescale: int =  round(math.log(0.0001, decay_rate)) 
            
            current_config: List[Chunk] = generate_configuration(target_chunk, parent_DataStr)

            # distance_list: List[float]= []
            # length_list: List[int]= [sum([count_tokens(chunk.string) for chunk in current_config])]
           
            for t in range(timescale):

                new_config:List[Chunk] = generate_neighbor_state(current_config, target_chunk, parent_DataStr)
                distance_current = metric_distance(current_config, query_embedding)
                distance_new = metric_distance(new_config, query_embedding)

                P_distance= np.exp(-(distance_current - distance_new)/temperature(T_init, decay_rate, t))
                P_length = np.exp(-(((len(new_config) - len(current_config))+2)/4)/temperature(T_init, decay_rate, t))   ##rescaled for -2 to 2 to 0 to 1
                P = (P_distance+0.1*P_length)/2 
                if random.uniform (0,1) < P:
                    current_config = new_config
                    # distance_list.append(distance_new)
                    # length_list.append(sum([count_tokens(chunk.string) for chunk in current_config]))
                else:
                    current_config = current_config
                    # distance_list.append(distance_current)
                    # length_list.append(sum([count_tokens(chunk.string) for chunk in current_config]))
            
            reconstructed_string = ' '.join([chunk.string for chunk in current_config])
            
            # distance_list_normalized = [(distance-min(distance_list))/(max(distance_list)-min(distance_list)) for distance in distance_list]
            # length_list_normalized = [(length-min(length_list))/(max(length_list)-min(length_list)) for length in length_list]
            # plt.plot(distance_list_normalized)
            # plt.plot(length_list_normalized)
            # plt.show()
    
            return reconstructed_string
        
        if len(parent_DataStr.chunks) <=10:
            return parent_DataStr.string
        else:
            composed_string = annealer_reconstructor(chunk, parent_DataStr, query_embedding)
            return composed_string
        
    #quick check to see if there is anything more related in database
    def L0_query(self, query_string:str) -> Optional[List[int]]:
        if len(self.DataChunks) == 0:
            pass
        else:
            try:
                query_embedding = self.embed_large_text(query_string)
                query_conjugate_vector = self.compute_conjugate_vector(query_embedding)
                top_5: List[int] = sorted(query_conjugate_vector.tolist(),reverse=True)[0:5]
                return top_5
            except Exception as e:
                print(f"Error in L0 query: {e}")
                return None
            
    def L1_query(self, query_string:str) -> List[str]:
        
        if len(self.DataChunks) == 0:
            return None
        else:
            try:
                
                query_embedding = self.embed_large_text(query_string)
                query_conjugate_vector = self.compute_conjugate_vector(query_embedding)
                top_5 = sorted(enumerate(query_conjugate_vector.tolist()), key=lambda x: x[1], reverse=True)[0:5]
                target_chunk_list = [self.DataChunks[index] for index, _ in top_5]
                
                reconstructed_strings = []
                with ProcessPoolExecutor(max_workers=len(target_chunk_list)) as executor:
                    futures = {executor.submit(self.local_datastr_reconstruct, target_chunk, query_string) for target_chunk in target_chunk_list}
                    for future in as_completed(futures):
                        reconstructed_strings.append(future.result())
                return reconstructed_strings
            
            except Exception as e:
                print(f"Error in L1 query: {e}")
                return None


    def fast_query(self, query_string: str) -> List[str]:
        def chunk_group_reconstruct( chunk: Chunk) -> str:
            top_5 = sorted(enumerate(chunk.conjugate_vector.tolist()), key=lambda x: x[1], reverse=True)[0:5]
            target_chunk_list = [self.DataChunks[index] for index, _ in top_5]
            string_group = "\n".join([chunk.string for chunk in target_chunk_list])
            return string_group
        if len(self.DataChunks) == 0:
            return None
        else:
            try:
                query_embedding = self.embed_large_text(query_string)
                query_conjugate_vector = self.compute_conjugate_vector(query_embedding)
                top_5 = sorted(enumerate(query_conjugate_vector.tolist()), key=lambda x: x[1], reverse=True)[0:5]
                target_chunk_list = [self.DataChunks[index] for index, _ in top_5]
                reconstructed_strings = []
                for target_chunk in target_chunk_list:
                    reconstructed_strings.append(chunk_group_reconstruct(target_chunk))
                return reconstructed_strings
            except Exception as e:
                print(f"Error in fast query: {e}")
                return None



    def add_data_str(self, input_string: str):

        def add_chunk(datastr_index: int, parent_str_id: str, input_string: str, input_string_embedding: np.ndarray) -> Chunk:
        
            chunk = Chunk(
                parent_DataStr_id = parent_str_id,
                Chunk_id=uuid.uuid4(),
                index=len(self.DataChunks),
                DataStr_index = datastr_index,
                string=input_string,
                embedding_vector=input_string_embedding,
                conjugate_vector=np.array([])
            )
            self.DataChunks.append(chunk)
            conjugate_vector = self.compute_conjugate_vector(chunk.embedding_vector)
            chunk.conjugate_vector = conjugate_vector
            self.update_conjugate_vectors(chunk)
            self.construct_matrices()

            return chunk
        
        try:
            datastr = input_string
            datastr_embedding = self.embed_large_text(input_string)
            datastr_uuid = uuid.uuid4()
            datastr_chunked = chunking.chunk_string(input_string)
            
            
            list_of_chunk_embeddings: List[np.ndarray] = []
            with ThreadPoolExecutor(max_workers=len(datastr_chunked)) as executor:
                list_of_chunk_embeddings = list(executor.map(self.embed_large_text, datastr_chunked))


            list_of_chunks: List[Chunk] = []    
            for string, embedding in zip(datastr_chunked, list_of_chunk_embeddings):
                data_chunk = add_chunk(datastr_index= len(list_of_chunks) , parent_str_id = datastr_uuid, input_string = string, input_string_embedding = embedding)
                list_of_chunks.append(data_chunk)
            
            data_str = DataStr(
                DataStr_id = datastr_uuid,
                index = len(self.DataStrings),
                chunks = list_of_chunks,
                string = datastr,
                embedding_vector = datastr_embedding
            )
            self.DataStrings.append(data_str)
            
            return data_str
        except Exception as e:
            print(f"Error in adding data string: {e}")
            return None
        
    def query(self, input_string: str, evalutator_k: Optional[float] = 0):
        if len(self.DataChunks) == 0:
            return None
        else:
            relatedness = self.L0_query(input_string)[0]
            if relatedness >= evalutator_k:
                return self.fast_query(input_string)
            else:
                return None

        
    

            
            
            




    
 






    

    

