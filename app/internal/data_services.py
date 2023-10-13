import json
import os
import csv
import pandas as pd

def extract_json_content(s):
    s=s.strip()
    for i, char in enumerate(s):
        if char == "[":
            return s[i:s.rfind("]")+1]
        elif char == "{":
            return s[i:s.rfind("}")+1]
    return None


def create_demographic_csv(filename, columns=[
    "Gender Identity", "Age", "Date of Birth", "Marital Status", "Sexual Orientation", 
    "Nationality", "Country of Residence", "State/Province", "City",
    "Rural or Urban", "Type of Residence", "Length of Residence", "Level of Education", 
    "Field of Study", "Occupation", "Income Level", "Social Class", "Employment Status", 
    "Home Ownership", "Ethnicity", "Language(s) Spoken", "Religion", "Cultural Practices",
    "Immigration Status", "Hobbies and Interests", "Shopping Preferences", "Dietary Preferences", 
    "Physical Activity Levels", "Social Media Usage", "Travel Habits", "Alcohol and Tobacco Use", 
    "Technology Usage", "Family Structure", "Household Size", "Pet Ownership", 
    "Relationship Status", "Caregiving Responsibilities", "General Health Status", 
    "Disabilities or Chronic Illnesses", "Mental Health Status", "Health Insurance Status", 
    "Access to Healthcare", "Political Affiliation", "Voting Behavior", "Political Engagement"
]):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)

#modified to accomodate for new demgen data output structure (append key values in a single dictionary)
def append_demographic(filename, data):
    # Check if directory exists
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        return f"Error: The directory {directory} does not exist."

    # Get the column names from the CSV file
    with open(filename, 'r', newline='') as file:
        fieldnames = next(csv.reader(file))

    # Open the CSV file in append mode
    with open(filename, 'a', newline='') as file:
        # Create a DictWriter
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the data to the CSV file
        writer.writerow(data)

def append_response(filename, data):
    # Check if file exists
    if not os.path.exists(filename):
        return f"Error: No file named {filename} is found."

    # Prepare a dictionary to store the answers
    answer_dict = {}

    # Iterate over the response data
    for item in data:
        # Use the question as the key and the answer as the value
        question = item["question"]
        answer = item["answer"]
        answer_dict[question] = answer

    # Open the CSV file in read mode to get the column names
    with open(filename, 'r', newline='') as file:
        fieldnames = next(csv.reader(file))

    # Open the CSV file in append mode to write the data
    with open(filename, 'a', newline='') as file:
        # Create a DictWriter
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the data to the CSV file
        writer.writerow(answer_dict)



def clean_up_csv(filename):
    # Load the dataframe
    df = pd.read_csv(filename)

    # Remove unwanted characters
    df = df.replace(to_replace =["\[","\]","\'", ""], value ="", regex = True)

    # Save the cleaned dataframe
    df.to_csv(filename, index=False)

