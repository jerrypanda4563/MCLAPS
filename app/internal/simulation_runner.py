import traceback
from typing import Dict, Optional
import json
import openai.error
import time


from app.redis_config import cache
import app.mongo_config as mongo_db
import app.mongo_config as mongo_config

from app.internal import simulation

from app.internal.celery import simulator
import concurrent
import concurrent.futures





def run_single_simulation(s: Dict, demo: Dict):
    try:
        inst = simulation.Simulation(survey = s["Survey Questions"], context = s["Survey Description"], demo = demo)
        inst.run()
        simulation_data = {
            "response_data": inst.responses,
            "demographic_data": inst.demographic_data
        }  
        return simulation_data
    
    except Exception as e:
        print(f"An error occurred in a single simulation run: {e}.")
        traceback.print_exc()
        return None


#@simulator.task  for setting up celery in future
def get_simulation_data(n_of_results: int, s:Dict, demo: Dict, sim_id: str, workers: Optional[int] = 15):
    
    #simulation variables
    n_of_successful_runs = 0
    max_retries = 5
    retries = 0
    num_workers = workers

    #check mongo status before simulation
    mongo_status=mongo_config.db_connection_test()
    if mongo_status is False:
        return



    while n_of_successful_runs < n_of_results and retries < max_retries:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:  
            future_to_simulation = {executor.submit(run_single_simulation, s, demo): _
                                    for _ in range(n_of_results - n_of_successful_runs)}

            for future in concurrent.futures.as_completed(future_to_simulation):
                try:
                    simulation_result = future.result()
                    if simulation_result is not None:  # if simulation was successful
                        n_of_successful_runs += 1
                        #############caching to redis as temp list
                        cache.rpush("r"+sim_id, json.dumps(simulation_result))
                        #############
                        print(f"Completion state:"+str(n_of_successful_runs))
                
                except Exception as e:  # exception while getting result from future
                    print(f"An error occurred in simulation runner while getting result from future: {e}. Retrying...")
                    print(traceback.format_exc())
                    retries += 1

        if n_of_successful_runs < n_of_results:
            print(
                f"After {retries} retries, {n_of_successful_runs} simulations completed successfully. Retrying the "
                f"remaining simulations..."
                )

    #completes the set in redis with "Simulation Result" as key and value being all simulation data serialized
    simulation_results = cache.lrange("r"+sim_id, 0, -1)
    decoded_results = [result.decode('utf-8') for result in simulation_results]
    simulation_results_serialized = json.dumps(decoded_results)
    cache.hset(sim_id,"Simulation Result", simulation_results_serialized)
    
    #setting simulation status to true 
    cache.hset(sim_id, "Simulation Status", "true")

    ### code for pushing chunk to mongodb once all simulation done
    data={
        "_id":sim_id,
        "Survey Name":(cache.hget(sim_id,"Survey Name")).decode('utf-8'),
        "Survey Description":cache.hget(sim_id, "Survey Description").decode('utf-8'),
        "Survey Questions": json.loads(cache.hget(sim_id, "Survey Questions").decode('utf-8')),
        "Target Demographic": json.loads(cache.hget(sim_id, "Target Demographic").decode('utf-8')),
        "Number of Runs": cache.hget(sim_id, "Number of Runs").decode('utf-8'),
        "Simulation Status": cache.hget(sim_id, "Simulation Status").decode('utf-8'),
        "Simulation Result": json.loads(cache.hget(sim_id,"Simulation Result").decode('utf-8'))
    }
    try: 
        database_collection=mongo_db.collection_simulations
        database_collection.insert_one(data)
        print(f'Simulation data successfully saved to mongodb')
        print(f"Successfully simulated {n_of_successful_runs} out of {n_of_results}.")
        return data 
    except mongo_config.PyMongoError as e:
        print(f'Mongo Error {e}.')
        return data
    
        

    ###
 



