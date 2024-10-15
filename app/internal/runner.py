import traceback
from typing import Dict, Optional



import app.mongo_config as mongo_db
from app.internal import simulation
from app.data_models import SurveyModel, DemographicModel, AgentParameters

from concurrent.futures import ProcessPoolExecutor, as_completed


from app.api_clients.mclaps_demgen import MclapsDemgenClient, DemgenRequest


import time


demgen = MclapsDemgenClient()

#demgen_task_id used as batch id for data logging
def run_simulation(sim_id: str, demgen_task_id: str, survey: Dict, agent_params: AgentParameters, n_workers: Optional[int]=5) -> None:
    
    
    try:
        database = mongo_db.database["requests"]
    except Exception as e:
        traceback.print_exc()
        raise Exception(f"Database connection failed: {e}")
    request_object_query = {"_id": sim_id}
    task_state = False
    demographic_profiles = None
    
   
    def update_batch_state(truth_value: bool):
        request_object = database.find_one(request_object_query)
        batch_states: dict = request_object["batch_states"]
        batch_states[demgen_task_id] = truth_value
        database.update_one(request_object_query, {"$set":{"batch_states": batch_states}})

    ######
    timeout = 100
    while task_state is False:
        try: 
            task_state = demgen.get_task_status(demgen_task_id)
            if task_state == True:
                break
            else: 
                time.sleep(10)
                timeout -= 1
                continue
        except Exception as e:
            traceback.print_exc()
            update_batch_state(False)
            raise Exception(f"Demgen task failed: {e}")
        
    demographic_profiles = demgen.get_task_results(demgen_task_id)

    #####
    

    try:
        simulation_instances = [simulation.Simulator(sim_id, survey=survey, demographic=demo, agent_params=agent_params) for demo in demographic_profiles]
    except Exception as e:
        traceback.print_exc()
        update_batch_state(False)
        raise Exception(f"Simulation instances failed: {e}")
    
    try:
        with ProcessPoolExecutor(max_workers = n_workers) as executor:
            tasks = [executor.submit(sim.simulate) for sim in simulation_instances]
            for task in tasks:
                task.result()
            
            #update request object     
            total_timesteps = database.find_one(request_object_query)["total_timesteps"]
            completed_timesteps = database.find_one(request_object_query)["completed_timesteps"]
            progress = 100*(completed_timesteps/total_timesteps)
            database.update_one(request_object_query, {"$set":{"progress": progress}})
            
        
        print(f"batch {demgen_task_id} for simulation {sim_id} completed.")
        update_batch_state(False)
        


    except Exception as e:
        traceback.print_exc()
        update_batch_state(False)
        raise Exception(f"batch {demgen_task_id} for simulation {sim_id} failed: {e}.")





        




