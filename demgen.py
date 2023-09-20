import openai
import json
with open("OPEN_AI_KEY.txt", "r") as file:
    openai.api_key = file.readline().strip()

def generate_demographic(gender_identity=None, age=None, date_of_birth=None,
                         marital_status=None, sexual_orientation=None, nationality=None,
                         country_of_residence=None, state_province=None, city=None,
                         rural_or_urban=None, type_of_residence=None, length_of_residence=None,
                         level_of_education=None, field_of_study=None, occupation=None, income_level=None,
                         social_class=None, employment_status=None, home_ownership=None, ethnicity=None,
                         languages_spoken=None, religion=None, cultural_practices=None,
                         immigration_status=None, hobbies_and_interests=None, shopping_preferences=None,
                         dietary_preferences=None, physical_activity_levels=None, social_media_usage=None,
                         travel_habits=None, alcohol_tobacco_use=None, technology_usage=None,
                         family_structure=None, household_size=None, pet_ownership=None,
                         relationship_status=None, caregiving_responsibilities=None,
                         general_health_status=None, disabilities_or_chronic_illnesses=None,
                         mental_health_status=None, health_insurance_status=None,
                         access_to_healthcare=None, political_affiliation=None, voting_behavior=None,
                         political_engagement=None):

    prompt_data =  {
        "Gender Identity": gender_identity,
        "Age": age,
        "Date of Birth": date_of_birth,
        "Marital Status": marital_status,
        "Sexual Orientation": sexual_orientation,
        "Nationality": nationality,
        "Country of Residence": country_of_residence,
        "State/Province": state_province,
        "City": city,
        "Rural or Urban": rural_or_urban,
        "Type of Residence": type_of_residence,
        "Length of Residence": length_of_residence,
        "Level of Education": level_of_education,
        "Field of Study": field_of_study,
        "Occupation": occupation,
        "Income Level": income_level,
        "Social Class": social_class,
        "Employment Status": employment_status,
        "Home Ownership": home_ownership,
        "Ethnicity": ethnicity,
        "Language(s) Spoken": languages_spoken,
        "Religion": religion,
        "Cultural Practices": cultural_practices,
        "Immigration Status": immigration_status,
        "Hobbies and Interests": hobbies_and_interests,
        "Shopping Preferences": shopping_preferences,
        "Dietary Preferences": dietary_preferences,
        "Physical Activity Levels": physical_activity_levels,
        "Social Media Usage": social_media_usage,
        "Travel Habits": travel_habits,
        "Alcohol and Tobacco Use": alcohol_tobacco_use,
        "Technology Usage": technology_usage,
        "Family Structure": family_structure,
        "Household Size": household_size,
        "Pet Ownership": pet_ownership,
        "Relationship Status": relationship_status,
        "Caregiving Responsibilities": caregiving_responsibilities,
        "General Health Status": general_health_status,
        "Disabilities or Chronic Illnesses": disabilities_or_chronic_illnesses,
        "Mental Health Status": mental_health_status,
        "Health Insurance Status": health_insurance_status,
        "Access to Healthcare": access_to_healthcare,
        "Political Affiliation": political_affiliation,
        "Voting Behavior": voting_behavior,
        "Political Engagement": political_engagement
    }

    prompt = json.dumps({k: None for k in prompt_data.keys()})
    system_prompt = json.dumps({k: v for k, v in prompt_data.items() if v is not None})
   
    # arguments = [
    #     gender_identity, age, date_of_birth, marital_status, sexual_orientation, nationality,
    #     country_of_residence, state_province, city, rural_or_urban, type_of_residence, length_of_residence,
    #     level_of_education, field_of_study, occupation, income_level, social_class, employment_status, home_ownership,
    #     ethnicity, languages_spoken, religion, cultural_practices, immigration_status, hobbies_and_interests,
    #     shopping_preferences, dietary_preferences, physical_activity_levels, social_media_usage, travel_habits,
    #     alcohol_tobacco_use, technology_usage, family_structure, household_size, pet_ownership, relationship_status,
    #     caregiving_responsibilities, general_health_status, disabilities_or_chronic_illnesses, mental_health_status,
    #     health_insurance_status, access_to_healthcare, political_affiliation, voting_behavior, political_engagement
    # ]
    #
    # num_parameters = sum(arg is not None for arg in arguments)
    # t_min = 1.25
    # t_max = 0.6
    # t = t_min + (t_max - t_min) * (num_parameters / len(arguments))

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role":"system", 
             "content": "Create a demographic profile by replacing null values for the undefined parameters in the json dictionary. The pre-defined constrained values are:\n" + system_prompt + "\nReplace the pre-defined constrained value with a value falling within the category. The output must contain the same json keys and have the same data structure as the input." },
            {"role": "user", 
             "content": prompt}
        ],
        temperature=1,
        max_tokens=1366,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    demographic_profile = response.choices[0].message.content
    return demographic_profile



