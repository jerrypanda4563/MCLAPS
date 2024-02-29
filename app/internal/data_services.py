import json
import os
import csv
import pandas as pd
from app.redis_config import cache
from typing import Dict, List

def extract_json_content(s):
    s=s.strip()
    for i, char in enumerate(s):
        if char == "[":
            return s[i:s.rfind("]")+1]
        elif char == "{":
            return s[i:s.rfind("}")+1]
    return None

def clean_up_csv(filename):
    # Load the dataframe
    df = pd.read_csv(filename)

    # Remove unwanted characters
    df = df.replace(to_replace =["\[","\]","\'", ""], value ="", regex = True)

    # Save the cleaned dataframe
    df.to_csv(filename, index=False)

def create_csv_from_simulation_results(sim_data: Dict, file_path= "./simulations"):
    # Extract the survey name and simulation results
    data=sim_data
    survey_id = data.get("_id", "Survey")
    simulation_results = data.get('Simulation Result', [])

    # File name using the survey_id
    file_name = f"{file_path}/{survey_id}_Simulation_Results.csv"

    # Open a file to write
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write headers
        headers_written = False
        for result in simulation_results:
            # Load the JSON string
            result_data = result

            # Extract response data
            response_data = result_data.get('response_data', [])
            demographic_data = result_data.get('demographic_data', {})

            # Combine response and demographic data
            combined_data = {**demographic_data}
            for response in response_data:
                key = response['question']
                answer = response.get('answer', 'N/A')
                combined_data[key] = answer

            # Write headers if not yet written
            if not headers_written:
                headers = list(combined_data.keys())
                writer.writerow(headers)
                headers_written = True

            # Write data
            writer.writerow(combined_data.values())

    return file_name



