import time
import threading





#for chat model = gpt-3.5-turbo-0125 and embedding model text-embedding-3-small/ large/ ada2
class OpenAIUsageMonitor():
    
    def __init__(self):
        

        #defining limits per minute
        self.embedding_token_limit: int = 10000000   
        self.chat_token_limit: int = 2000000   
        self.embedding_request_limit: int = 10000
        self.chat_request_limit: int = 10000

        #aggregate tokens and requests
        self.total_embedding_tokens: int = 0
        self.total_chat_tokens: int = 0
        self.total_embedding_requests: int = 0
        self.total_chat_requests: int = 0

        #token counters
        self.embedding_tokens_used: int = 0
        self.chat_tokens_used: int = 0

        #request counters
        self.embedding_requests: int = 0
        self.chat_requests: int = 0


        self.start_time = time.time()
        self.stop_signal = threading.Event()
        self.timer_thread = None


    def initiate_counter(self):
        def timer():
            while not self.stop_signal.is_set():
                elapsed_time = time.time() - self.start_time
                if elapsed_time >= 60:
                    #reset timer
                    self.start_time = time.time()
                    
                    #updating aggregate values
                    self.total_embedding_tokens += self.embedding_tokens_used
                    self.total_chat_tokens += self.chat_tokens_used
                    self.total_embedding_requests += self.embedding_requests
                    self.total_chat_requests += self.chat_requests

                    #resetting counters
                    self.embedding_tokens_used = 0
                    self.chat_tokens_used = 0
                    self.embedding_requests = 0
                    self.chat_requests = 0
                
                time.sleep(0.1)
        self.timer_thread = threading.Thread(target=timer, daemon=True)
        self.timer_thread.start()
    
    def stop_counter(self):
        self.stop_signal.set()  # Signal the thread to stop
        self.timer_thread.join()  # Wait for the thread to actually stop

    def check_time(self):
        reset_time = 60 - (time.time() - self.start_time)
        return reset_time
    
    def check_chat_status(self) -> bool:
        if self.chat_tokens_used >= round(0.98*self.chat_token_limit):
            return False
        if self.chat_requests >= round(0.98*self.chat_request_limit):
            return False
        return True
    

    def check_embedding_status(self) -> bool:
        if self.embedding_tokens_used >= round(0.98*self.embedding_token_limit):
            return False
        if self.embedding_requests >= round(0.98*self.embedding_request_limit):
            return False
        return True


    def new_response(self, response: dict): 
        if response.object == "list":
            self.embedding_requests += 1
            self.embedding_tokens_used += response.usage.total_tokens
            return {"type": "embedding", "tokens_used": self.embedding_tokens_used, "requests_made": self.embedding_requests}


        if response.object == "chat.completion":
            self.chat_requests += 1
            self.chat_tokens_used += response.usage.total_tokens
            return {"type": "chat", "tokens_used": self.chat_tokens_used, "requests_made": self.chat_requests}

    def check_embedding_usage(self) -> dict:
        return{"total_embedding_tokens": self.total_embedding_tokens, "total_embedding_requests": self.total_embedding_requests}
    
    def check_chat_usage(self) -> dict:
        return{"total_chat_tokens": self.total_chat_tokens, "total_chat_requests": self.total_chat_requests}
        

        
limiter=OpenAIUsageMonitor()









