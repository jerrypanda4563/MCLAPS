import rq.registry
from app.internal import runner
from app.internal import data_services
import app.mongo_config as mongo_db
from app.redis_config import cache 
from app.data_models import SimulationParameters
import app.api_clients.mclapsrl as mclapsrl

from tests import test
from typing import Dict, List

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import os
import json

import rq


import uuid

from app.api_clients.mclaps_demgen import MclapsDemgenClient

import logging





demgen_client = MclapsDemgenClient()
application = FastAPI()
queue = rq.Queue(name = 'sim_requests', connection = cache)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@application.get("/")
async def root():
    return{"API Connection": "Success!"}


@application.get("/connection_test")
async def test_services():

    openai_status=test.openai_connection_test()
    mongo_status=test.mongo_connection_test()
    redis_status=test.redis_connection_test()
    mclapsrl_client = mclapsrl.mclapsrlClient()
    mclapsrl_status = mclapsrl_client.check_service_status()
    demgen_client = MclapsDemgenClient()
    demgen_status = demgen_client.service_status()

    return {
        "OpenAI Status": openai_status, 
        "Mongo Status": mongo_status,
        "Redis Status": redis_status, 
        "RateLimiter Status": mclapsrl_status, 
        "Demgen Status": demgen_status
        }




@application.post("/simulations/new_simulation")
async def new_simulation(sim_param: SimulationParameters,
                                background_tasks: BackgroundTasks):
    
    #unwraps simulation parameters

    if test.mongo_connection_test():
        print("MongoDB connection successful.")

        sim_id = str(uuid.uuid4())
        n_of_runs=sim_param.n_of_runs
        n_of_workers=sim_param.workers
        survey_params=sim_param.survey_params
        demographic_params=sim_param.demographic_params
        agent_params=sim_param.agent_params
        
        survey_object: Dict[str, List[Dict]] = {
            "description": survey_params.description,
            "questions": [json.loads(question.json()) for question in survey_params.questions]
        }

        #batching the simulation runs
        batch_size = 250
        if n_of_runs > batch_size:
        
            n_of_batches = n_of_runs // batch_size
            remainder_batch_size = n_of_runs % batch_size
            request_batches = [i for i in [batch_size] * n_of_batches + [remainder_batch_size] if i != 0]
        
        else:
            request_batches = [n_of_runs]

        try:
            tasks = [queue.enqueue(runner.run_simulation, args = (sim_id, survey_object, demographic_params, agent_params, batch_sample_size, n_of_workers), retry = rq.Retry(max=3, interval = 10), results_ttl = 3600) for batch_sample_size in request_batches]
            
            queued_jobs = queue.jobs
            started_registry = rq.registry.StartedJobRegistry(queue=queue)
            started_job_ids = started_registry.get_job_ids()
            started_jobs = [queue.fetch_job(job_id) for job_id in started_job_ids]
            all_jobs = started_jobs + queued_jobs
            job_ids = [job.id for job in all_jobs]
            queue_positions = [(job_ids.index(task.id) + 1) for task in tasks]
            logger.info(f"Tasks {tasks} enqueued, queue position: {queue_positions}.")
        except Exception as e:
            raise HTTPException(status_code=400,detail=f'Failed to initiate simulation task: {e}.')
        
        tasks_queued = {k:v for k,v in zip([task.id for task in tasks], request_batches)}

        data_object: Dict = {
            "_id":sim_id,
            "Queued Tasks": tasks_queued,
            "Survey Name": survey_params.name,
            "Survey Description": survey_params.description,
            "Survey Questions": [json.loads(question.json()) for question in survey_params.questions],
            "Target Demographic": json.loads(demographic_params.json()),
            "Number of Runs": n_of_runs,
            "Completed Runs": 0,
            "Run Status": True,
            "Simulation Result": []
        }
        database = mongo_db.collection_simulations
        database.insert_one(data_object)
        

        # try:
        #     background_tasks.add_task(runner.run_simulation, sim_id, survey_object, demographic_params, agent_params, n_of_runs, n_of_workers)
        # except Exception as e:
        #     raise HTTPException(status_code=400,detail=f'Failed to initiate simulation task: {e}.')

        return {"task_id": [task.id for task in tasks], "simulation_id": sim_id, "queue_position": queue_positions} 
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")




@application.get("/simulations/status")
async def sim_status(sim_id: str):
    if test.mongo_connection_test():
        database = mongo_db.collection_simulations
        try:
            simulation_obj: Dict = database.find_one({"_id": sim_id})
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Simulation id {sim_id} doesnt exist {e}")

        queued_tasks: Dict = simulation_obj["Queued Tasks"]
        task_states = []
        for task_id in list(queued_tasks.keys()):
            task = queue.fetch_job(task_id)
            task_states.append(task.get_status())
        
        if all(task == "finished" for task in task_states):
            database.update_one({"_id": sim_id}, {"$set": {"Run Status": False}})
            return {sim_id: f"Completed. {simulation_obj['Completed Runs']} out of {simulation_obj['Number of Runs']} runs completed."}
        
        if all(task == "failed" for task in task_states):
            database.update_one({"_id": sim_id}, {"$set": {"Run Status": False}})
            return {sim_id: f"All tasks failed. Completed {simulation_obj['Completed Runs']} out of {simulation_obj['Number of Runs']} runs."}
        

        return {sim_id: f"Running. {simulation_obj['Completed Runs']} out of {simulation_obj['Number of Runs']} runs completed.", "Task Status": task_states}
        
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")
            
            




@application.get("/simulations/simulation_status")
async def simulation_status(sim_id: str):
    if test.mongo_connection_test():
        print("MongoDB connection successful.")
        database = mongo_db.collection_simulations
        obj: Dict = database.find_one({"_id": sim_id})
        if obj:
            run_status = obj["Run Status"]
            completed_runs = obj["Completed Runs"]
            total_runs = obj["Number of Runs"]
            return {"Run Status": run_status, "Completion Percentage": f"{completed_runs} out of {total_runs} runs completed."}
        else:
            raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")

        
    

@application.get("/simulations/load_simulation")
async def load_simulation(sim_id: str) -> Dict:
    if test.mongo_connection_test():
        database = mongo_db.collection_simulations
        obj: Dict = database.find_one({"_id": sim_id})
        if obj:
            return obj
        else:
            raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")
        
        
@application.get("/simulations/load_simulation/csv")
async def load_simulation_csv(sim_id: str, file_path = "./simulations"):
    if test.mongo_connection_test():
        print("MongoDB connection successful.")
        database = mongo_db.collection_simulations
        obj: Dict = database.find_one({"_id": sim_id})
        if obj:    
            try:
                data_services.create_csv_from_simulation_results(sim_data=obj)
                file_path = f"{file_path}/{sim_id}_Simulation_Results.csv"
                survey_name: str = obj["Survey Name"]

            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error creating CSV file: {e}")
            if not os.path.isfile(file_path):
                raise HTTPException(status_code=404, detail="CSV file not found.")
            
            return FileResponse(path=file_path, media_type='text/csv', filename=f"{survey_name}_{sim_id}_Simulation_Results.csv")
        
        else:
            raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")
       


