from typing import List, Dict, Any
import json



##survey question payloads to construct:  input for all functions is the dict extracted from survey, output is a string
# short/long answer question prompts
# multiple choice question prompts
# checkbox question prompts 
# linear scale question prompts

answer_schema = {"answer": ""}

def short_answer_prompt(question: Dict[str, Any]) -> str:
    question_text: str = question["question"]
    question_payload = question_text + f"\n Your response must be a short answer."
    prompt_payload = question_payload + "\n JSON response schema:\n" + json.dumps(answer_schema)
    return prompt_payload



def long_answer_prompt(question: Dict[str, Any]) -> str:
    question_text: str = question["question"]
    question_payload = question_text + f"\n Your response must be a long answer."
    prompt_payload = question_payload + "\n JSON response schema:\n" + json.dumps(answer_schema)
    return prompt_payload

def ranking_prompt(question: Dict[str, Any]) -> str:
    question_text: str = question["question"]
    choices: List[str] = question["choices"]
    question_payload = question_text + "The choices are:\n" + "\n".join([f"{option}" for option in choices]) + "\n Your response must be a ranked list of the choices given."
    # question_payload = question_text + "\n" + "\n".join([f"Choice {i+1}: {option}" for i, option in enumerate(choices)]) + "\n Your response must be a ranking of the choices given."
    prompt_payload = question_payload + "\n JSON response schema:\n" + json.dumps(answer_schema)
    return prompt_payload

def multiple_choice_prompt(question: Dict[str, Any]) -> str:
    question_text: str = question["question"]
    choices: List[str] = question["choices"]
    question_payload = question_text + "The choices are:\n" + "\n".join([f"{option}" for option in choices]) + "\n Your response must be one of the choices given."
    # question_payload = question_text + "\n" + "\n".join([f"Choice {i+1}: {option}" for i, option in enumerate(choices)]) + "\n Your response must be one of the choices given."

    prompt_payload = question_payload + "\n JSON response schema:\n" + json.dumps(answer_schema)
    return prompt_payload


def checkbox_prompt(question: Dict[str, Any]) -> str:
    question_text: str = question["question"]
    choices: List[str] = question["choices"]
    question_payload = question_text + "The choices are:\n" + "\n".join([f"{option}" for option in choices]) + "\n Your response must be one or multiple choices from the choices given."
    # question_payload = question_text + "The choices are:\n" + "\n".join([f"Choice {i+1}: {option}" for i, option in enumerate(choices)]) + "\n Your response must be one or multiple choices from the choices given"
    prompt_payload = question_payload + "\n JSON response schema:\n" + json.dumps(answer_schema)
    return prompt_payload

def linear_scale_prompt(question: Dict[str, Any]) -> str:
    question_text: str = question["question"]
    min_value: int = question["min_value"]
    max_value: int = question["max_value"]
    question_payload = question_text + "\n" + f"Scale: {list(range(min_value, max_value))}" + "\n Your response must be a number on the scale given"
    prompt_payload = question_payload + "\n JSON response schema:\n" + json.dumps(answer_schema)
    return prompt_payload


def input_question( question: Dict) -> str:

    if question["type"] == "short answer":
        return short_answer_prompt(question)
    
    elif question["type"] == "long answer":
        return long_answer_prompt(question)

    elif question["type"] == "multiple choice":
        return multiple_choice_prompt(question)
        
    elif question["type"] == "checkboxes":
        return checkbox_prompt(question)
    
    elif question["type"] == "ranking":
        return ranking_prompt(question)
    
    elif question["type"] == "linear scale":
        return linear_scale_prompt(question)
    
    else:
        return str(question)

## agent initialization prompt: input is demographic parameters, initial world state/ instructions from survey body, output is a string
def initialization_prompt(demographic: Dict, persona: str) -> str: 
    demographic_information = '\n'.join([f"{k}: {v}" for k, v in demographic.items()])
    prompt_payload = f"You are not a helpful assistant. You are a person with the following identity:\n"+f"{demographic_information}\n\n" + f"Your self description is: \n {persona}" + "You must think and behave as this identity when responding to user queries."
    return prompt_payload

    
