import survey
import simulation
import data_services
import concurrent
from typing import Dict
from typing import List
import concurrent.futures



#global variables
# class data_var:
#     def __init__(self):
survey_array = {
"survey_name":"",
"survey_questions":None
}
demographic_parameters = {}
survey_description=None



#command line callables
def post_demographics(gender_identity=None, age=None, date_of_birth=None,
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
    global demographic_parameters
    demographic_parameters.update({
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
    })

def create_survey(survey_name:str):
    global survey_array
    survey_array["survey_name"]=survey_name
    survey_array["survey_questions"]=survey.Survey()
    return survey_array

def post_survey_description(description:str):
    global survey_description
    survey_description=description

def post_short_answer_question(ques:str):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_short_answer_question(question=ques)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")


def post_long_answer_question(ques:str):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_long_answer_question(question=ques)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")

def post_checkboxes_question(ques:str,choices:List[str]):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_checkboxes_question(question=ques,choices=choices)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")

def post_multiple_choice_question(ques:str,choices:List[str]):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_multiple_choice_question(question=ques,choices=choices)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")

def post_linear_scale_question(ques:str, min_val:int, max_val:int):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_linear_scale_question(question=ques,min_value=min_val,max_value=max_val)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")

def get_simulation_data(n_of_results: int):

    global survey_array
    global demographic_parameters
    global survey_description

    def run_single_simulation():
        global survey_array
        global demographic_parameters
        global survey_description
        try:
            inst = simulation.simulate(survey=survey_array['survey_questions'].show(),context=survey_description)
            inst.update_demographic_parameters(demographic_parameters)
            inst.run()
            simulation_data={
                "response_data": inst.responses,
                "demographic_data": inst.demographic_data
            } 
            data_services.append_demographic(filename='./simulations/' + survey_array['survey_name'] + '_demographics.csv',data=simulation_data['demographic_data'])
            data_services.append_response(filename='./simulations/' + survey_array['survey_name'] + '.csv',data=simulation_data['response_data'])
            return simulation_data
        except Exception as e:
            print(f"An error occurred: {e}.")
            return None
        
    data_services.create_demographic_csv(filename='./simulations/' + survey_array['survey_name'] + '_demographics.csv')
    survey_array['survey_questions'].create_csv('./simulations/' + survey_array['survey_name'] + '.csv')

    n_of_successful_runs = 0
    max_retries = 5
    retries = 0

    while n_of_successful_runs < n_of_results and retries < max_retries:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # using 4 threads, but adjust as needed
            future_to_simulation = {executor.submit(run_single_simulation): _ for _ in range(n_of_results - n_of_successful_runs)}
            
            for future in concurrent.futures.as_completed(future_to_simulation):
                try:
                    result = future.result()
                    if result is not None:  # if simulation was successful
                        n_of_successful_runs += 1
                except Exception as e:  # exception while getting result from future
                    print(f"An error occurred: {e}. Retrying...")
                    retries += 1

        if n_of_successful_runs < n_of_results:
            print(f"After {retries} retries, {n_of_successful_runs} simulations completed successfully. Retrying the remaining simulations...")

    print(f"Successfully simulated {n_of_successful_runs} out of {n_of_results}.")



def run_single_simulation():
    global survey_array
    global demographic_parameters
    try:
        inst = simulation.simulate(survey=survey_array['survey_questions'].show())
        inst.update_demographic_parameters(demographic_parameters)
        inst.run()
        simulation_data={
            "response_data": inst.responses,
            "demographic_data": inst.demographic_data
        } 
        data_services.append_demographic(filename='./simulations/' + survey_array['survey_name'] + '_demographics.csv',data=simulation_data['demographic_data'])
        data_services.append_response(filename='./simulations/' + survey_array['survey_name'] + '.csv',data=simulation_data['response_data'])
        return simulation_data
    except Exception as e:
        print(f"An error occurred: {e}.")
        return None