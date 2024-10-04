import traceback
from typing import Dict, Optional



import app.mongo_config as mongo_db
from app.internal import simulation
from app.data_models import SurveyModel, DemographicModel, AgentParameters

from concurrent.futures import ProcessPoolExecutor, as_completed


from app.api_clients.mclaps_demgen import MclapsDemgenClient, DemgenRequest


import time


demgen = MclapsDemgenClient()


def run_simulation(sim_id: str, demgen_task_id: str, survey: Dict, agent_params: AgentParameters, n_of_runs: int, n_workers: Optional[int]=5) -> bool:
    
    database = mongo_db.collection_simulations
    task_states = False
    demographic_profiles = None
    while task_states is False:
        try:
            task_states = demgen.get_task_status(list(demgen_task_id))
            if task_states == True:
                demographic_profiles = demgen.get_task_results(list(demgen_task_id))
                print(f"{demographic_profiles}")
                print("Demographic profiles received.")
            elif task_states == False:
                print("Demgen in progress.")
                time.sleep(10)
            else:
                print("Demgen task failed, ending simulation.")
                return False
        except Exception as e:
            print(f"Demgen task error: {e}")
            #add function to delete the demgen task in demgen
            # demgen_client.delete_task(demgen_task_id)
            traceback.print_exc()
            query = {"_id": sim_id}
            run_status = False
            database.update_one(query, {"$set":{"Run Status": run_status}})
            return False

    simulation_instances = [simulation.Simulator(survey=survey, demographic=demo, agent_params=agent_params) for demo in demographic_profiles]
    print("simulation instances created")
    n_of_completed_runs = 0



    try:
        with ProcessPoolExecutor(max_workers = n_workers) as executor:
            future_to_simulation = {executor.submit(sim.simulate): sim for sim in simulation_instances}
            for future in as_completed(future_to_simulation):
                n_of_completed_runs += 1
                result = future.result()
                result_response = result["response_data"]
                answers = [response["answer"] for response in result_response]
                query = {"_id": sim_id}
                database.update_one(query, {"$push":{"Simulation Result": result}})
                database.update_one(query, {"$inc":{"Completed Runs": 1}})
                print(f"Completed {n_of_completed_runs} of {n_of_runs} runs.")
                if n_of_completed_runs == n_of_runs:
                    query = {"_id": sim_id}
                    runs_total = database.find_one(query, "Number of Runs")
                    runs_completed = database.find_one(query, "Completed Runs")
                    if runs_total == runs_completed:
                        run_status = False
                        database.update_one(query, {"$set":{"Run Status": run_status}})
                        print(f"All runs completed for simulation {sim_id}.")
                        return True
                    else:
                        print(f"Task batch completed. Simulation {sim_id} has {runs_completed} of {runs_total} runs completed.")
                        return True
        
                
    except Exception as e:
        print(f"Thread pool was unexpectedly terminated: {e}.")
        traceback.print_exc()
        query = {"_id": sim_id}
        run_status = False
        database.update_one(query, {"$set":{"Run Status": run_status}})
        return False



#new function for batching inside running function
# import rq
# from app.redis_config import cache


# queue = rq.Queue(name = 'sim_requests', connection = cache, default_timeout=7200)

# def run(sim_id: str, survey: Dict, demographic_parameters: DemographicModel, agent_params: AgentParameters, n_of_runs: int,  n_workers: Optional[int]=5) -> bool:
#     database = mongo_db.collection_simulations

#     batch_size = 250
#     if n_of_runs > batch_size:
    
#         n_of_batches = n_of_runs // batch_size
#         remainder_batch_size = n_of_runs % batch_size
#         request_batches = [i for i in [batch_size] * n_of_batches + [remainder_batch_size] if i != 0]
#     else:
#         request_batches = [n_of_runs]

#     demographic_profiles = []
#     for i, batch in enumerate(request_batches):
        




