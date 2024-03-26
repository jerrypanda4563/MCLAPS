import traceback
import json
from typing import Dict, Optional
import time

import app.mongo_config as mongo_db
from app.internal import simulation

from app.internal.demgen import Demographic_Generator
from concurrent.futures import ProcessPoolExecutor, as_completed

def run_simulation(survey: Dict, demographic_parameters: Dict, agent_model: str, agent_temperature: float, n_of_runs: int, sim_id: str, n_workers: Optional[int]=5) -> bool:
    

    database = mongo_db.collection_simulations
    demographic_generator=Demographic_Generator(demo=demographic_parameters, n_of_results=n_of_runs)
    demographic_profiles=demographic_generator.generate_demographic_dataset()
    print("demographic profiles generated")
    simulation_instances = [simulation.Simulator(survey=survey, demographic=demo, agent_model=agent_model, agent_temperature=agent_temperature) for demo in demographic_profiles]
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


    
