import openai
import json

import settings

openai.api_key = settings.OPEN_AI_KEY


class Demographic:
    def __init__(
            self,
            gender_identity=None,
            age=None,
            date_of_birth=None,
            marital_status=None,
            sexual_orientation=None,
            nationality=None,
            country_of_residence=None,
            state_province=None,
            city=None,
            rural_or_urban=None,
            type_of_residence=None,
            length_of_residence=None,
            level_of_education=None,
            field_of_study=None,
            occupation=None,
            income_level=None,
            social_class=None,
            employment_status=None,
            home_ownership=None,
            ethnicity=None,
            languages_spoken=None,
            religion=None,
            cultural_practices=None,
            immigration_status=None,
            hobbies_and_interests=None,
            shopping_preferences=None,
            dietary_preferences=None,
            physical_activity_levels=None,
            social_media_usage=None,
            travel_habits=None,
            alcohol_tobacco_use=None,
            technology_usage=None,
            family_structure=None,
            household_size=None,
            pet_ownership=None,
            relationship_status=None,
            caregiving_responsibilities=None,
            general_health_status=None,
            disabilities_or_chronic_illnesses=None,
            mental_health_status=None,
            health_insurance_status=None,
            access_to_healthcare=None,
            political_affiliation=None,
            voting_behavior=None,
            political_engagement=None,
    ) -> None:
        self.gender_identity = gender_identity
        self.age = age
        self.date_of_birth = date_of_birth
        self.marital_status = marital_status
        self.sexual_orientation = sexual_orientation
        self.nationality = nationality
        self.country_of_residence = country_of_residence
        self.state_province = state_province
        self.city = city
        self.rural_or_urban = rural_or_urban
        self.type_of_residence = type_of_residence
        self.length_of_residence = length_of_residence
        self.level_of_education = level_of_education
        self.field_of_study = field_of_study
        self.occupation = occupation
        self.income_level = income_level
        self.social_class = social_class
        self.employment_status = employment_status
        self.home_ownership = home_ownership
        self.ethnicity = ethnicity
        self.languages_spoken = languages_spoken
        self.religion = religion
        self.cultural_practices = cultural_practices
        self.immigration_status = immigration_status
        self.hobbies_and_interests = hobbies_and_interests
        self.shopping_preferences = shopping_preferences
        self.dietary_preferences = dietary_preferences
        self.physical_activity_levels = physical_activity_levels
        self.social_media_usage = social_media_usage
        self.travel_habits = travel_habits
        self.alcohol_tobacco_use = alcohol_tobacco_use
        self.technology_usage = technology_usage
        self.family_structure = family_structure
        self.household_size = household_size
        self.pet_ownership = pet_ownership
        self.relationship_status = relationship_status
        self.caregiving_responsibilities = caregiving_responsibilities
        self.general_health_status = general_health_status
        self.disabilities_or_chronic_illnesses = disabilities_or_chronic_illnesses
        self.mental_health_status = mental_health_status
        self.health_insurance_status = health_insurance_status
        self.access_to_healthcare = access_to_healthcare
        self.political_affiliation = political_affiliation
        self.voting_behavior = voting_behavior
        self.political_engagement = political_engagement


def generate_demographic(demo: Demographic):
    prompt_data = {
        "Gender Identity": demo.gender_identity,
        "Age": demo.age,
        "Date of Birth": demo.date_of_birth,
        "Marital Status": demo.marital_status,
        "Sexual Orientation": demo.sexual_orientation,
        "Nationality": demo.nationality,
        "Country of Residence": demo.country_of_residence,
        "State/Province": demo.state_province,
        "City": demo.city,
        "Rural or Urban": demo.rural_or_urban,
        "Type of Residence": demo.type_of_residence,
        "Length of Residence": demo.length_of_residence,
        "Level of Education": demo.level_of_education,
        "Field of Study": demo.field_of_study,
        "Occupation": demo.occupation,
        "Income Level": demo.income_level,
        "Social Class": demo.social_class,
        "Employment Status": demo.employment_status,
        "Home Ownership": demo.home_ownership,
        "Ethnicity": demo.ethnicity,
        "Language(s) Spoken": demo.languages_spoken,
        "Religion": demo.religion,
        "Cultural Practices": demo.cultural_practices,
        "Immigration Status": demo.immigration_status,
        "Hobbies and Interests": demo.hobbies_and_interests,
        "Shopping Preferences": demo.shopping_preferences,
        "Dietary Preferences": demo.dietary_preferences,
        "Physical Activity Levels": demo.physical_activity_levels,
        "Social Media Usage": demo.social_media_usage,
        "Travel Habits": demo.travel_habits,
        "Alcohol and Tobacco Use": demo.alcohol_tobacco_use,
        "Technology Usage": demo.technology_usage,
        "Family Structure": demo.family_structure,
        "Household Size": demo.household_size,
        "Pet Ownership": demo.pet_ownership,
        "Relationship Status": demo.relationship_status,
        "Caregiving Responsibilities": demo.caregiving_responsibilities,
        "General Health Status": demo.general_health_status,
        "Disabilities or Chronic Illnesses": demo.disabilities_or_chronic_illnesses,
        "Mental Health Status": demo.mental_health_status,
        "Health Insurance Status": demo.health_insurance_status,
        "Access to Healthcare": demo.access_to_healthcare,
        "Political Affiliation": demo.political_affiliation,
        "Voting Behavior": demo.voting_behavior,
        "Political Engagement": demo.political_engagement
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
            {"role": "system",
             "content": "Create a demographic profile by replacing null values for the undefined parameters in the json dictionary. The pre-defined constrained values are:\n" + system_prompt + "\nReplace the pre-defined constrained value with a value falling within the category. The output must contain the same json keys and have the same data structure as the input."},
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
