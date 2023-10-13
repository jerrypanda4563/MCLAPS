import numpy as np
import openai
import random
import pandas as pd
#import tiktoken
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

import settings

openai.api_key = settings.OPEN_AI_KEY


class VectorDataFrame:
    def __init__(self, dimension=1536):
        self.dimension = dimension
        self.data = [[] for _ in range(dimension)]
        self.latest_index = 0
        
    def add(self, vector, index=None):
        if len(vector) != self.dimension:
            raise ValueError(f"Vector dimension must be {self.dimension}")
        
        if index is None:
            index = self.latest_index
            self.latest_index += 1
        else:
            if index < 0 or index >= self.dimension:
                raise IndexError(f"Index out of range. Must be between 0 and {self.dimension - 1}")
            self.latest_index = max(self.latest_index, index + 1)
        
        self.data[index] = vector
    
    def delete(self, index):
        if index < 0 or index >= self.dimension:
            raise IndexError(f"Index out of range. Must be between 0 and {self.dimension - 1}")
        
        self.data[index] = []
    
    def query(self, input_vector):
        if len(input_vector) != self.dimension:
            raise ValueError(f"Input vector dimension must be {self.dimension}")
        
        similarity_scores = []
        
        for index, vector in enumerate(self.data):
            if vector:
                similarity_score = cosine_similarity([input_vector], [vector])[0][0]
                # Only consider scores greater than or equal to 0.2
                if similarity_score >= 0.2:
                    similarity_scores.append((index, similarity_score))
        
        # If all similarity scores are below 0.2, return an empty list
        if not similarity_scores:
            return []

        # Sort and get the top 5 similar vectors
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [index for index, _ in similarity_scores[:5] if self.data[index]]
        
        return top_indices
        
    def query_recent(self):
        recent_entries = [index for index, vector in enumerate(self.data[self.latest_index - 1::-1]) if vector]
        return recent_entries[:2]     


class StringDataFrame:
    def __init__(self):
        self.data = []
        
    def add(self, string):
        self.data.append(string)
    
    def delete(self, index):
        if 0 <= index < len(self.data):
            del self.data[index]
        else:
            raise IndexError(f"Index out of range. Must be between 0 and {len(self.data) - 1}")
    def query(self, indices, separator="\n"):
        result = [self.data[index] for index in indices if 0 <= index < len(self.data) and self.data[index] is not None]
        return separator.join(result)


class Agent:
        
    def __init__(self,character):
        self.string_db = StringDataFrame()  # Initialize String database
        self.vector_db = VectorDataFrame()  # Initialize Vector database
        self.memory = ""
        self.prompt = ""
        self.character=character
    
    def embed(self,string):
        response=openai.Embedding.create(
          model="text-embedding-ada-002",
          input=str(string)
        )
        embedding = response['data'][0]['embedding']
        return embedding
    
    #retrieve strings and vector similarity search merged into one function
    def semantic_search(self, vector):
        # Query the vector database using the VectorDataFrame class for similar vector embeddings
        top_indices = self.vector_db.query(vector)
        recent_indices = self.vector_db.query_recent()
        indices=top_indices+recent_indices
        retrieved_strings = self.string_db.query(indices)
        return retrieved_strings
    
    
    def create_memory(self, retrieved_strings):
        self.memory = " ".join(retrieved_strings)
    
    def create_input_prompt(self):
        input_prompt =  self.prompt  #memory removed from user prompt into system prompt
        return input_prompt
    
    def generate_response(self, input_prompt):
        completion=openai.ChatCompletion.create(
                  model="gpt-3.5-turbo-16k",
                  messages=[
                        {"role": "system", "content": self.character+"\nContextual memory:"+self.memory},
                        {"role": "user", "content":input_prompt},
                    ],
                  temperature=1,
                  max_tokens=1024,
                  n=1  
                )
        response=completion.choices[0].message.content
        return response
    
    def inject_memory(self, string):
        self.string_db.add(string)
        embedded_string = self.embed(string)
        self.vector_db.add(embedded_string)
    
    def chat(self, prompt):
        self.prompt = prompt
        
        #semantic search
        embedded_prompt = self.embed(prompt)
        memory = self.semantic_search(embedded_prompt)
        self.create_memory(memory)
        
        #LLM call
        input = self.create_input_prompt()
        response = self.generate_response(input_prompt=input)
        
        #Creating long-term memory
        new_string = response  #prompt removed from memory creation
        self.string_db.add(new_string)
        
        embedded_string = self.embed(new_string)
        self.vector_db.add(embedded_string)
        
        return response


#test code comments: modification complete without any bugs, memory capacity increased to 5 prior response plus 2 most recent
#hotel_a = {
#    "name": "London Luxury Hotel",
#    "location": "London, UK",
#    "address": "123 Main Street, London",
#    "phone": "+44 20 1234 5678",
#    "email": "info@londonluxuryhotel.com",
#    "website": "https://www.londonluxuryhotel.com",
#    "rating": 4.5,
#    "wifi": True,
#    "gym": True,
#    "pool": False,
#    "restaurant": True,
#    "room_types": ["Single", "Double", "Suite"],
#    "room_rates": [100, 150, 250],
#    "description": "The London Luxury Hotel offers premium accommodation in the heart of London, with luxurious amenities and excellent service. Our hotel features a fully-equipped gym, a fine-dining restaurant, and spacious rooms with high-speed WiFi and comfortable bedding. Whether you're here for business or pleasure, the London Luxury Hotel is the perfect choice for your stay in London."
#}

#hotel_a_list = [(key, value) for key, value in hotel_a.items()]
#testbot=Agent("hotel conceirge")
#for i in hotel_a_list:
#    testbot.inject_memory(str(i))
#testbot.chat("where is the hotel")
#testbot.chat("Whats the address?")
#testbot.chat("amenities?")
# testbot.chat("I have a complaint")
# testbot.chat("I dont have wifi")
# testbot.chat("can you give me the password")
# testbot.chat("fine, i want to take a dip in the pool")
# testbot.chat("fuck you")
# print("Hi Simon \n How are you today")