import traceback
from typing import Dict, Optional



import app.mongo_config as mongo_db
from app.internal import simulation
from app.data_models import SurveyModel, DemographicModel, AgentParameters

from concurrent.futures import ProcessPoolExecutor, as_completed


from app.api_clients.mclaps_demgen import MclapsDemgenClient, DemgenRequest


import time


demgen = MclapsDemgenClient()


def run_simulation(sim_id: str, survey: Dict, demographic_parameters: DemographicModel, agent_params: AgentParameters, n_of_runs: int,  n_workers: Optional[int]=5) -> bool:
    
    database = mongo_db.collection_simulations


    # #manual counter creation in runner process for initial demgen thread
    # rate_limiter = mclapsrlClient()
    # rate_limiter.create_counter(agent_model)

    demographic_profiles = None
    try:
        demgen_task = demgen.demgen_request(DemgenRequest(number_of_samples=n_of_runs, sampling_conditions=demographic_parameters))
    except Exception as e:
        print(f"Demgen request failed: {e}")
        traceback.print_exc()
        return False
    
    task_ids = demgen_task["task_ids"] #list of task ids
    dataset_id = demgen_task["dataset_id"]
    task_states = False
    while task_states is False:
        task_states = demgen.get_task_status(task_ids)
        if task_states == True:
            demographic_profiles = demgen.get_task_results(task_ids)
            print("Demographic profiles received.")
        elif task_states == False:
            print("Demgen in progress.")
            time.sleep(5)
        else:
            print("Demgen task failed, ending simulation.")
            return False

    simulation_instances = [simulation.Simulator(survey=survey, demographic=demo, agent_params=agent_params) for demo in demographic_profiles]
    print("simulation instances created")
    n_of_completed_runs = 0

    try:
        with ProcessPoolExecutor(max_workers=n_workers) as executor:
            future_to_simulation = {executor.submit(sim.simulate): sim for sim in simulation_instances}
            for future in as_completed(future_to_simulation):
                n_of_completed_runs += 1
                result = future.result()
                result_response = result["response_data"]
                answers = [response["answer"] for response in result_response]
                query = {"_id": sim_id}
                database.update_one(query, {"$push":{"Simulation Result": result}})
                database.update_one(query, {"$inc":{"Completed Runs": 1}})
                print(f"Completed {n_of_completed_runs} of {n_of_runs} runs, responses are {answers}.")
                if n_of_completed_runs == n_of_runs:
                    run_status = False
                    database.update_one(query, {"$set":{"Run Status": run_status}})
                    print(f"All runs completed for simulation {sim_id}.")
                    return True
        
                
    except Exception as e:
        print(f"Thread pool was unexpectedly terminated: {e}.")
        traceback.print_exc()
        query = {"_id": sim_id}
        run_status = False
        database.update_one(query, {"$set":{"Run Status": run_status}})
        return False


    
