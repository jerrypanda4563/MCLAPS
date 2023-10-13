import traceback
from typing import Optional, Any

from app.internal import data_services, survey, simulation, demgen
import concurrent
import concurrent.futures


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
