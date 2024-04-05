import time
from app.redis_config import cache
import uuid
from multiprocessing import Process, Event



#initialized in runner, which is a background task
class CounterProcess():
    def __init__(self, simulation_id):

        self.simulation_id = simulation_id
        
        self.embedding_token_limit: int = 10000000      
        self.chat_token_limit: int = 2000000  
        self.embedding_request_limit: int = 10000
        self.chat_request_limit: int = 10000

        self.counter_id = None

        self.stop_signal = Event()
        self.timer_thread = None


    def create_counter(self):
        self.counter_id = str(uuid.uuid4())+str(time.time())
        counter = {
            "embedding_tokens_available": self.embedding_token_limit, 
            "embedding_requests_available": self.embedding_request_limit,
            "chat_tokens_available": self.chat_token_limit, 
            "chat_requests_available": self.chat_request_limit,
            "chat_status": str(True),
            "embedding_status": str(True)
            }
        cache.hset(self.counter_id, mapping = counter)
    
    def create_reference(self):
        simulation_ref = {
            'simulation_id': self.simulation_id,
            'counter_id': self.counter_id,
            'embedding_tokens_used': 0,
            'embedding_requests_made': 0,
            'chat_input_tokens_used': 0,
            'chat_completion_tokens_used': 0,
            'chat_requests_made': 0
        }
        cache.hset(self.simulation_id, mapping = simulation_ref)
    
    def initiate(self):
        # Create the initial counter
        self.create_counter()  
        self.create_reference()
        
        def timer():
            last_counter_time = time.time()
            while not self.stop_signal.is_set():
                if time.time() - last_counter_time >= 60:
                    self.create_counter()
                    cache.hset(self.simulation_id, "counter_id", self.counter_id) ##updates simulation reference
                    last_counter_time = time.time()
                time.sleep(0.1)
                
        self.timer_process = Process(target=timer)
        self.timer_process.start()
        
    def stop_counter(self) -> dict:
        usage_data={k.decode('utf-8'): v.decode('utf-8') for k, v in cache.hgetall(self.simulation_id).items()}
        self.stop_signal.set()
        self.timer_process.join() 
        return usage_data
    
    def run(self):
        try:
            self.initiate()
            while not self.stop_signal.is_set():
                # Keep the process alive or perform other tasks
                time.sleep(1)
        finally:
            self.stop_counter()



if __name__ == "__main__":
    simulation_id = "your_simulation_id_here"
    counter = CounterProcess(simulation_id)
    counter.run()