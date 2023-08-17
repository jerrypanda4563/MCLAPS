import numpy as np
import openai
import random
import pandas as pd
import os
import csv
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

with open("OPEN_AI_KEY.txt", "r") as file:
    openai.api_key = file.readline().strip()


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
                similarity_scores.append((index, similarity_score))
        
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        top_2_indices = [index for index, _ in similarity_scores[:2] if self.data[index]]
        
        return top_2_indices
    
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
        self.string_db = StringDataFrame()  # String database
        self.vector_db = VectorDataFrame()  # Vector database
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
    
    def semantic_search(self, vector):
        # Query the vector database using the VectorDataFrame class for similar vector embeddings
        top_indices = self.vector_db.query(vector)
        return top_indices
    
    def retrieve_strings(self, indices):
        # Query the string database using the StringDataFrame class for strings with given indices
        retrieved_strings = self.string_db.query(indices)
        return retrieved_strings
    
    def create_memory(self, retrieved_strings):
        self.memory = " ".join(retrieved_strings)
    
    def create_input_prompt(self):
        input_prompt = self.memory + "\n" + self.prompt
        return input_prompt
    
    def generate_response(self, input_prompt):
        completion=openai.ChatCompletion.create(
                  model="gpt-4",
                  messages=[
                        {"role": "system", "content": self.character},
                        {"role": "user", "content":input_prompt},
                    ],
                  temperature=1.2,
                  max_tokens=4096,
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
        top_indices = self.semantic_search(embedded_prompt)
        retrieved_strings = self.retrieve_strings(top_indices)
        self.create_memory(retrieved_strings)
        
        #LLM call
        input_prompt = self.create_input_prompt()
        response = self.generate_response(input_prompt)
        
        #Creating long-term memory
        new_string = prompt + "\n" + response
        self.string_db.add(new_string)
        
        embedded_string = self.embed(new_string)
        self.vector_db.add(embedded_string)
        
        return response

