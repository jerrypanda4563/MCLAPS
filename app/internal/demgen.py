import openai
import json
from typing import Dict

from app import settings

openai.api_key = settings.OPEN_AI_KEY

        


def generate_demographic(demo: Dict):
    prompt_data = {
        "Sex at Birth": demo["sex_at_brith"],
        "Gender Identity": demo["gender_identity"],
        "Age": demo["age"],
        "Marital Status": demo["marital_status"],
        "Sexual Orientation": demo["sexual_orientation"],
        "Nationality": demo["nationality"],
        "Country of Residence": demo["country_of_residence"],
        "State/Province": demo["state_province"],
        "City": demo["city"],
        "Rural or Urban": demo["rural_or_urban"],
        "Type of Residence": demo["type_of_residence"],
        "Length of Residence": demo["length_of_residence"],
        "Level of Education": demo["level_of_education"],
        "Student Status": demo["student_status"],
        "Field of Study": demo["field_of_study"],
        "Occupational Area": demo["occupational_area"],
        "Annual Income Level": demo["annual_income_level"],
        "Employment Status": demo["employment_status"],
        "Home Ownership": demo["home_ownership"],
        "Ethnicity": demo["ethnicity"],
        "Language(s) Spoken": demo["languages_spoken"],
        "Religion": demo["religion"],
        "Cultural Practices": demo["cultural_practices"],
        "Immigration Status": demo["immigration_status"],
        "Hobbies and Interests": demo["hobbies_and_interests"],
        "Shopping Preferences": demo["shopping_preferences"],
        "Dietary Preferences": demo["dietary_preferences"],
        "Physical Activity Levels": demo["physical_activity_levels"],
        "Social Media Usage": demo["social_media_usage"],
        "Travel Habits": demo["travel_habits"],
        "Alcohol and Tobacco Use": demo["alcohol_tobacco_use"],
        "Technology Usage": demo["technology_usage"],
        "Family Structure": demo["family_structure"],
        "Household Size": demo["household_size"],
        "Pet Ownership": demo["pet_ownership"],
        "Relationship Status": demo["relationship_status"],
        "Caregiving Responsibilities": demo["caregiving_responsibilities"],
        "General Health Status": demo["general_health_status"],
        "Disabilities or Chronic Illnesses": demo["disabilities_or_chronic_illnesses"],
        "Mental Health Status": demo["mental_health_status"],
        "Health Insurance Status": demo["health_insurance_status"],
        "Access to Healthcare": demo["access_to_healthcare"],
        "Political Affiliation": demo["political_affiliation"],
        "Voting Behavior": demo["voting_behavior"],
        "Political Engagement": demo["political_engagement"]
    }
    prompt = json.dumps({k: None for k in prompt_data.keys()})
    system_prompt = json.dumps({k: v for k, v in prompt_data.items() if v is not None})
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
             "content": "Create a demographic profile of an individuals in json format. The constrained parameters are:\n" + system_prompt + "\nReplace the constrained value with a value falling reasonably within the category."},
            {"role": "user",
             "content": prompt}
        ],
        temperature=1.3,
        max_tokens=1366,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    demographic_profile = response.choices[0].message.content
    return demographic_profile

# Testing notes: with the new prompt/system prompt structure, data form consistency is increased, but for the parameter constraints, they lose flexibility in creating more random ones falling withinn category.
# Solution: create structured selection types for each of the parameter in next iteration of MVP


