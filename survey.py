import csv
import os
import json

class Survey():

    def __init__(self):
        self.questions=[]

    def add_short_answer_question(self, question):
        obj={
            "type":"short answer",
            "question":question,
            "answer":None
        }
        self.questions.append(obj)
    
    def add_long_answer_question(self, question):
        obj={
            "type":"long answer",
            "question":question,
            "answer":None
        }
        self.questions.append(obj)
    
    def add_multiple_choice_question(self, question, choices):
        obj={
            "type":"multiple choice",
            "question":question,
            "choices":choices,
            "answer":None
        }
        self.questions.append(obj)

    def add_checkboxes_question(self, question, choices):
        obj={
            "type":"checkboxes",
            "question":question,
            "choices":choices,
            "answer":None
        }
        self.questions.append(obj)


    def add_linear_scale_question(self, question, min_value, max_value):
        obj={
            "type":"linear scale",
            "question":question,
            "min_value":min_value,
            "max_value":max_value,
            "answer":None
        }
        self.questions.append(obj)

    def create_csv(self, filename):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            headers = [q["question"] for q in self.questions]
            writer.writerow(headers)
    
    def to_json(self):
        return json.dumps(self.questions)
    
    def show(self):
        return self.questions
    

