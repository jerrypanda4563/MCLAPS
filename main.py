import traceback

import demgen
import survey
import simulation
import data_services
import concurrent
from typing import Dict, Any, Optional, Union, List
from typing import List
import concurrent.futures

import terminal

# global variables
# class data_var:
#     def __init__(self):
survey_array = {
    "survey_name": "",
    "survey_questions": None
}

survey_description = None


def create_survey(survey_name: str):
    return survey.Survey(survey_name)


# def post_survey_description(description: str):
#     global survey_description
#     survey_description = description


def post_short_answer_question(ques: str, s: survey.Survey):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_short_answer_question(question=ques)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")


def post_long_answer_question(ques: str):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_long_answer_question(question=ques)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")


def post_checkboxes_question(ques: str, choices: List[str]):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_checkboxes_question(question=ques, choices=choices)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")


def post_multiple_choice_question(ques: str, choices: List[str]):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_multiple_choice_question(question=ques, choices=choices)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")


def post_linear_scale_question(ques: str, min_val: int, max_val: int):
    global survey_array
    if survey_array:
        survey_array["survey_questions"].add_linear_scale_question(question=ques, min_value=min_val, max_value=max_val)
        survey_array["survey_questions"].show()
    else:
        print("create_survey first")


def get_simulation_data(n_of_results: int, s: survey.Survey, demo: demgen.Demographic, context=None):
    data_services.create_demographic_csv(filename='./simulations/' + s.name + '_demographics.csv')
    s.create_csv('./simulations/' + s.name + '.csv')

    n_of_successful_runs = 0
    max_retries = 5
    retries = 0

    # if n_of_results == 1:
    #     dump responses and return

    while n_of_successful_runs < n_of_results and retries < max_retries:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # using 4 threads, but adjust as needed
            future_to_simulation = {executor.submit(run_single_simulation, s, demo, context): _
                                    for _ in range(n_of_results - n_of_successful_runs)}

            for future in concurrent.futures.as_completed(future_to_simulation):
                try:
                    result = future.result()
                    if result is not None:  # if simulation was successful
                        n_of_successful_runs += 1
                except Exception as e:  # exception while getting result from future
                    print(f"An error occurred: {e}. Retrying...")
                    print(traceback.format_exc())
                    retries += 1

        if n_of_successful_runs < n_of_results:
            print(
                f"After {retries} retries, {n_of_successful_runs} simulations completed successfully. Retrying the "
                f"remaining simulations...")

    print(f"Successfully simulated {n_of_successful_runs} out of {n_of_results}.")


def run_single_simulation(s: survey.Survey, demo: demgen.Demographic, context=None) -> Optional[dict[str, Any]]:
    try:
        inst = simulation.Simulation(survey=s.questions, demo=demo, context=context)
        inst.update_demographic_parameters(demo)
        inst.run()
        simulation_data = {
            "response_data": inst.responses,
            "demographic_data": inst.demographic_data
        }
        data_services.append_demographic(filename='./simulations/' + s.name + '_demographics.csv',
                                         data=simulation_data['demographic_data'])
        data_services.append_response(filename='./simulations/' + s.name + '.csv',
                                      data=simulation_data['response_data'])
        return simulation_data
    except Exception as e:
        print(f"An error occurred: {e}.")
        return None


def price_simulation(age: int, demographic: map, prompt: str):
    # fill the survey
    price_simulation()
    return


def price_simulation() -> survey.Survey:
    s = survey.Survey("price simulation")
    s.add_long_answer_question("what is the name of your company")
    return s


def new_price_demographic() -> demgen.Demographic:
    d = demgen.Demographic(gender_identity="female, male, queer")
    return d


def main():
    invictus_survey = survey.Survey("Osman Simulation")
    invictus_survey.add_long_answer_question(
        'What is the timescale and cost of MEP and HVAC installation jobs within buildings?')
    invictus_survey.add_long_answer_question(
        'In your experience, what are the factors negatively effecting the MEP and HVAC installation jobs within '
        'buildings?')
    invictus_survey.add_long_answer_question(
        'What specific technologies or tools do you utilize to enhance productivity and address these factors?')
    invictus_survey.add_long_answer_question(
        'Could you describe a recent project where you encountered significant physical challenges to do with these '
        'jobs?')
    invictus_survey.add_long_answer_question(
        'How open are you (or your organisation) to adopting new innovations and technology in your work? If so Have '
        'you adopted/implemented any?')

    demo = demgen.Demographic(country_of_residence='United Kingdom and Europe', employment_status='Full-time',
                              occupation=['construction builder', 'construction project manager',
                                          'construction project consultant', 'building services engineer'])
    get_simulation_data(1, invictus_survey, demo)


if __name__ == "__main__":
    terminal.pricing_simulation(1)