# Testing notes: with the new prompt/system prompt structure, data form consistency is increased, but for the parameter constraints, they lose flexibility in creating more random ones falling withinn category.
# Solution: create structured selection types for each of the parameter in next iteration of MVP








# def prompt_test(gender_identity=None, age=None, date_of_birth=None,
#                          marital_status=None, sexual_orientation=None, nationality=None,
#                          country_of_residence=None, state_province=None, city=None,
#                          rural_or_urban=None, type_of_residence=None, length_of_residence=None,
#                          level_of_education=None, field_of_study=None, occupation=None, income_level=None,
#                          social_class=None, employment_status=None, home_ownership=None, ethnicity=None,
#                          languages_spoken=None, religion=None, cultural_practices=None,
#                          immigration_status=None, hobbies_and_interests=None, shopping_preferences=None,
#                          dietary_preferences=None, physical_activity_levels=None, social_media_usage=None,
#                          travel_habits=None, alcohol_tobacco_use=None, technology_usage=None,
#                          family_structure=None, household_size=None, pet_ownership=None,
#                          relationship_status=None, caregiving_responsibilities=None,
#                          general_health_status=None, disabilities_or_chronic_illnesses=None,
#                          mental_health_status=None, health_insurance_status=None,
#                          access_to_healthcare=None, political_affiliation=None, voting_behavior=None,
#                          political_engagement=None):

#     prompt_data =  {
#         "Gender Identity": gender_identity,
#         "Age": age,
#         "Date of Birth": date_of_birth,
#         "Marital Status": marital_status,
#         "Sexual Orientation": sexual_orientation,
#         "Nationality": nationality,
#         "Country of Residence": country_of_residence,
#         "State/Province": state_province,
#         "City": city,
#         "Rural or Urban": rural_or_urban,
#         "Type of Residence": type_of_residence,
#         "Length of Residence": length_of_residence,
#         "Level of Education": level_of_education,
#         "Field of Study": field_of_study,
#         "Occupation": occupation,
#         "Income Level": income_level,
#         "Social Class": social_class,
#         "Employment Status": employment_status,
#         "Home Ownership": home_ownership,
#         "Ethnicity": ethnicity,
#         "Language(s) Spoken": languages_spoken,
#         "Religion": religion,
#         "Cultural Practices": cultural_practices,
#         "Immigration Status": immigration_status,
#         "Hobbies and Interests": hobbies_and_interests,
#         "Shopping Preferences": shopping_preferences,
#         "Dietary Preferences": dietary_preferences,
#         "Physical Activity Levels": physical_activity_levels,
#         "Social Media Usage": social_media_usage,
#         "Travel Habits": travel_habits,
#         "Alcohol and Tobacco Use": alcohol_tobacco_use,
#         "Technology Usage": technology_usage,
#         "Family Structure": family_structure,
#         "Household Size": household_size,
#         "Pet Ownership": pet_ownership,
#         "Relationship Status": relationship_status,
#         "Caregiving Responsibilities": caregiving_responsibilities,
#         "General Health Status": general_health_status,
#         "Disabilities or Chronic Illnesses": disabilities_or_chronic_illnesses,
#         "Mental Health Status": mental_health_status,
#         "Health Insurance Status": health_insurance_status,
#         "Access to Healthcare": access_to_healthcare,
#         "Political Affiliation": political_affiliation,
#         "Voting Behavior": voting_behavior,
#         "Political Engagement": political_engagement
#     }

#     prompt = json.dumps(prompt_data)
#     return prompt_data

# input=prompt_test(gender_identity="24-30",country_of_residence="Phillipines",occupation="Financial services industry")
# system_prompt = {k: v for k, v in input.items() if v is not None}
# prompt = json.dumps({k: None for k in input.keys()})
# print(json.dumps(system_prompt))
# print(prompt)