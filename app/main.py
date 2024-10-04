import rq.registry
from app.internal import runner
from app.internal import data_services
import app.mongo_config as mongo_db
from app.redis_config import cache 
from app.data_models import SimulationParameters, SurveyModel
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
import traceback




demgen_client = MclapsDemgenClient()
application = FastAPI()
queue = rq.Queue(name = 'sim_requests', connection = cache, default_timeout=7200)
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


           
from rq.registry import FinishedJobRegistry, StartedJobRegistry, FailedJobRegistry

@application.get("/simulations/all_tasks")
async def all_tasks():
    try:
        queued_jobs = queue.jobs
        queued_job_ids = [job.id for job in queued_jobs]

        # Get started jobs
        started_registry = StartedJobRegistry(queue=queue)
        started_job_ids = started_registry.get_job_ids()


        # Get finished jobs
        finished_registry = FinishedJobRegistry(queue=queue)
        finished_job_ids = finished_registry.get_job_ids()


        # Get failed jobs
        failed_registry = FailedJobRegistry(queue=queue)
        failed_job_ids = failed_registry.get_job_ids()

        return {"finished tasks":  finished_job_ids, "started tasks": started_job_ids,  "queued tasks": queued_job_ids, "failed tasks": failed_job_ids}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {e}")

from rq.job import Job
@application.get("/simulations/kill_all")
async def kill_all():
    try:
        job_ids = queue.job_ids  # Retrieve all job IDs in the queue
        for job_id in job_ids:
            job = Job.fetch(job_id, connection=queue)
            job.cancel()  # Cancel the job

        # Optionally: You could also empty the queue after canceling all jobs
        queue.empty()
        return {"message": "All tasks killed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing tasks: {e}")

@application.get("/simulations/clear_queue")
async def clear_queue():
    try:
        queue.empty()
        return {"message": "Queue cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing tasks: {e}")

from app.api_clients.mclaps_demgen import MclapsDemgenClient, DemgenRequest
@application.post("/simulations/new_simulation")
async def new_simulation(sim_param: SimulationParameters):
    
    #unwraps simulation parameters
    
    if test.mongo_connection_test():
        print("MongoDB connection successful.")

        sim_id = str(uuid.uuid4())
        n_of_runs=sim_param.n_of_runs
        n_of_workers=sim_param.workers
        survey_params=sim_param.survey_params
        demographic_params=sim_param.demographic_params
        agent_params=sim_param.agent_params
        
        survey_object: dict = survey_params.dict()


        #############send demgen request here
        demgen = MclapsDemgenClient()
        try:
            demgen_task = demgen.demgen_request(DemgenRequest(number_of_samples=n_of_runs, sim_id = sim_id, sampling_conditions = demographic_params))
        except Exception as e:
            print(f"Demgen request failed: {e}")
            traceback.print_exc()
            return False
        
        task_ids = demgen_task["task_ids"] #list of task ids for each batch


        ####################

        #batching the simulation runs
        batch_size = 250
        if n_of_runs > batch_size:
        
            n_of_batches = n_of_runs // batch_size
            remainder_batch_size = n_of_runs % batch_size
            request_batch_sizes = [i for i in [batch_size] * n_of_batches + [remainder_batch_size] if i != 0]
            request_batches = []
            for batch, demgen_task_id in zip(request_batch_sizes, task_ids):
                request_batch = (batch, demgen_task_id)
                request_batches.append(request_batch)
        else:
            request_batches = [(n_of_runs, task_ids[0])]

        try:

            tasks = [queue.enqueue(
                runner.run_simulation, 
                args = (sim_id, demgen_task_id, survey_object, demographic_params, agent_params, batch_sample_size, n_of_workers), 
                retry = rq.Retry(max=3, interval = 10), 
                results_ttl = 7200, 
                timeout = 7200) 
                for batch_sample_size, demgen_task_id in request_batches]
            
        ####################

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=400,detail=f'Failed to initiate simulation task: {e}.') 
            
        

        
        queued_jobs = queue.get_job_ids()
        # Fetch started jobs, get queue positions of tasks
        started_registry = rq.registry.StartedJobRegistry(queue=queue)
        started_job_ids = started_registry.get_job_ids()
        all_job_ids = queued_jobs + started_job_ids
        job_position_map = {job_id: idx + 1 for idx, job_id in enumerate(all_job_ids)}
        queue_positions = [job_position_map.get(task.id, -1) for task in tasks]
        
        tasks_queued = {k:v for k,v in zip([task.id for task in tasks], request_batches)}
        data_object: Dict = {
            "_id":sim_id,
            "Queued Tasks": tasks_queued,
            "Survey Name": survey_params.name,
            "Survey Description": survey_params.context,
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
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")




# @application.get("/simulations/status")
# async def sim_status(sim_id: str):
#     if test.mongo_connection_test():
#         database = mongo_db.collection_simulations
#         try:
#             simulation_obj: Dict = database.find_one({"_id": sim_id})
#         except Exception as e:
#             raise HTTPException(status_code=404, detail=f"Simulation id {sim_id} doesnt exist {e}")
#         try:
#             queued_tasks: Dict = simulation_obj["Queued Tasks"]
#             task_states = []
#             for task_id in list(queued_tasks.keys()):
#                 task = queue.fetch_job(task_id)
#                 task_states.append(task.get_status())
            
#             if all(task == "finished" for task in task_states):
#                 database.update_one({"_id": sim_id}, {"$set": {"Run Status": False}})
#                 return {sim_id: f"Completed. {simulation_obj['Completed Runs']} out of {simulation_obj['Number of Runs']} runs completed."}
            
#             if all(task == "failed" for task in task_states):
#                 database.update_one({"_id": sim_id}, {"$set": {"Run Status": False}})
#                 return {sim_id: f"All tasks failed. Completed {simulation_obj['Completed Runs']} out of {simulation_obj['Number of Runs']} runs."}
            

#             return {
#                 sim_id: f"Running. {simulation_obj['Completed Runs']} out of {simulation_obj['Number of Runs']} runs completed.", 
#                 "Task Status": task_states
#                 }
        
#         except Exception as e:
#             return {sim_id: f"Run Status: {simulation_obj['Run Status']}. {simulation_obj['Completed Runs']} out of {simulation_obj['Number of Runs']} runs completed.",}
    
#     else:
#         raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")
        


@application.get("/simulations/status")
def sim_status(sim_id: str) -> Dict:
    if test.mongo_connection_test():
        database = mongo_db.collection_simulations
        simulation_obj: Dict = database.find_one({"_id": sim_id})
        if simulation_obj:
            return {
                "simulation_id": sim_id,
                "status": simulation_obj["Run Status"],
                "progress": f" {simulation_obj['Completed Runs']} out of {simulation_obj['Number of Runs']} completed",
                }
        else:
            raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")

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
       


