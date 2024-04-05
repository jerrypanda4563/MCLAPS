import time
import threading
from app.redis_config import cache
import uuid
from multiprocessing import Process, Event



#initialized in runner with the sim_id, and backward imported in child processes
class CounterFunctions():
    
    def __init__(self,simulation_id):

        self.simulation_id = simulation_id

        self.current_counter_id = None


    def new_response(self, response: dict):
        self.current_counter_id = str(cache.hget(self.simulation_id, "counter_id").decode('utf-8'))
        tokens_used = response.usage.total_tokens
        requests_made = 1
        if response.object == "list":
            cache.hincrby(self.current_counter_id, "embedding_tokens_available", -tokens_used)
            cache.hincrby(self.current_counter_id, "embedding_requests_available", -requests_made)
            cache.hincrby(self.simulation_id, "embedding_tokens_used", response.usage.prompt_tokens)
            cache.hincrby(self.simulation_id, "embedding_requests_made", 1)

            tokens_available = int(cache.hget(self.current_counter_id, "embedding_tokens_available").decode("utf-8"))
            requests_available = int(cache.hget(self.current_counter_id, "embedding_requests_available").decode("utf-8"))
            if tokens_available <= int(0.02*self.embedding_token_limit) or requests_available <= int(0.01*self.embedding_request_limit):
                cache.hset(self.current_counter_id, "embedding_status", str(False))
            
        if response.object == "chat.completion":
            cache.hincrby(self.current_counter_id, "chat_tokens_available", -tokens_used)
            cache.hincrby(self.current_counter_id, "chat_requests_available", -requests_made)
            cache.hincrby(self.simulation_id, "chat_input_tokens_used", response.usage.prompt_tokens)
            cache.hincrby(self.simulation_id, "chat_completion_tokens_used", response.usage.completion_tokens)
            cache.hincrby(self.simulation_id, "chat_requests_made", 1)

            tokens_available = int(cache.hget(self.current_counter_id, "chat_tokens_available").decode("utf-8"))
            requests_available = int(cache.hget(self.current_counter_id, "chat_requests_available").decode("utf-8"))
            if tokens_available <= int(0.02*self.chat_token_limit) or requests_available <= int(0.01*self.chat_request_limit):
                cache.hset(self.current_counter_id, "chat_status", str(False))

    def check_embedding_status(self) -> bool:
        self.current_counter_id = str(cache.hget(self.simulation_id, "counter_id").decode('utf-8'))
        status = str(cache.hget(self.current_counter_id, "embedding_status").decode("utf-8"))
        boolean_value = status == "True"
        return boolean_value
    def check_chat_status(self) -> bool:
        self.current_counter_id = str(cache.hget(self.simulation_id, "counter_id").decode('utf-8'))
        status = str(cache.hget(self.current_counter_id, "chat_status").decode("utf-8"))
        boolean_value = status == "True"
        return boolean_value





